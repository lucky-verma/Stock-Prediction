import streamlit as st
from .multipage import save, MultiPage

# lookup list
expReturnsRange = ['0', '2.40% - 6.19%', '6.19%	- 10.07%', '10.07% - 14.03%', '14.03% - 18.07%', '18.07% - 21.85%']
RiskProfiles = ['Conservative', 'Moderate', 'Balanced', 'Assertive', 'Aggressive']
volatilityRange = ['0', '3.35% - 4.34%', '4.34% - 6.30%', '6.30% - 8.72%', '8.72% - 11.36%', '11.36% - 16.81%']
maxDailyRange = ['0', '1.59% - 1.86%', '1.86% - 2.13%', '2.13% - 2.73%', '2.73 - 3.64%', '3.64% - 5.60%']
maxDrawRange = ['0', '9.78% - 11.21%', '11.21% - 13.15%', '13.15% - 17.63%', '17.63% - 23.70%', '23.70% - 33.79%']


def app1(prev_vars):  # First page
    if prev_vars is not None:
        start_index = prev_vars  # Defines the start index for a selectbox (defined below) as the option previously
        # chosen by the user
    else:
        start_index = 1  # Defines the start index for a selectbox (defined below) as 1

    riskScores = {'investAmount': 0, 'age': 0, 'duration': 0, 'investFor': 0, 'anticipate': 0, 'investKnowledge': 0,
                  'secure': 0, 'totalInvest': 0}
    finalRiskProfile = None
    tempExpReturns = None
    tempExpReturnsScore = 0
    tempMaxDraw = None
    tempMaxDrawScore = 0

    # UI
    main_left, main_right = st.beta_columns((1, 0.2))
    with main_left:
        st.title('**User Profile**')
        st.subheader("")
    with main_right:
        st.image('data/quniq.png')

    """
    ### Profile
    """
    left, right = st.beta_columns(2)

    with left:
        name = st.text_input('NAME')
        age = st.select_slider('Age (Years)',
                               options=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                                        32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                                        49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 'Above 60'])
        investAmount = st.number_input('Investment Amount', value=100000)
        duration = st.slider('Investment Duration (Years)', min_value=1, max_value=50)
        investFor = st.selectbox('Investing For?',
                                 ('Home', "Child's Education", 'Emergency Fund', 'Retirement', 'Income'))
        # goal = st.selectbox('Investment Goal', ('Preserve value or minimize risk.', 'Emphasize current income.',
        #                                         'Generate current income and gradually growth over time.',
        #                                         'Growth over time and generate some current income.',
        #                                         'Substantially growth over time and do not generate current income.'))

        anticipate = st.selectbox("How much you anticipate needing a portion of your invested funds before completion "
                                  "of "
                                  "the duration of your investment?",
                                  ('Less than 10%',
                                   'Between 10% - 30%',
                                   'Between 30% - 50%',
                                   'More than 50%'))
    with right:
        investKnowledge = st.selectbox("How familiar are you with investment matters?",
                                       ('Not familiar', 'Not very familiar'
                                        , 'Somewhat familiar',
                                        'Fairly familiar',
                                        'Very familiar'))

        secure = st.selectbox('How secure is your current and future income from sources such as salary, pensions or '
                              'other '
                              'investments?', ('Not secure', 'Somewhat secure', 'Fairly secure', 'Very secure'))
        totalInvest = st.selectbox('What is the proportion the amount you are investing respect of your total '
                                   'investment '
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
        # print(riskScores)
        totalRiskScore = sum(riskScores.values())

        # Risk Profile brackets
        if totalRiskScore >= 56:
            finalRiskProfile = RiskProfiles[4]
            tempMaxDraw = '23.70-33.79%'
            tempExpReturnsScore = 5
            tempMaxDrawScore = 5
        elif 56 >= totalRiskScore >= 42:
            finalRiskProfile = RiskProfiles[3]
            tempMaxDraw = '17.63-23.70%'
            tempExpReturnsScore = 4
            tempMaxDrawScore = 4
        elif 42 >= totalRiskScore >= 28:
            finalRiskProfile = RiskProfiles[2]
            tempMaxDraw = '13.15-17.63%'
            tempExpReturnsScore = 3
            tempMaxDrawScore = 3
        elif 28 >= totalRiskScore >= 14:
            finalRiskProfile = RiskProfiles[1]
            tempMaxDraw = '11.21-13.15%'
            tempExpReturnsScore = 2
            tempMaxDrawScore = 2
        elif 14 >= totalRiskScore >= 0:
            finalRiskProfile = RiskProfiles[0]
            tempMaxDraw = '9.78-11.21%'
            tempExpReturnsScore = 1
            tempMaxDrawScore = 1

        # print(totalRiskScore, finalRiskProfile)

        # Auto Populated Section (Can be altered)
        with st.spinner("Loading ..."):
            st.markdown("***")
            expReturns = st.slider('Expected Returns (% p.a.) (Auto-generated)', value=int(totalRiskScore // 3.2),
                                   min_value=0
                                   , max_value=25)

            maxDraw = st.select_slider('Drawdown Tolerance (Auto-generated)', value=tempMaxDraw,
                                       options=['9.78-11.21%', '11.21-13.15%', '13.15-17.63%', '17.63-23.70%',
                                                '23.70-33'
                                                '.79%'])
            # filters = st.multiselect('Asset Filters (Auto-generated)', ['Equity', 'ETFs', 'Mutual Funds', 'Bonds'])
            # shortTermAll = st.slider('Short Term Allocation (% of Funding Amount) (Auto-generated)', min_value=0,
            # max_value=25)

    st.markdown("***")
    if st.button("Generate Portfolio..."):
        st.spinner()
        with st.spinner(text='Processing...'):
            st.success("Profile Saved")
            save(var_list=[name, age, investAmount, duration, investFor, anticipate, investKnowledge, secure,
                           totalInvest, totalRiskScore, finalRiskProfile, expReturns, tempMaxDrawScore], name="App1",
                 page_names=["Generated Portfolio", "Portfolio Management",
                             "Admin Panel"])  # Saves the variables to be used on the second, third & fourth pages.
        ######

    # Shows how to set placeholders based on a selection

    # new_var_list = ["This framework rocks!", "This framework is really cool!", "I really liked this framework!"]
    # new_var = st.selectbox("Select an option: ", new_var_list,
    #                        index=start_index)  # Creates a selectbox in order to show how to keep the option chosen
    # by the user even after he leaves the page...
    # start_index = new_var_list.index(new_var)

    # save([start_index], "placeholder1",
    #      ["App2", "App3"])  # Saves the variable "start_index" to be used again on the first page
