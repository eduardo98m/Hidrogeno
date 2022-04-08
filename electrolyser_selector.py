    
import streamlit as st
# Other imports
import numpy as np
from scipy import interpolate
import plotly.graph_objects as go
from functions import calculate_profitability, calculate_profitability_V2
import json

with open('electrolyser_params.json') as json_file:
    IRENA_data = json.load(json_file)

def display_selector():
    col1, col2 = st.columns([3, 3])
    
    # Select the avilable power output
    power_output = col2.number_input("Available power output (MW)",
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
    projected_energy_cost = [0.05, 0.04, 0.03, 0.03, 0.03, 0.03]
    with st.expander("Energy production costs"):
        col_a, col_b = st.columns([1, 3])
        energy_production_costs = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation for the energy production costs",
                                                ["linear","cubic"])
        for i, year in enumerate(years):
            energy_production_costs[i] = col_a.slider("Year {}".format(year),
                                                min_value=0.00,
                                                max_value=1.00,
                                                value=projected_energy_cost[i],
                                                step=0.01)
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
        interpolation_type = col_a.selectbox("Interpolation for hydrogen price",
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
    

    # Do a similar container for water price
    years = [2022, 2025, 2030, 2040, 2050, 2060]
    projected_water_price = [3.85, 3.95, 3.98, 4.00, 4.05, 4.13]
    with st.expander("Water price"):
        col_a, col_b = st.columns([1, 3])
        water_prices = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation for water price",
                                                ["linear","cubic"])
        for i, year in enumerate(years):
            water_prices[i] = col_a.slider("Water price in  \
                                            {}".format(year),
                                            min_value=0.0,
                                            max_value=18.0,
                                            value = projected_water_price[i],
                                            step=0.1,
                                            )
        
        water_price_func = interpolate.interp1d(years, water_prices, 
                                            kind=interpolation_type,
                                            fill_value="extrapolate")
        
        years_plot = np.arange(2022, 2061, 1)
        
        water_prices_plot= water_price_func(years_plot)

        chart = go.Figure()
        
        chart.add_trace(go.Scatter(x=years_plot, y=water_prices_plot,
                        mode='lines', name='interpolation'))
        
        chart.add_trace(go.Scatter(x=years, y=water_prices,
                    mode='markers', name='control points'))
        
        chart.update_layout(title='Water price',
                   xaxis_title='Years',
                   yaxis_title=r'$USD/m^3$')
        
        col_b.plotly_chart(chart, use_container_width=True)
    
    col_a, col_b , col_c= st.columns([1, 2, 1])


    col_a.subheader("Electrolyser Parameters")

    # Efficiency of the electrolyser
    
    with st.container():

        electrolyser_efficiency = col_a.slider("Efficiency [kW/KgH2]",
                                                min_value=IRENA_data[electrolyser_type]["efficiency"]["min"],
                                                max_value=IRENA_data[electrolyser_type]["efficiency"]["max"],
                                                step=0.01)
        
        electrolyser_life_time = col_a.slider("Life time [thousand of hours]",
                                                min_value=IRENA_data[electrolyser_type]["lifetime"]["min"],
                                                max_value=IRENA_data[electrolyser_type]["lifetime"]["max"],
                                                step=0.01)

        capital_cost_electrolyser = col_a.slider("Capital cost [USD/kW]",
                                                min_value=IRENA_data[electrolyser_type]["full system cost"]["min"] ,     
                                                max_value=IRENA_data[electrolyser_type]["full system cost"]["max"], 
                                                step=0.01) * power_output



    cumulative_return, yearly_return, life_span  =calculate_profitability_V2(
                                                            electrolyser_efficiency,
                                                            capital_cost_electrolyser,
                                                            electrolyser_life_time,
                                                            power_output,
                                                            electrolyser_type,
                                                            rate_of_use,
                                                            disscount_rate,
                                                            energy_cost_func,
                                                            hydrogen_price_func,
                                                            water_price_func
                                                            )
    ROI = (cumulative_return[-1])/capital_cost_electrolyser *100

    water_flow_rate = power_output*9/(electrolyser_efficiency * 997) 
    hydrogen_flow_rate = power_output/(electrolyser_efficiency * 0.08375) 
    hydrogen_mass_rate = power_output/electrolyser_efficiency *24*rate_of_use
    # Display the results
    col_b.header("Results")
    #col_c.container()
    col_b.text("Capital costs: {0:.2f}M $".format(capital_cost_electrolyser*10**(-6)))
    #st.text("Anual operating costs: {}k $".format(int(params["OPEX_sys"]/1000)))
    #st.text("Efficiency: {0:.2f} [kWh/kgH2]".format(params["efficiency"]*100))
    #Life span
    #st.text("Lifetime: {} years".format(params["lifetime years"]))
    # Expected return
    col_b.text("Net present value: {0:.2f}M $".format(cumulative_return[-1]*10**(-6)))
    col_b.text("ROI {0:.2f}% ".format(ROI))
    col_b.text("Water flow rate: {0:.2f} [m3/s]".format(water_flow_rate))
    col_b.text("Hydrogen flow rate: {0:.2f} [m3/s]".format(hydrogen_flow_rate))
    col_b.text("Dayly Hydrogen production: {0:.2f} [kg/24h]".format(hydrogen_mass_rate))
    #st.text("Estimated water flow: {}m3/h".format(params["water flow"]))

    st.subheader("")
    
    chart = go.Figure()
    
    chart.add_trace(go.Scatter(x=life_span, y=yearly_return,
                        mode='lines', name='yearly return'))
    
    chart.add_trace(go.Scatter(x=life_span, y=cumulative_return,
                        mode='lines', name='cumulative return'))
    
    chart.update_layout(title='Profitability',
                   xaxis_title='Years',
                   yaxis_title='USD')
    
    st.plotly_chart(chart, use_container_width=True)

