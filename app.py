import streamlit as st
import streamlit.components.v1 as components
import numpy as np

# Internal imports 
from explanation import display_paper
from electrolyser_selector import display_selector


# We set the webpage configuration
st.set_page_config(
    page_title="Electrolyser Selector",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/eduardo98m",
        'About': "www.usb.ve"
    }
)
# Hide streamlit logo
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



# We list the pages that our apliccation is going to contatin
pages = ["⚡ Electrolyser Selector",
         "🧮 Algorithms",
         "📚 Bibliography",
         ]

# The pages are set in the aplication sidebar, so the user can
# jump betweent them using a radio button in the sidebar
st.session_state.current_page = st.sidebar.radio(
    "",
    pages)

# We set the initial page to "⚡ Electrolyser Selector"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "⚡ Electrolyser Selector",

# This component is used to make that every time the users changes pages the 
# scrollbar goes to the top
components.html(
    f"""
        <p>{st.session_state.current_page }</p>
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0
)


st.title(st.session_state.current_page)


if st.session_state.current_page == "⚡ Electrolyser Selector":
    display_selector()

elif st.session_state.current_page ==  "🧮 Algorithms":
    display_paper()




        
    

    


                                


    