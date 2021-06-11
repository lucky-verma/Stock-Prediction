import streamlit as st
import time
import json
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import graphviz as graphviz
import src.admin_dash
import src.user_dash

PAGES = {
    "Home": src.admin_dash,
    "Resources": src.user_dash,
}

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# @st.cache(allow_output_mutation=True)
# def modelLoading():
#     return model

def riskProfile():
    """
        Maths
    """
    return


def main():
    # temp scores
    riskScores = {'investAmount': 0, 'age': 0, 'duration': 0, 'investFor': 0, 'anticipate': 0, 'investKnowledge': 0,
                  'secure': 0, 'totalInvest': 0}
    RiskProfiles = ['Conservative', 'Moderate', 'Balanced', 'Assertive', 'Aggressive']
    finalRiskProfile = None
    tempExpReturns = None
    tempExpReturnsScore = 0
    tempMaxDraw = None
    tempMaxDrawScore = 0

    # UI
    st.title('QuniQ')
    st.subheader("Risk Profiler")

    # st.sidebar.title("Navigation")
    # selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    #
    # page = PAGES[selection]

    name = st.text_input('NAME')
    age = st.select_slider('Age (Years)', options=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                                                   32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                                                   49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 'Above 60'])
    investAmount = st.number_input('Investment Amount')
    duration = st.slider('Investment Duration (Years)', min_value=1, max_value=50)
    investFor = st.selectbox('Investing For?', ('Home', "Child's Education", 'Emergency Fund', 'retirement', 'Income'))
    # goal = st.selectbox('Investment Goal', ('Preserve value or minimize risk.', 'Emphasize current income.',
    #                                         'Generate current income and gradually growth over time.',
    #                                         'Growth over time and generate some current income.',
    #                                         'Substantially growth over time and do not generate current income.'))
    anticipate = st.selectbox("How much you anticipate needing a portion of your invested funds before completion of "
                              "the duration of your investment?",
                              ('Less than 10%',
                               'Between 10% - 30%',
                               'Between 30% - 50%',
                               'More than 50%'))
    investKnowledge = st.selectbox("How familiar are you with investment matters?", ('Not familiar', 'Not very familiar'
                                                                                     , 'Somewhat familiar',
                                                                                     'Fairly familiar',
                                                                                     'Very familiar'))
    secure = st.selectbox('How secure is your current and future income from sources such as salary, pensions or other '
                          'investments?', ('Not secure', 'Somewhat secure', 'Fairly secure', 'Very secure'))
    totalInvest = st.selectbox('What is the proportion the amount you are investing respect of your total investment '
                               'assets?', ('Less than 10%',
                                           'Between 10% - 30%',
                                           'Between 30% - 50%',
                                           'More than 50%'))

    try:
        # Age
        if age == 'Above 60':
            riskScores['age'] = 1
        elif age >= 60:
            riskScores['age'] = 1
        elif 59 >= age >= 50:
            riskScores['age'] = 3
        elif 50 >= age >= 40:
            riskScores['age'] = 5
        elif 40 >= age >= 30:
            riskScores['age'] = 7
        elif 30 >= age >= 15:
            riskScores['age'] = 9

        # Investment Amount
        if investAmount >= 10 ** 7:
            riskScores['investAmount'] = 9
        elif 10 ** 7 >= investAmount >= 10 ** 7 * 0.75:
            riskScores['investAmount'] = 7
        elif 10 ** 7 * 0.75 >= investAmount >= 10 ** 7 * 0.5:
            riskScores['investAmount'] = 5
        elif 10 ** 7 * 0.5 >= investAmount >= 10 ** 7 * 0.25:
            riskScores['investAmount'] = 3
        elif 10 ** 7 * 0.25 >= investAmount:
            riskScores['investAmount'] = 1

        # Duration of Investment
        if duration >= 25:
            riskScores['duration'] = 9
        elif 25 >= duration >= 16:
            riskScores['duration'] = 7
        elif 15 >= duration >= 11:
            riskScores['duration'] = 5
        elif 10 >= duration >= 6:
            riskScores['duration'] = 3
        elif 5 >= duration >= 1:
            riskScores['duration'] = 1

        # Investment for
        if investFor == 'retirement' and age == 'Above 60':
            riskScores['investFor'] = 1
        elif investFor == 'retirement' and 60 >= age >= 35:
            riskScores['investFor'] = 1
        elif investFor == 'retirement' and 35 >= age >= 26:
            riskScores['investFor'] = 3
        elif investFor == 'retirement' and 25 >= age >= 20:
            riskScores['investFor'] = 5
        elif investFor == 'retirement' and 20 >= age >= 15:
            riskScores['investFor'] = 7
        elif investFor == 'Home':
            riskScores['investFor'] = 3
        elif investFor == "Child's Education":
            riskScores['investFor'] = 5
        elif investFor == 'Income':
            riskScores['investFor'] = 9
        elif investFor == 'Emergency Fund':
            riskScores['investFor'] = 3

        # anticipate
        if anticipate == 'Less than 10%':
            riskScores['anticipate'] = 9
        elif anticipate == 'Between 10% - 30%':
            riskScores['anticipate'] = 7
        elif anticipate == 'Between 30% - 50%':
            riskScores['anticipate'] = 3
        elif anticipate == 'More than 50%':
            riskScores['anticipate'] = 1

        # Investment Knowledge
        if investKnowledge == 'Not familiar':
            riskScores['investKnowledge'] = 1
        elif investKnowledge == 'Not very familiar':
            riskScores['investKnowledge'] = 3
        elif investKnowledge == 'Somewhat familiar':
            riskScores['investKnowledge'] = 5
        elif investKnowledge == 'Fairly familiar':
            riskScores['investKnowledge'] = 7
        elif investKnowledge == 'Very familiar':
            riskScores['investKnowledge'] = 9

        # Security
        if secure == 'Not secure':
            riskScores['secure'] = 1
        elif secure == 'Somewhat secure':
            riskScores['secure'] = 3
        elif secure == 'Fairly secure':
            riskScores['secure'] = 5
        elif secure == 'Very secure':
            riskScores['secure'] = 7

        # Total Investment Proportion
        if totalInvest == 'Less than 10%':
            riskScores['totalInvest'] = 9
        elif totalInvest == 'Between 10% - 30%':
            riskScores['totalInvest'] = 7
        elif totalInvest == 'Between 30% - 50%':
            riskScores['totalInvest'] = 3
        elif totalInvest == 'More than 50%':
            riskScores['totalInvest'] = 1
    except Exception as e:
        print(e)

    # local generated values
    print(riskScores)
    totalRiskScore = sum(riskScores.values())

    # Risk Profile brackets
    if totalRiskScore >= 56:
        finalRiskProfile = RiskProfiles[4]
        tempExpReturns = 20
        tempMaxDraw = '23.70-33.79%'
        tempExpReturnsScore = 5
        tempMaxDrawScore = 5
    elif 56 >= totalRiskScore >= 42:
        finalRiskProfile = RiskProfiles[3]
        tempExpReturns = 16
        tempMaxDraw = '17.63-23.70%'
        tempExpReturnsScore = 4
        tempMaxDrawScore = 4
    elif 42 >= totalRiskScore >= 28:
        finalRiskProfile = RiskProfiles[2]
        tempExpReturns = 12
        tempMaxDraw = '13.15-17.63%'
        tempExpReturnsScore = 3
        tempMaxDrawScore = 3
    elif 28 >= totalRiskScore >= 14:
        finalRiskProfile = RiskProfiles[1]
        tempExpReturns = 8
        tempMaxDraw = '11.21-13.15%'
        tempExpReturnsScore = 2
        tempMaxDrawScore = 2
    elif 14 >= totalRiskScore >= 0:
        finalRiskProfile = RiskProfiles[0]
        tempExpReturns = 4
        tempMaxDraw = '9.78-11.21%'
        tempExpReturnsScore = 1
        tempMaxDrawScore = 1

    print(totalRiskScore, finalRiskProfile)

    # Auto Populated Section (Can be altered)
    with st.spinner("Loading ..."):
        expReturns = st.slider('Expected Returns (Auto-generated)', value=tempExpReturns, min_value=0, max_value=25)

        maxDraw = st.select_slider('Drawdown Tolerance (Auto-generated)', value=tempMaxDraw,
                                   options=['9.78-11.21%', '11.21-13.15%', '13.15-17.63%', '17.63-23.70%', '23.70-33'
                                                                                                           '.79%'])
        # filters = st.multiselect('Asset Filters (Auto-generated)', ['Equity', 'ETFs', 'Mutual Funds', 'Bonds'])
        # shortTermAll = st.slider('Short Term Allocation (% of Funding Amount) (Auto-generated)', min_value=0,
        # max_value=25)


if __name__ == '__main__':
    main()
