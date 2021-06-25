import streamlit as st
from .multipage import save, clear_cache

# lookup list
expReturnsRange = ['0', '2.40% - 6.19%', '6.19%	- 10.07%', '10.07% - 14.03%', '14.03% - 18.07%', '18.07% - 21.85%']
RiskProfiles = ['Conservative', 'Moderate', 'Balanced', 'Assertive', 'Aggressive']
volatilityRange = ['0', '3.35% - 4.34%', '4.34% - 6.30%', '6.30% - 8.72%', '8.72% - 11.36%', '11.36% - 16.81%']
maxDailyRange = ['0', '1.59% - 1.86%', '1.86% - 2.13%', '2.13% - 2.73%', '2.73 - 3.64%', '3.64% - 5.60%']
maxDrawRange = ['0', '9.78% - 11.21%', '11.21% - 13.15%', '13.15% - 17.63%', '17.63% - 23.70%', '23.70% - 33.79%']


def app3(prev_vars):  # Management page
    if type(prev_vars) is int:  # Checks if the user saved the variables previously
        st.write("Ooops... You forgot to generate portfolio...")
        start_index = prev_vars
        save([start_index], "placeholder", ["App1"])
    else:
        try:  # Checks if the user saved the last variable on the second page
            start_index, var1, var2, var3 = prev_vars
            if st.button("Click here to erase the last variable"):
                clear_cache(["last_var"])  # Erases the variables saved under the name "last_var"

            if st.button("Click here to multiply the variables"):
                st.write(var1 * var2 * var3)
            save([start_index], "placeholder", ["App1"])
        except:
            st.write("Ooops...")
            start_index = prev_vars[0]
            save([start_index], "placeholder", ["App1"])
