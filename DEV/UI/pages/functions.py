import os
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

os.environ['NUMBA_DISABLE_JIT'] = '1'  # uncomment this if you want to use pypfopt within simulation
from numba import njit

import vectorbt as vbt  # version 0.16.1
from vectorbt.generic.nb import nanmean_nb
from vectorbt.portfolio.nb import create_order_nb, auto_call_seq_ctx_nb
from vectorbt.portfolio.enums import SizeType, Direction
import riskfolio.ConstraintsFunctions as cf
import riskfolio.Portfolio as pf
import riskfolio.HCPortfolio as hc
import riskfolio.RiskFunctions as rk
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings("ignore")


def prep_func_nb(simc, every_nth):
    # Define rebalancing days
    simc.active_mask[:, :] = False
    simc.active_mask[every_nth::every_nth, :] = True
    return ()


def segment_prep_func_nb(sc, find_weights_nb, rm, model, obj, history_len, ann_factor, num_tests, srb_sharpe):
    if history_len == -1:
        # Look back at the entire time period
        close = sc.close[:sc.i, sc.from_col:sc.to_col]
    else:
        # Look back at a fixed time period
        if sc.i - history_len <= 0:
            return (np.full(sc.group_len, np.nan),)  # insufficient data
        close = sc.close[sc.i - history_len:sc.i, sc.from_col:sc.to_col]

    # Find optimal weights
    best_sharpe_ratio, weights = find_weights_nb(sc, rm, model, obj, close, num_tests)
    srb_sharpe[sc.i] = best_sharpe_ratio

    # Update valuation price and reorder orders
    size_type = np.full(sc.group_len, SizeType.TargetPercent)
    direction = np.full(sc.group_len, Direction.LongOnly)
    temp_float_arr = np.empty(sc.group_len, dtype=np.float_)
    for k in range(sc.group_len):
        col = sc.from_col + k
        sc.last_val_price[col] = sc.close[sc.i, col]
    auto_call_seq_ctx_nb(sc, weights, size_type, direction, temp_float_arr)

    return (weights,)


def order_func_nb(oc, weights):
    col_i = oc.call_seq_now[oc.call_idx]
    return create_order_nb(
        size=weights[col_i],
        size_type=SizeType.TargetPercent,
        price=oc.close[oc.i, oc.col]
    )


def backTest(shock, freq):
    print("Scenario - " + shock, str(freq) + " Days ")
    # Loading data
    industry = pd.read_excel('index constituents/industy_class_list.xlsx', index_col=0, engine='openpyxl')

    if shock == 'shock':
        data = pd.read_excel('data/updated_EQ_POC.xlsx', index_col=0, engine='openpyxl')
        data.index = pd.DatetimeIndex(data.index)
        data_NSE_shock = pd.read_excel('data/NSE_shock.xlsx', index_col=0, engine='openpyxl')
        data_NSE_shock.index = pd.DatetimeIndex(data_NSE_shock.index)
        data_NSE = data_NSE_shock['Adj Close']
    else:
        data = pd.read_excel('data/updated_EQ_POC.xlsx', index_col=0, engine='openpyxl')
        data = data[:1506]
        data.index = pd.DatetimeIndex(data.index)
        data_NSE_no_shock = pd.read_excel('data/NSE_no_shock.xlsx', index_col=0, engine='openpyxl')
        data_NSE_no_shock.index = pd.DatetimeIndex(data_NSE_no_shock.index)
        data_NSE = data_NSE_no_shock['Adj Close']

    Y = data.pct_change().dropna()

    clusters = cf.assets_clusters(returns=Y,
                                  correlation='spearman',
                                  linkage='ward',
                                  k=None,
                                  max_k=11,
                                  leaf_order=True)

    clusters = clusters.sort_index()
    clusters = pd.merge(clusters,
                        industry[['Symbol', 'Industry']],
                        left_on='Assets',
                        right_on='Symbol')

    del clusters['Symbol']

    constraints = {'Disabled': [False, False, False],
                   'Type': ['All Assets', 'All Classes', 'All Classes'],
                   'Set': ['', 'Clusters', 'Industry'],
                   'Position': ['', '', ''],
                   'Sign': ['<=', '<=', '<='],
                   'Weight': [0.05, 0.4, 0.4],
                   'Type Relative': ['', '', ''],
                   'Relative Set': ['', '', ''],
                   'Relative': ['', '', ''],
                   'Factor': ['', '', '']}

    constraints = pd.DataFrame(constraints)

    A, B = cf.assets_constraints(constraints, clusters)

    vbt.settings.returns['year_freq'] = '252 days'

    num_tests = 2000
    ann_factor = data.vbt.returns(freq='D').ann_factor

    assets = Y.columns.tolist()

    def opt_weights(sc, rm, model, obj, close, num_tests):
        # Calculate expected returns and sample covariance matrix
        close = pd.DataFrame(close, columns=assets)
        returns = close.pct_change().dropna()

        #    model = model # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
        #    rm = rm # Risk measure used, this time will be variance
        #    obj = 'MinRisk' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
        hist = True  # Use historical scenarios for risk measures that depend on scenarios
        rf = 0  # Risk free rate
        l = 0  # Risk aversion factor, only useful when obj is 'Utility'

        if model == 'Classic':

            # Building the portfolio object
            port = pf.Portfolio(returns=returns)

            # Select method and estimate input parameters:

            method_mu = 'hist'  # Method to estimate expected returns based on historical data.
            method_cov = 'hist'  # Method to estimate covariance matrix based on historical data.

            port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

            port.ainequality = A
            port.binequality = B

            # Calculating optimum portfolio
            #         port.solvers = ['MOSEK']

            w = port.optimization(model=model,
                                  rm=rm,
                                  obj=obj,
                                  rf=rf,
                                  l=l,
                                  hist=hist)

            weights = np.ravel(w.to_numpy())
            shp = rk.Sharpe(w, port.mu, cov=port.cov, returns=returns, rm=rm, rf=0, alpha=0.05)

        elif model == 'kelly':

            # Building the portfolio object
            port = pf.Portfolio(returns=returns)

            # Select method and estimate input parameters:

            method_mu = 'hist'  # Method to estimate expected returns based on historical data.
            method_cov = 'hist'  # Method to estimate covariance matrix based on historical data.

            port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

            port.ainequality = A
            port.binequality = B

            # Calculating optimum portfolio
            #         port.solvers = ['MOSEK']

            w = port.optimization(model='Classic',
                                  rm=rm,
                                  obj=obj,
                                  kelly='exact',
                                  rf=rf,
                                  l=l,
                                  hist=hist)

            weights = np.ravel(w.to_numpy())
            shp = rk.Sharpe(w, port.mu, cov=port.cov, returns=returns, rm=rm, rf=0, alpha=0.05)

        elif model in ['HRP', 'HERC']:

            port = hc.HCPortfolio(returns=returns)
            #        model=model # Could be HRP or HERC
            correlation = 'pearson'  # Correlation matrix used to group assets in clusters
            #        rm = rm # Risk measure used, this time will be variance
            rf = 0  # Risk free rate
            linkage = 'ward'  # Linkage method used to build clusters
            max_k = 11  # Max number of clusters used in two difference gap statistic
            leaf_order = True  # Consider optimal order of leafs in dendrogram

            w = port.optimization(model=model,
                                  correlation=correlation,
                                  rm=rm,
                                  rf=rf,
                                  linkage=linkage,
                                  max_k=max_k,
                                  leaf_order=leaf_order)

            weights = np.ravel(w.to_numpy())
            shp = rk.Sharpe(w, returns.mean(), cov=port.cov, returns=returns, rm=rm, rf=0, alpha=0.05)

        return shp, weights

    # Risk Measures available:
    #
    # 'MV': Standard Deviation.
    # 'MAD': Mean Absolute Deviation.
    # 'MSV': Semi Standard Deviation.
    # 'FLPM': First Lower Partial Moment (Omega Ratio).
    # 'SLPM': Second Lower Partial Moment (Sortino Ratio).
    # 'CVaR': Conditional Value at Risk.
    # 'EVaR': Entropic Value at Risk.
    # 'WR': Worst Realization (Minimax)
    # 'MDD': Maximum Drawdown of uncompounded returns (Calmar Ratio).
    # 'ADD': Average Drawdown of uncompounded returns.
    # 'CDaR': Conditional Drawdown at Risk of uncompounded returns.
    # 'UCI': Ulcer Index of uncompounded returns.

    # rms = ["MV", "MSV", "CVaR", "EVaR", "WR"] * 2  # + ["MV"]*2
    # models = ["Classic"] * 10  # + ["HRP", 'HERC']
    # objs = ["MinRisk"] * 5 + ["Sharpe"] * 5  # + ["HC"]*2

    rms = ["MV"] * 2
    models = ["Classic"] * 2
    objs = ["MinRisk"] + ["Sharpe"]

    sharpe = {}
    portfolio = {}

    for i, j, k in zip(rms, models, objs):
        sharpe[k + "-" + j + "-" + i] = np.full(data.shape[0], np.nan)
        profile = k + "-" + j + "-" + i
        print(profile)
        # Run simulation with a custom order function (Numba should be disabled)
        portfolio[k + "-" + j + "-" + i] = vbt.Portfolio.from_order_func(
            data,
            order_func_nb,
            prep_func_nb=prep_func_nb,
            prep_args=(int(freq),),  # Rebalance frequency 21 a 252
            segment_prep_func_nb=segment_prep_func_nb,
            segment_prep_args=(opt_weights, i, j, k, 252 * 1, ann_factor, num_tests, sharpe[k + "-" + j + "-" + i]),
            cash_sharing=True,
            group_by=True,
            freq='D',
            incl_unrealized=True,
            seed=42
        )

    # a = portfolio['MinRisk-Classic-WR'].value().iloc[252*3+252:]
    # values = pd.DataFrame([])
    # values = pd.concat([values, a], axis=1, join='outer')

    values = pd.DataFrame([])
    stats = pd.DataFrame([])
    weights = {}

    for i, j, k in zip(rms, models, objs):
        a = portfolio[k + "-" + j + "-" + i].value().iloc[252 * 2:]
        b = a.pct_change().vbt.returns(freq='D').stats(0)
        w = portfolio[k + "-" + j + "-" + i].holding_value(group_by=False).vbt / portfolio[
            k + "-" + j + "-" + i].value()
        idx = np.flatnonzero((portfolio[k + "-" + j + "-" + i].share_flow() != 0).any(axis=1))
        w = w.iloc[idx, :]
        values = pd.concat([values, a], axis=1, join='outer')
        stats = pd.concat([stats, b], axis=1)
        weights[k + "-" + j + "-" + i] = w

    values.columns = ['Your Portfolio', 'Your PortFolio']
    stats.columns = zip(objs, models, rms)


    data_NSE_2 = data_NSE.reindex(values.index).fillna(method='ffill')
    data_NSE_2 = data_NSE_2.to_frame()
    data_NSE_2.columns = ['NIFTY 50']
    a = data_NSE_2 / data_NSE_2.iloc[0] * 100
    # display(a)
    b = data_NSE_2.pct_change().vbt.returns(freq='D').stats(0).T
    values = pd.concat([values, a], axis=1)
    stats = pd.concat([stats, b], axis=1)

    fig, ax = plt.subplots(figsize=(16, 7))
    values.plot(ax=ax)
    print('plotted')
    print('-----------------')

    return weights, values, stats
