    
import streamlit as st
# Other imports
import numpy as np
from scipy import interpolate
import plotly.graph_objects as go
from functions import calculate_profitability_V2, calculate_profitability_V3,\
                     triangular_dist_density
import json
import plotly.express as px

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
    # Disscount rate
    disscount_rate = col2.number_input("Disscount rate [%]",
                                value = 5.25, 
                                min_value=0.00,step = 0.01, max_value = 15.00,
                                format="%0.2f") * 0.01
    
    # Efficiency reduction rate.
    eff_reduction_rate = col2.number_input("Efficiency decreasse rate [%/ten thousand hours]",
                                value = 1.25, 
                                min_value=0.00,step = 0.00, max_value = 100.00,
                                format="%0.2f") * 0.01

    montecarlo_iters = col1.number_input("Montecarlo iterations",
                                value = 1000,   
                                min_value=1,
                                max_value=10000,
                                step = 1,
                                format="%d")
        

    # Now we make several containers for energy production cost, hydorgen price
    # and water price.
    years = [2022, 2025, 2030, 2040, 2050, 2060]
    projected_energy_cost = [0.05, 0.04, 0.03, 0.03, 0.03, 0.03]
    with st.expander("Energy production costs"):
        
        col_a, col_b = st.columns([1, 3])
        energy_production_costs = np.zeros(len(years))
        interpolation_type = col_a.selectbox("Interpolation for the energy \
                                                production costs",
                                                ["linear","nearest"])
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
                                                ["linear","nearest"])
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
                                                ["linear","nearest"])
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
    
    

    st.subheader("Electrolyser Parameters")

    # Efficiency of the electrolyser

    cont_eff =  st.container()

    col_a, col_b, col_c= cont_eff.columns([1, 2, 1])

    col_a.subheader("Efficiency of the electrolyser")

    electrolyser_efficiency_mode = col_a.slider("Efficiency mode [kW/KgH2]",
            min_value = IRENA_data[electrolyser_type]["efficiency"]["min"],
            max_value = IRENA_data[electrolyser_type]["efficiency"]["max"],
            value = (IRENA_data[electrolyser_type]["efficiency"]["min"] + \
                IRENA_data[electrolyser_type]["efficiency"]["max"])/2,
            step=0.01)

    electrolyser_efficiency_left = col_a.slider("Efficiency min [kW/KgH2]",
            min_value = IRENA_data[electrolyser_type]["efficiency"]["min"],
            max_value = IRENA_data[electrolyser_type]["efficiency"]["max"],
            value = IRENA_data[electrolyser_type]["efficiency"]["min"],
            step=0.01)
    
    electrolyser_efficiency_right = col_a.slider("Efficiency max [kW/KgH2]",
            min_value=IRENA_data[electrolyser_type]["efficiency"]["min"],
            max_value=IRENA_data[electrolyser_type]["efficiency"]["max"],
            value=IRENA_data[electrolyser_type]["efficiency"]["max"],
            step=0.01)
    
    x_efficiency = np.linspace(electrolyser_efficiency_left,
                                electrolyser_efficiency_right,
                                num=100)
    
    y_efficiency = triangular_dist_density(x_efficiency, 
                                            electrolyser_efficiency_left, 
                                            electrolyser_efficiency_right,
                                            electrolyser_efficiency_mode)
    
    chart = go.Figure()

    chart.add_trace(go.Scatter(x=x_efficiency, y=y_efficiency, fill = 'tozeroy',
                    mode='lines', name='interpolation'))
    
    chart.update_layout(title='Efficiency Distribution',
                xaxis_title='Efficiency [kW/KgH2]',
                yaxis_title='Probability')
    
    col_b.plotly_chart(chart, use_container_width=True)

    #--------------------------------------------------------------------------#

    cont_lifetime =  st.container()

    col_a, col_b, _= cont_lifetime.columns([1, 2, 1])
    
    col_a.subheader("Lifetime of the electrolyser")

    # Electrolyser lifetime
    electrolyser_lifetime_mode = col_a.slider("Lifetime mode [years]",
            min_value = IRENA_data[electrolyser_type]["lifetime"]["min"],
            max_value = IRENA_data[electrolyser_type]["lifetime"]["max"],
            value = (IRENA_data[electrolyser_type]["lifetime"]["min"] + \
                IRENA_data[electrolyser_type]["lifetime"]["max"])/2,
            step=0.01)
    
    electrolyser_lifetime_left = col_a.slider("Lifetime min [years]",
            min_value = IRENA_data[electrolyser_type]["lifetime"]["min"],
            max_value = IRENA_data[electrolyser_type]["lifetime"]["max"],
            value = IRENA_data[electrolyser_type]["lifetime"]["min"],
            step=0.01)
    
    electrolyser_lifetime_right = col_a.slider("Lifetime max [years]",
            min_value=IRENA_data[electrolyser_type]["lifetime"]["min"],
            max_value=IRENA_data[electrolyser_type]["lifetime"]["max"],
            value=IRENA_data[electrolyser_type]["lifetime"]["max"],
            step=0.01)
    
    x_lifetime = np.linspace(electrolyser_lifetime_left,
                                electrolyser_lifetime_right,
                                num=100)

    y_lifetime = triangular_dist_density(x_lifetime,
                                            electrolyser_lifetime_left,
                                            electrolyser_lifetime_right,
                                            electrolyser_lifetime_mode)
    
    chart = go.Figure()

    chart.add_trace(go.Scatter(x=x_lifetime, y=y_lifetime, fill = 'tozeroy',
                    mode='lines', name='interpolation'))
    
    chart.update_layout(title='Lifetime Distribution',
                    xaxis_title='Lifetime [thousand of hours]',
                yaxis_title='Probability')
    
    col_b.plotly_chart(chart, use_container_width=True)

    #--------------------------------------------------------------------------#

    cont_cost =  st.container()

    col_a, col_b, _= cont_cost.columns([1, 2, 1])

    col_a.subheader("Capital Cost of the electrolyser")

    # Electrolyser capital cost

    electrolyser_capital_cost_mode = col_a.slider("Capital Cost mode [USD/kW]",
            min_value = IRENA_data[electrolyser_type]["full system cost"]["min"],
            max_value = IRENA_data[electrolyser_type]["full system cost"]["max"],
            value = (IRENA_data[electrolyser_type]["full system cost"]["min"] + \
                IRENA_data[electrolyser_type]["full system cost"]["max"])/2,
            step=0.01)* power_output
    
    electrolyser_capital_cost_left = col_a.slider("Capital Cost min [USD/kW]",
            min_value = IRENA_data[electrolyser_type]["full system cost"]["min"],
            max_value = IRENA_data[electrolyser_type]["full system cost"]["max"],
            value = IRENA_data[electrolyser_type]["full system cost"]["min"],
            step=0.01)* power_output
    
    electrolyser_capital_cost_right = col_a.slider("Capital Cost max [USD/kW]",
            min_value=IRENA_data[electrolyser_type]["full system cost"]["min"],
            max_value=IRENA_data[electrolyser_type]["full system cost"]["max"],
            value=IRENA_data[electrolyser_type]["full system cost"]["max"],
            step=0.01)* power_output
    
    x_capital_cost = np.linspace(electrolyser_capital_cost_left,
                                electrolyser_capital_cost_right,
                                num=100)
    
    y_capital_cost = triangular_dist_density(x_capital_cost,
                                            electrolyser_capital_cost_left, 
                                            electrolyser_capital_cost_right,
                                            electrolyser_capital_cost_mode)
    
    chart = go.Figure()

    chart.add_trace(go.Scatter(x=x_capital_cost, y=y_capital_cost, 
                    fill = 'tozeroy', mode='lines', name='interpolation'))
    
    chart.update_layout(title='Capital Cost Distribution', 
                xaxis_title='Capital Cost [USD/kW]',
                yaxis_title='Probability')
    
    col_b.plotly_chart(chart, use_container_width=True)

       
    #--------------------------------------------------------------------------#
    
    ROI_arr = np.zeros(montecarlo_iters)
    IRR_arr = np.zeros(montecarlo_iters)
    RT_arr = np.zeros(montecarlo_iters)
    H2_COST_arr = np.zeros(montecarlo_iters)

    efficiency_arr = np.zeros(montecarlo_iters)
    CAPEX_arr = np.zeros(montecarlo_iters)
    lifetime_years_arr = np.zeros(montecarlo_iters)
    for i in range(montecarlo_iters):
        efficiency = np.random.triangular(electrolyser_efficiency_left, 
                                          electrolyser_efficiency_mode,
                                          electrolyser_efficiency_right
                                          )
        lifetime = np.random.triangular(electrolyser_lifetime_left,
                                        electrolyser_lifetime_mode,
                                        electrolyser_lifetime_right)
        
        capital_cost = np.random.triangular(electrolyser_capital_cost_left,
                                            electrolyser_capital_cost_mode,
                                            electrolyser_capital_cost_right)
        
        # Return on Investment
        # Internal rate of return
        # Return Time 
        # Are calculated
        ROI, IRR, RT, H2_COST = calculate_profitability_V3( 
                                                        efficiency,
                                                        eff_reduction_rate,
                                                        capital_cost,
                                                        lifetime,
                                                        power_output,
                                                        electrolyser_type,
                                                        rate_of_use,
                                                        disscount_rate,
                                                        energy_cost_func,
                                                        hydrogen_price_func,
                                                        water_price_func
                                                        )

        ROI_arr[i]     = ROI
        IRR_arr[i]     = IRR
        RT_arr[i]      = RT
        H2_COST_arr[i] = H2_COST
        
        efficiency_arr[i] = efficiency
        CAPEX_arr[i] = capital_cost
        lifetime_years_arr[i] = int(np.floor(lifetime * 1000 /(rate_of_use * 24 *365)))
    
    #--------------------------------------------------------------------------#

    col_a, col_b = st.columns([1.2,3])
    col_b.subheader("Empirical cumulative distributions")
    ROI_ecdf = px.ecdf(x = ROI_arr)

    ROI_ecdf.update_layout(title='Return on Investment',
                            xaxis_title='ROI [%]',  
                            yaxis_title='Percentile')

    col_b.plotly_chart(ROI_ecdf, use_container_width=True)

    IRR_ecdf = px.ecdf(x = IRR_arr*100)

    IRR_ecdf.update_layout(title='Internal Rate of Return',
                            xaxis_title='IRR [%]',
                            yaxis_title='Percentile')
    col_b.plotly_chart(IRR_ecdf, use_container_width=True)

    H2_COST_ecdf = px.ecdf(x = H2_COST_arr)

    H2_COST_ecdf.update_layout(title='Hydrogen Cost',
                            xaxis_title='Hydrogen Cost [USD/kg]',
                            yaxis_title='Percentile')
    
    col_b.plotly_chart(H2_COST_ecdf, use_container_width=True)

    

    #--------------------------------------------------------------------------#
    ROI_mean = ROI_arr.mean()
    IRR_mean = np.mean(IRR_arr[~np.isnan(IRR_arr)])*100
    H2_COST_mean = H2_COST_arr.mean()
    lifetime_years_mean = lifetime_years_arr.mean()
    efficiency_mean = efficiency_arr.mean()
    CAPEX_mean = CAPEX_arr.mean()
    
    total_return = ROI_mean/100 * CAPEX_mean
    water_flow_rate  = power_output*9/(efficiency_mean * 997) 
    hydrogen_flow_rate = power_output/(efficiency_mean * 0.08375) 
    hydrogen_mass_rate = power_output/efficiency_mean*24*rate_of_use
    
    # Display the results
    col_a.subheader("Results for the average case")
    col_a.text("Capital costs: {0:.2f}M $".format(electrolyser_capital_cost_mode*10**(-6)))
    col_a.text("Net present value: {0:.2f}M $".format(total_return*10**(-6)))
    col_a.text("Return On Invesment:  {0:.2f} % ".format(ROI_mean))
    col_a.text("Water flow rate: {0:.2f} [m3/s]".format(water_flow_rate))
    col_a.text("Hydrogen flow rate: {0:.2f} [m3/s]".format(hydrogen_flow_rate))
    col_a.text("Daily Hydrogen production: {0:.2f} [kg/24h]".format(hydrogen_mass_rate))
    col_a.text("Internal Rate of Return : {0:.2f} % ".format(IRR_mean))
    col_a.text("Hydrogen cost: {0:.2f} [USD/kg]".format(H2_COST_mean))
    col_a.text("Lifetime: {} years".format(lifetime_years_mean))
    col_a.text("Payback Year : {} ".format(np.median(RT_arr)))
    col_a.write("Payback Time :  {:.2f} years ".format(np.median(RT_arr) -2022) )

    
    



