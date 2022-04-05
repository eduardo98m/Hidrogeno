import streamlit as st
import streamlit.components.v1 as components
import numpy as np

# Internal imports 
from explanation import display_paper

# Other imports
from scipy import interpolate
import plotly.express as px
import plotly.graph_objects as go

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
    col1, col2 = st.columns(2)

    # Select the hydrogen normalized flow rate
    hg_nf = col1.number_input("Hydrogen normalized flow rate (Nm3/h)", 
                                min_value=0.0, step = 10.,
                                format="%0.1f")
    # Select the avilable power output
    p_av = col1.number_input("Available power output (kW)",
                                min_value=0.0,step = 10.,
                                format="%0.1f")
    
    # Select the electrolyser type
    electrolyser_type = col2.selectbox("Electrolyser type",
                                ["Alkaline",
                                "PEM",
                                ])
    
    # Intermitent use of the electrolyser
    intermitent_use = col2.checkbox("Intermitent use of the electrolyser",
                                value=False)

    years = [2022, 2025, 2030, 2040, 2050, 2060]
    projected_energy_cost = [10.4, 10.3, 10.3, 9.9, 9.6, 9.5]
    with st.expander("Energy production costs"):
        col_a, col_b = st.columns([1, 3])
        energy_production_costs = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation type",["linear","cubic"])
        for i, year in enumerate(years):
            energy_production_costs[i] = col_a.slider("Year {}".format(year),
                                                    min_value=0.0,
                                                    max_value=20.0,
                                                    value=projected_energy_cost[i],
                                                    step=0.1)
        interp_func = interpolate.interp1d(years, energy_production_costs, kind=interpolation_type)
        years_plot = np.arange(2022, 2061, 1)
        energy_production_costs_plot= interp_func(years_plot)

        chart = go.Figure()
        chart.add_trace(go.Scatter(x=years_plot, y=energy_production_costs_plot,
                        mode='lines', name='interpolation'))
        chart.add_trace(go.Scatter(x=years, y=energy_production_costs,
                    mode='markers', name='points'))
        chart.update_layout(title='Energy production costs',
                   xaxis_title='Years',
                   yaxis_title='USD/kWh')
        col_b.plotly_chart(chart, use_container_width=True)

    # Do a similar container for hydrogen price
    years = [2022, 2025, 2030, 2040, 2050, 2060]
    projected_hydrogen_price = [6.8, 6.4, 5.8, 5.4, 5.2, 5.0]
    with st.expander("Hydrogen price"):
        col_a, col_b = st.columns([1, 3])
        hydrogen_prices = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation type b",["linear","cubic"])
        for i, year in enumerate(years):
            hydrogen_prices[i] = col_a.slider("Hydrogen price in  {}".format(year),
                                                    min_value=0.0,
                                                    max_value=18.0,
                                                    value=projected_hydrogen_price[i],
                                                    step=0.1)
        interp_func = interpolate.interp1d(years, hydrogen_prices, kind=interpolation_type)
        years_plot = np.arange(2022, 2061, 1)
        hydrogen_prices_plot= interp_func(years_plot)

        chart = go.Figure()
        chart.add_trace(go.Scatter(x=years_plot, y=hydrogen_prices_plot,
                        mode='lines', name='interpolation'))
        chart.add_trace(go.Scatter(x=years, y=hydrogen_prices,
                    mode='markers', name='points'))
        chart.update_layout(title='Hydrogen price',
                   xaxis_title='Years',
                   yaxis_title='USD/Kg')
        col_b.plotly_chart(chart, use_container_width=True)

elif st.session_state.current_page ==  "🧮 Algorithms":
    display_paper()




        
    

    


                                


    