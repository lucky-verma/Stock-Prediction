import streamlit as st
from pages.multipage import MultiPage, start_app
from pages.profile import app1
from pages.portfolio import app2
from pages.management import app3
from pages.admin import app4

st.set_page_config(
    page_title="QUNIQ",
    # page_icon="whatbox_LIFT_UP_white.png",
    layout="wide",
    initial_sidebar_state="expanded", )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

######

#  Multi Page setup

######

start_app()  # Clears the cache when the app is started

app = MultiPage()
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next"
app.previous_page_button = "Previous"


def startpage():
    # st.markdown("""# quniq """)
    l, centre, r = st.beta_columns((1.5, 2, 1))
    with l:
        st.image('data/quniq.png')


######

# Pages

######

def appOne(prev_vars):
    app1(prev_vars)


def appTwo(prev_vars):
    app2(prev_vars)


def appThree(prev_vars):
    app3(prev_vars)


def appFour(prev_vars):
    app4(prev_vars)


######

app.set_initial_page(startpage)
app.add_app("User Profile", appOne)  # Adds first page (app1) to the framework
app.add_app("Generated Portfolio", appTwo)  # Adds second page (app2) to the framework
app.add_app("Portfolio Management", appThree)  # Adds third page (app3) to the framework
app.add_app("Admin Panel", appFour)  # Adds third page (app3) to the framework
app.run()  # Runs the multipage app!
