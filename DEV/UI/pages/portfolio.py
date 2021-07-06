import streamlit as st
from .multipage import save
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from .functions import backTest

# lookup list
expReturnsRange = ['0', '2.40% - 6.19%', '6.19%	- 10.07%', '10.07% - 14.03%', '14.03% - 18.07%', '18.07% - 21.85%']
RiskProfiles = ['Conservative', 'Moderate', 'Balanced', 'Assertive', 'Aggressive']
volatilityRange = ['0', '3.35% - 4.34%', '4.34% - 6.30%', '6.30% - 8.72%', '8.72% - 11.36%', '11.36% - 16.81%']
maxDailyRange = ['0', '1.59% - 1.86%', '1.86% - 2.13%', '2.13% - 2.73%', '2.73 - 3.64%', '3.64% - 5.60%']
maxDrawRange = ['0', '9.78% - 11.21%', '11.21% - 13.15%', '13.15% - 17.63%', '17.63% - 23.70%', '23.70% - 33.79%']


def app2(prev_vars):  # Portfoio page

    if type(prev_vars) is int:  # Checks if the user saved the variables previously
        st.write("Ooops... You forgot to generate portfolio...")
        start_index = prev_vars
        save([start_index], "placeholder", ["App1"])

    else:
        left_generated, right_generated, process, write = st.beta_columns((0.3, 0.3, 0.4, 0.2))
        with left_generated:
            scenarios = st.radio("Select the possible scenarios", ['Shock', 'No Shock'])
        with right_generated:
            re_balancing = st.radio("Select the Rebalance Frequency", ['Anually', 'Monthly'])
        with process:
            backTestProcess = st.button('Back Test')
        with write:
            st.image('data/quniq.png')
        if backTestProcess:
            if scenarios == 'No Shock' and re_balancing == 'Anually':
                st.spinner()
                with st.spinner(text='Portfolio Generation & Backtesting...'):
                    weights, values, stats = backTest(shock='no_shock', freq=252, prev_vars=prev_vars)
            elif scenarios == 'No Shock' and re_balancing == 'Monthly':
                st.spinner()
                with st.spinner(text='Portfolio Generation & Backtesting...'):
                    weights, values, stats = backTest(shock='no_shock', freq=21, prev_vars=prev_vars)
            elif scenarios == 'Shock' and re_balancing == 'Anually':
                st.spinner()
                with st.spinner(text='Portfolio Generation & Backtesting...'):
                    weights, values, stats = backTest(shock='shock', freq=252, prev_vars=prev_vars)
            else:
                st.spinner()
                with st.spinner(text='Portfolio Generation & Backtesting...'):
                    weights, values, stats = backTest(shock='shock', freq=21, prev_vars=prev_vars)

            ############## TODO: add new temps

            print('Portfolio Page', prev_vars)

            # Dummy Data
            text = [['Equity', '% share']]

            st.info("## Back-Testing ")

            if prev_vars[-3] == "Balanced":
                # st.dataframe(stats)

                stats.columns = ['MinRisk-Classic-MSV', 'Sharpe-Classic-CVaR', 'NIFTY 50']
                del values['Your Portfolio']
                st.line_chart(values, use_container_width=True)

                st.info("## Statistics")

                returns_data_matrix = [['INITIAL INVESTMENT', prev_vars[2]],
                                       ['CURRENT POT', int(prev_vars[2] + prev_vars[2] * 0.01 * float(
                                           "{:.2f}".format(stats['Sharpe-Classic-CVaR'][3])))],
                                       ['HORIZON YEARS', prev_vars[3]],
                                       ['ANNUAL RETURN [% p.a.]', "{:.2f}".format(stats["Sharpe-Classic-CVaR"][5])],
                                       ['SHARPE RATIO', "{:.2f}".format(stats["Sharpe-Classic-CVaR"][7])],
                                       ['MAX. DRAWDOWN [%]', "{:.2f}".format(stats["Sharpe-Classic-CVaR"][9])],
                                       # ['EXPECTED VOLATILITY', volatilityRange[prev_vars[12]]],
                                       ['ANNUAL VOLATILITY [YOUR PORTFOLIO]',
                                        "{:.2f}".format(stats["Sharpe-Classic-CVaR"][6])],
                                       ['ANNUAL VOLATILITY [NIFTY]', "{:.2f}".format(stats["NIFTY 50"][6])],
                                       ]

                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                font = ['#ffffff', '#008B00', '#004F00', '#008B00', '#008B00', '#004F00',  '#004F00',
                        '#004F00']
                fig = ff.create_table(returns_data_matrix, colorscale=colorscale, font_colors=font, index=True)

                # Make text size larger
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 24

                st.plotly_chart(fig, use_container_width=True)

                st.info("## Holdings Split")
                x = weights['Sharpe-Classic-CVaR'].columns.tolist()
                y = [float("{:.3f}".format(element * 100)) for element in
                     weights['Sharpe-Classic-CVaR'].iloc[-1].tolist()]
                for k in range(len(x)):
                    text.append([x[k], y[k]])

                temp_bar_x = []
                temp_bar_y = []
                for j in text:
                    if j[1] != 0:
                        temp_bar_x.append(j[0])
                        temp_bar_y.append(j[1])
                # Use the hovertext kw argument for hover text
                fig = go.Figure(data=[go.Bar(x=[i[:-3] for i in temp_bar_x[1:]], y=temp_bar_y[1:],
                                             # hovertext=['27% market share', '24% market share', '19% market share']
                                             )])
                # Customize aspect
                fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                  marker_line_width=1.5, opacity=0.6)
                st.plotly_chart(fig, use_container_width=True)

                # Holding section
                st.info("## Holdings")
                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                # font = ['#FCFCFC', '#00EE00', '#008B00', '#004F00', '#660000', '#CD0000', '#FF3030']

                hodlings = []
                for m in text:
                    if m[1] != 0:
                        hodlings.append(m)

                fig = ff.create_table(hodlings, colorscale=colorscale)
                fig.layout.width = 250

                st.plotly_chart(fig, use_container_width=True)

                # Remaining cash
                st.info('Distribution')
                left, right = st.beta_columns((1, 1))
                with left:
                    st.success(str("{:.2f}".format(sum(temp_bar_y[1:]))) + "% Invested in Equities")
                with right:
                    st.success(str("{:.2f}".format(abs((100 - sum(temp_bar_y[1:]))))) + "% left in Cash")


            elif prev_vars[-3] == "Assertive":
                # st.dataframe(stats)

                stats.columns = ['MinRisk-Classic-MV', 'Sharpe-Classic-MV', 'NIFTY 50']
                del values['Your PortFolio']
                st.line_chart(values, use_container_width=True)

                st.info("## Statistics")

                returns_data_matrix = [['INITIAL INVESTMENT', prev_vars[2]],
                                       ['CURRENT POT', int(prev_vars[2] + prev_vars[2] * 0.01 * float(
                                           "{:.2f}".format(stats['MinRisk-Classic-MV'][3])))],
                                       ['HORIZON YEARS', prev_vars[3]],
                                       ['ANNUAL RETURN [% p.a.]', "{:.2f}".format(stats["MinRisk-Classic-MV"][5])],
                                       ['SHARPE RATIO', "{:.2f}".format(stats["MinRisk-Classic-MV"][7])],
                                       ['MAX. DRAWDOWN [%]', "{:.2f}".format(stats["MinRisk-Classic-MV"][9])],
                                       # ['EXPECTED VOLATILITY', volatilityRange[prev_vars[12]]],
                                       ['ANNUAL VOLATILITY [YOUR PORTFOLIO]',
                                        "{:.2f}".format(stats["MinRisk-Classic-MV"][6])],
                                       ['ANNUAL VOLATILITY [NIFTY]', "{:.2f}".format(stats["NIFTY 50"][6])],
                                       ]

                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                font = ['#ffffff', '#008B00', '#004F00', '#008B00', '#008B00',  '#004F00', '#004F00',
                        '#004F00']
                fig = ff.create_table(returns_data_matrix, colorscale=colorscale, font_colors=font, index=True)

                # Make text size larger
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 24

                st.plotly_chart(fig, use_container_width=True)

                st.info("## Holdings Split")
                x = weights['MinRisk-Classic-MV'].columns.tolist()
                y = [float("{:.3f}".format(element * 100)) for element in
                     weights['MinRisk-Classic-MV'].iloc[-1].tolist()]
                for k in range(len(x)):
                    text.append([x[k], y[k]])

                temp_bar_x = []
                temp_bar_y = []
                for j in text:
                    if j[1] != 0:
                        temp_bar_x.append(j[0])
                        temp_bar_y.append(j[1])
                # Use the hovertext kw argument for hover text
                fig = go.Figure(data=[go.Bar(x=[i[:-3] for i in temp_bar_x[1:]], y=temp_bar_y[1:],
                                             # hovertext=['27% market share', '24% market share', '19% market share']
                                             )])
                # Customize aspect
                fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                  marker_line_width=1.5, opacity=0.6)
                st.plotly_chart(fig, use_container_width=True)

                # Holding section
                st.info("## Holdings")
                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                # font = ['#FCFCFC', '#00EE00', '#008B00', '#004F00', '#660000', '#CD0000', '#FF3030']

                hodlings = []
                for m in text:
                    if m[1] != 0:
                        hodlings.append(m)

                fig = ff.create_table(hodlings, colorscale=colorscale)
                fig.layout.width = 250

                st.plotly_chart(fig, use_container_width=True)

                # Remaining cash
                st.info('Distribution')
                left, right = st.beta_columns((1, 1))
                with left:
                    st.success(str("{:.2f}".format(sum(temp_bar_y[1:]))) + "% Invested in Equities")
                with right:
                    st.success(str("{:.2f}".format(abs((100 - sum(temp_bar_y[1:]))))) + "% left in Cash")


            elif prev_vars[-3] == "Aggressive":

                stats.columns = ['MinRisk-Classic-MV', 'Sharpe-Classic-MV', 'NIFTY 50']
                del values['Your Portfolio']
                st.line_chart(values, use_container_width=True)

                st.info("## Statistics")

                returns_data_matrix = [['INITIAL INVESTMENT', prev_vars[2]],
                                       ['CURRENT POT', int(prev_vars[2] + prev_vars[2] * 0.01 * float(
                                           "{:.2f}".format(stats['Sharpe-Classic-MV'][3])))],
                                       ['HORIZON YEARS', prev_vars[3]],
                                       ['ANNUAL RETURN [% p.a.]', "{:.2f}".format(stats["Sharpe-Classic-MV"][5])],
                                       ['Sharpe Ratio', "{:.2f}".format(stats["Sharpe-Classic-MV"][7])],
                                       ['Max. Drawdown [%]', "{:.2f}".format(stats["Sharpe-Classic-MV"][9])],
                                       # ['Expected Volatility', volatilityRange[prev_vars[12]]],
                                       ['ANNUAL VOLATILITY [YOUR PORTFOLIO]',
                                        "{:.2f}".format(stats["Sharpe-Classic-MV"][6])],
                                       ['ANNUAL VOLATILITY [NIFTY]', "{:.2f}".format(stats["NIFTY 50"][6])],
                                       ]

                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                font = ['#ffffff', '#008B00', '#004F00', '#008B00', '#008B00',  '#004F00', '#004F00',
                        '#004F00']
                fig = ff.create_table(returns_data_matrix, colorscale=colorscale, font_colors=font, index=True)

                # Make text size larger
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 24

                st.plotly_chart(fig, use_container_width=True)

                st.info("## Holdings Split")
                x = weights['Sharpe-Classic-MV'].columns.tolist()
                y = [float("{:.3f}".format(element * 100)) for element in
                     weights['Sharpe-Classic-MV'].iloc[-1].tolist()]
                for k in range(len(x)):
                    text.append([x[k], y[k]])

                temp_bar_x = []
                temp_bar_y = []
                for j in text:
                    if j[1] != 0:
                        temp_bar_x.append(j[0])
                        temp_bar_y.append(j[1])
                # Use the hovertext kw argument for hover text
                fig = go.Figure(data=[go.Bar(x=[i[:-3] for i in temp_bar_x[1:]], y=temp_bar_y[1:],
                                             # hovertext=['27% market share', '24% market share', '19% market share']
                                             )])
                # Customize aspect
                fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                  marker_line_width=1.5, opacity=0.6)
                st.plotly_chart(fig, use_container_width=True)

                # Holding section
                st.info("## Holdings")

                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                # font = ['#FCFCFC', '#00EE00', '#008B00', '#004F00', '#660000', '#CD0000', '#FF3030']

                hodlings = []
                for m in text:
                    if m[1] != 0:
                        hodlings.append(m)

                fig = ff.create_table(hodlings, colorscale=colorscale)
                fig.layout.width = 250

                st.plotly_chart(fig, use_container_width=True)

                # Writing the excel file
                # writer = pd.ExcelWriter('Backtesting_{0}.xlsx'.format(prev_vars[0]), engine='xlsxwriter')
                # values.to_excel(writer, sheet_name='Values')
                # stats.to_excel(writer, sheet_name='Stats')
                # for i in weights.keys():
                #     weights[i].to_excel(writer, sheet_name=i)
                #
                # writer.save()

                # Remaining cash
                st.info('Distribution')
                left, right = st.beta_columns((1, 1))
                with left:
                    st.success(str("{:.2f}".format(sum(temp_bar_y[1:]))) + "% Invested in Equities")
                with right:
                    st.success(str("{:.2f}".format(abs((100 - sum(temp_bar_y[1:])))) + "% left in Cash"))

            else:
                stats.columns = ['MinRisk-Classic-MSV', 'Sharpe-Classic-CVaR', 'NIFTY 50']
                # st.dataframe(stats)
                del values['Your PortFolio']
                st.line_chart(values, use_container_width=True)

                st.info("## Statistics")

                returns_data_matrix = [['INITIAL INVESTMENT', prev_vars[2]],
                                       ['CURRENT POT', int(prev_vars[2] + prev_vars[2] * 0.01 * float(
                                           "{:.2f}".format(stats['MinRisk-Classic-MSV'][3])))],
                                       ['HORIZON YEARS', prev_vars[3]],
                                       ['ANNUAL RETURN [% p.a.]', "{:.2f}".format(stats["MinRisk-Classic-MSV"][5])],
                                       ['SHARPE RATIO', "{:.2f}".format(stats["MinRisk-Classic-MSV"][7])],
                                       ['MAX. DRAWDOWN [%]', "{:.2f}".format(stats["MinRisk-Classic-MSV"][9])],
                                       # ['EXPECTED VOLATILITY', volatilityRange[prev_vars[12]]],
                                       ['ANNUAL VOLATILITY [YOUR PORTFOLIO]',
                                        "{:.2f}".format(stats["MinRisk-Classic-MSV"][6])],
                                       ['ANNUAL VOLATILITY [NIFTY]', "{:.2f}".format(stats["NIFTY 50"][6])],
                                       ]

                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                font = ['#ffffff', '#008B00', '#004F00', '#008B00', '#008B00',  '#004F00', '#004F00',
                        '#004F00']
                fig = ff.create_table(returns_data_matrix, colorscale=colorscale, font_colors=font, index=True)

                # Make text size larger
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 24

                st.plotly_chart(fig, use_container_width=True)

                st.info("## Holdings Split")
                x = weights['MinRisk-Classic-MSV'].columns.tolist()
                y = [float("{:.3f}".format(element * 100)) for element in
                     weights['MinRisk-Classic-MSV'].iloc[-1].tolist()]
                for k in range(len(x)):
                    text.append([x[k], y[k]])

                temp_bar_x = []
                temp_bar_y = []
                for j in text:
                    if j[1] != 0:
                        temp_bar_x.append(j[0])
                        temp_bar_y.append(j[1])
                # Use the hovertext kw argument for hover text
                fig = go.Figure(data=[go.Bar(x=[i[:-3] for i in temp_bar_x[1:]], y=temp_bar_y[1:],
                                             # hovertext=['27% market share', '24% market share', '19% market share']
                                             )])
                # Customize aspect
                fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                  marker_line_width=1.5, opacity=0.6)
                st.plotly_chart(fig, use_container_width=True)

                # Holding section
                st.info("## Holdings")
                colorscale = [[0, '#272D31'], [.5, '#ffffff'], [1, '#ffffff']]
                # font = ['#FCFCFC', '#00EE00', '#008B00', '#004F00', '#660000', '#CD0000', '#FF3030']

                hodlings = []
                for m in text:
                    if m[1] != 0:
                        hodlings.append(m)

                fig = ff.create_table(hodlings, colorscale=colorscale)
                fig.layout.width = 250

                st.plotly_chart(fig, use_container_width=True)

                # Remaining cash
                st.info('Distribution')
                left, right = st.beta_columns((1, 1))
                with left:
                    st.success(str("{:.2f}".format(sum(temp_bar_y[1:]))) + "% Invested in Equities")
                with right:
                    st.success(str("{:.2f}".format(abs((100 - sum(temp_bar_y[1:]))))) + "% left in Cash")

    #####
