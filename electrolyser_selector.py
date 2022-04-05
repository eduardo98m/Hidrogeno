    
import streamlit as st
# Other imports
import numpy as np
from scipy import interpolate
import plotly.graph_objects as go
from functions import calculate_profitability


def display_selector():
    col1, col2 = st.columns([3, 3])
    
    # Select the avilable power output
    power_outut = col2.number_input("Available power output (MW)",
                                value = 15.00,
                                min_value=10.00,step = 0.01,
                                format="%0.2f") * 1000 # kW
    
    # Select the electrolyser type
    electrolyser_type = col1.selectbox("Electrolyser type",
                                ["alkaline",
                                "PEM",
                                ])
    # Rate of use (percentage of the day the electrolyser is used at full power)
    rate_of_use = col1.slider("Expected daily rate of use",
                                min_value=0.0,
                                max_value=100.0,
                                value=80.0,
                                step=0.1) * 0.01
    
    disscount_rate = col2.number_input("Disscount rate [%]",
                                value = 5.25, 
                                min_value=0.00,step = 0.00, max_value = 15.00,
                                format="%0.2f") * 0.01

    years = [2022, 2025, 2030, 2040, 2050, 2060]
    projected_energy_cost = [10.4, 10.3, 10.3, 9.9, 9.6, 9.5]
    with st.expander("Energy production costs"):
        col_a, col_b = st.columns([1, 3])
        energy_production_costs = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation type",
                                                ["linear","cubic"])
        for i, year in enumerate(years):
            energy_production_costs[i] = col_a.slider("Year {}".format(year),
                                                min_value=0.0,
                                                max_value=20.0,
                                                value=projected_energy_cost[i],
                                                step=0.1)
        energy_cost_func = interpolate.interp1d(years, energy_production_costs, 
                                            kind=interpolation_type,
                                            fill_value="extrapolate")
        years_plot = np.arange(2022, 2061, 1)
        energy_production_costs_plot= energy_cost_func(years_plot)

        chart = go.Figure()
        chart.add_trace(go.Scatter(x=years_plot, y=energy_production_costs_plot,
                        mode='lines', name='interpolation'))
        chart.add_trace(go.Scatter(x=years, y=energy_production_costs,
                    mode='markers', name='control points'))
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
        interpolation_type = col_a.selectbox("Interpolation type b",
                                                ["linear","cubic"])
        for i, year in enumerate(years):
            hydrogen_prices[i] = col_a.slider("Hydrogen price in  \
                                            {}".format(year),
                                            min_value=0.0,
                                            max_value=18.0,
                                            value = projected_hydrogen_price[i],
                                            step=0.1,
                                            )
        
        hydrogen_price_func = interpolate.interp1d(years, hydrogen_prices, 
                                            kind=interpolation_type,
                                            fill_value="extrapolate")
        
        years_plot = np.arange(2022, 2061, 1)
        
        hydrogen_prices_plot= hydrogen_price_func(years_plot)

        chart = go.Figure()
        
        chart.add_trace(go.Scatter(x=years_plot, y=hydrogen_prices_plot,
                        mode='lines', name='interpolation'))
        
        chart.add_trace(go.Scatter(x=years, y=hydrogen_prices,
                    mode='markers', name='control points'))
        
        chart.update_layout(title='Hydrogen price',
                   xaxis_title='Years',
                   yaxis_title='USD/Kg')
        
        col_b.plotly_chart(chart, use_container_width=True)


    cumulative_return, yearly_return, life_span = calculate_profitability(
                                                        power_outut,
                                                        electrolyser_type,
                                                        rate_of_use,
                                                        disscount_rate,
                                                        energy_cost_func,
                                                        hydrogen_price_func
                                                        )
    
    chart = go.Figure()
    
    chart.add_trace(go.Scatter(x=life_span, y=yearly_return,
                        mode='lines', name='yearly return'))
    
    chart.add_trace(go.Scatter(x=life_span, y=cumulative_return,
                        mode='lines', name='cumulative return'))
    
    chart.update_layout(title='Profitability',
                   xaxis_title='Years',
                   yaxis_title='USD')
    
    st.plotly_chart(chart, use_container_width=True)