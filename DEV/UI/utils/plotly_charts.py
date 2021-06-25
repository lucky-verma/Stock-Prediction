import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd


def multiple_axes(df1, df2):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    # eg. x=[1, 2, 3], y=[40, 50, 60]
    fig.add_trace(
        go.Scatter(x=df1[0], y=df1[1], name="yaxis data"),
        secondary_y=False,
    )

    # x=[1, 2, 3], y=[40, 50, 60]
    fig.add_trace(
        go.Scatter(x=df2[0], y=df2[1], name="yaxis2 data"),
        secondary_y=True,
    )

    # Add figure title
    # fig.update_layout(
    #     title_text="Volatility & Drawdown Index"
    # )

    # Set x-axis title
    fig.update_xaxes(title_text="Years")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Volatility</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Drawdown</b>", secondary_y=True)

    fig.update_layout(
        autosize=False,
        width=900,
        height=300, )

    return fig


def multi_time(df):
    fig = go.Figure()

    # Add traces TODO: Add more Traces and update layouts
    fig.add_trace(go.Scatter(
        x=df.index.tolist(),
        y=df['Your Portfolio'].tolist(),
        name="Your Portfolio",
        text=df['Your Portfolio'].tolist(),
        yaxis="y",
    ))

    fig.add_trace(go.Scatter(
        x=["2015-04-13", "2015-05-13", "2015-06-08", "2015-08-05", "2016-02-25"],
        y=["53.0", "69.0", "89.0", "41.0", "41.0"],
        name="var1",
        text=["53.0", "69.0", "89.0", "41.0", "41.0"],
        yaxis="y2",
    ))

    fig.add_trace(go.Scatter(
        x=["2013-01-29", "2013-02-26", "2013-04-19", "2013-07-02", "2013-08-27",
           "2013-10-22",
           "2014-01-20", "2014-04-09", "2014-05-05", "2014-07-01", "2014-09-30",
           "2015-02-09",
           "2015-04-13", "2015-06-08", "2016-02-25"],
        y=["9.6", "4.6", "2.7", "8.3", "18", "7.3", "3", "7.5", "1.0", "0.5", "2.8", "9.2",
           "13", "5.8", "6.9"],
        name="var2",
        text=["9.6", "4.6", "2.7", "8.3", "18", "7.3", "3", "7.5", "1.0", "0.5", "2.8",
              "9.2",
              "13", "5.8", "6.9"],
        yaxis="y3",
    ))

    fig.add_trace(go.Scatter(
        x=["2013-01-29", "2013-02-26", "2013-04-19", "2013-07-02", "2013-08-27",
           "2013-10-22",
           "2014-01-20", "2014-04-09", "2014-05-05", "2014-07-01", "2014-09-30",
           "2015-02-09",
           "2015-04-13", "2015-06-08", "2016-02-25"],
        y=["6.9", "7.5", "7.3", "7.3", "6.9", "7.1", "8", "7.8", "7.4", "7.9", "7.9", "7.6",
           "7.2", "7.2", "8.0"],
        name="var3",
        text=["6.9", "7.5", "7.3", "7.3", "6.9", "7.1", "8", "7.8", "7.4", "7.9", "7.9",
              "7.6",
              "7.2", "7.2", "8.0"],
        yaxis="y4",
    ))

    fig.add_trace(go.Scatter(
        x=["2013-02-26", "2013-07-02", "2013-09-26", "2013-10-22", "2013-12-04",
           "2014-01-02",
           "2014-01-20", "2014-05-05", "2014-07-01", "2015-02-09", "2015-05-05"],
        y=["290", "1078", "263", "407", "660", "740", "33", "374", "95", "734", "3000"],
        name="var4",
        text=["290", "1078", "263", "407", "660", "740", "33", "374", "95", "734", "3000"],
        yaxis="y5",
    ))

    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 0.5},
        marker={"size": 8},
        mode="lines+markers",
        showlegend=False
    )

    # Add annotations
    fig.update_layout(
        annotations=[
            dict(
                x="2013-06-01",
                y=0,
                arrowcolor="rgba(63, 81, 181, 0.2)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="state1",
                xref="x",
                yanchor="bottom",
                yref="y"
            ),
            dict(
                x="2014-09-13",
                y=0,
                arrowcolor="rgba(76, 175, 80, 0.1)",
                arrowsize=0.3,
                ax=0,
                ay=30,
                text="state2",
                xref="x",
                yanchor="bottom",
                yref="y"
            )
        ],
    )

    # Add shapes
    fig.update_layout(
        shapes=[
            dict(
                fillcolor="rgba(63, 81, 181, 0.2)",
                line={"width": 0},
                type="rect",
                x0="2013-01-15",
                x1="2013-10-17",
                xref="x",
                y0=0,
                y1=0.95,
                yref="paper"
            ),
            dict(
                fillcolor="rgba(76, 175, 80, 0.1)",
                line={"width": 0},
                type="rect",
                x0="2013-10-22",
                x1="2015-08-05",
                xref="x",
                y0=0,
                y1=0.95,
                yref="paper"
            )
        ]
    )

    # Update axes
    fig.update_layout(
        xaxis=dict(
            autorange=True,
            range=["2012-10-31 18:36:37.3129", "2016-05-10 05:23:22.6871"],
            rangeslider=dict(
                autorange=True,
                range=["2012-10-31 18:36:37.3129", "2016-05-10 05:23:22.6871"]
            ),
            type="date"
        ),
        yaxis=dict(
            anchor="x",
            autorange=True,
            domain=[0, 0.2],
            linecolor="#673ab7",
            mirror=True,
            range=[-60.0858369099, 28.4406294707],
            showline=True,
            side="right",
            tickfont={"color": "#673ab7"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#673ab7"},
            type="linear",
            zeroline=False
        ),
        yaxis2=dict(
            anchor="x",
            autorange=True,
            domain=[0.2, 0.4],
            linecolor="#E91E63",
            mirror=True,
            range=[29.3787777032, 100.621222297],
            showline=True,
            side="right",
            tickfont={"color": "#E91E63"},
            tickmode="auto",
            ticks="",
            titlefont={"color": "#E91E63"},
            type="linear",
            zeroline=False
        ),
        yaxis3=dict(
            anchor="x",
            autorange=True,
            domain=[0.4, 0.6],
            linecolor="#795548",
            mirror=True,
            range=[-3.73690396239, 22.2369039624],
            showline=True,
            side="right",
            tickfont={"color": "#795548"},
            tickmode="auto",
            ticks="",
            title="mg/L",
            titlefont={"color": "#795548"},
            type="linear",
            zeroline=False
        ),
        yaxis4=dict(
            anchor="x",
            autorange=True,
            domain=[0.6, 0.8],
            linecolor="#607d8b",
            mirror=True,
            range=[6.63368032236, 8.26631967764],
            showline=True,
            side="right",
            tickfont={"color": "#607d8b"},
            tickmode="auto",
            ticks="",
            title="mmol/L",
            titlefont={"color": "#607d8b"},
            type="linear",
            zeroline=False
        ),
        yaxis5=dict(
            anchor="x",
            autorange=True,
            domain=[0.8, 1],
            linecolor="#2196F3",
            mirror=True,
            range=[-685.336803224, 3718.33680322],
            showline=True,
            side="right",
            tickfont={"color": "#2196F3"},
            tickmode="auto",
            ticks="",
            title="mg/Kg",
            titlefont={"color": "#2196F3"},
            type="linear",
            zeroline=False
        )
    )

    # Update layout
    fig.update_layout(
        dragmode="zoom",
        hovermode="x",
        legend=dict(traceorder="reversed"),
        height=600,
        template="plotly_white",
        margin=dict(
            t=100,
            b=100
        ),
    )
