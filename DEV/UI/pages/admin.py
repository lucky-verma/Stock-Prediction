import streamlit as st
from .multipage import save

# lookup list
expReturnsRange = ['0', '2.40% - 6.19%', '6.19%	- 10.07%', '10.07% - 14.03%', '14.03% - 18.07%', '18.07% - 21.85%']
RiskProfiles = ['Conservative', 'Moderate', 'Balanced', 'Assertive', 'Aggressive']
volatilityRange = ['0', '3.35% - 4.34%', '4.34% - 6.30%', '6.30% - 8.72%', '8.72% - 11.36%', '11.36% - 16.81%']
maxDailyRange = ['0', '1.59% - 1.86%', '1.86% - 2.13%', '2.13% - 2.73%', '2.73 - 3.64%', '3.64% - 5.60%']
maxDrawRange = ['0', '9.78% - 11.21%', '11.21% - 13.15%', '13.15% - 17.63%', '17.63% - 23.70%', '23.70% - 33.79%']


def app4(prev_vars):  # Admin page
    if type(prev_vars) is int:  # Checks if the user saved the variables previously
        st.write("Ooops... You forgot to generate portfolio...")
        start_index = prev_vars
        save([start_index], "placeholder", ["App1"])
    else:
        try:  # Checks if the user saved the last variable on the second page
            print('Admin Page', prev_vars)

            st.write("Name")
            st.info(prev_vars[0])
            st.write("Age (Years)")
            st.info(prev_vars[1])
            st.write("Investment Amount (in Rupees)")
            st.info(prev_vars[2])
            st.write("Duration of Investment (Years)")
            st.info(prev_vars[3])
            st.write("Investing For?")
            st.info(prev_vars[4])
            st.write("How much you anticipate needing a portion of your invested funds before completion of "
                     "the duration of your investment?")
            st.info(prev_vars[5])
            st.write("How familiar are you with investment matters?")
            st.info(prev_vars[6])
            st.write("How secure is your current and future income from sources such as salary, pensions or other "
                     "investments?")
            st.info(prev_vars[7])
            st.write("What is the proportion the amount you are investing respect of your total investment assets?")
            st.info(prev_vars[8])
            st.write("Risk Score")
            st.success(str(prev_vars[9]) + " / 70")
            st.write("Profile Nature")
            st.info(str(prev_vars[10]))
            st.write("Expected Returns (% p.a.)")
            st.info(str(expReturnsRange[prev_vars[12]]))
            st.write("Volatility (%)")
            st.info(str(volatilityRange[prev_vars[12]]))
            st.write("Daily Loss 5% confidence level")
            st.info(str(maxDailyRange[prev_vars[12]]))
            st.write("Drawdown")
            st.info(str(maxDrawRange[prev_vars[12]]))

        except Exception as e:
            print(2, e)
            st.write("Ooops... ")
            #####
