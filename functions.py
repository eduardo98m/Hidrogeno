from scipy import interpolate
import numpy as np
import json
from typing import *
from scipy.optimize import fsolve, root_scalar, least_squares
import numpy_financial as npf
# We load the parameters of the electrolysers
# Data from IRENA:Green hydrogen cost reduction
with open('electrolyser_params.json') as json_file:
    params = json.load(json_file)


def calculate_lifetime(
    electrolyser_type: str,
    rate_of_use:float,
    )-> tuple:

    # Step 1: Get the electrolyser lifetime from the IRENA data.

    base_lifetime = np.random.uniform(
                                params[electrolyser_type]["lifetime"]["min"], 
                                params[electrolyser_type]["lifetime"]["max"]
                                ) # thousands of hours

    lifetime_hours = base_lifetime * 1000 # hours
    
    # Step 2: Using the rate of use, calculate the lifetime of the electrolyser
    # in years.
    lifetime_years = np.floor(lifetime_hours /(rate_of_use * 24 *365)) # years

    return lifetime_hours, int(lifetime_years)

def electrolyser_params(E_o, elec_type, rate_of_use) -> dict:
    """
    Calculates the parameters of the electrolyser

    Arguments:
    ---------
    elec_type: str -> Electrolyser type

    E_o: float -> Operating energy of the electrolyser (kW)

    Returns:
    -------
    dict -> Electrolyser parameters
    """
    
    # Efficiency of the electrolyser
    efficiency = np.random.uniform(
                                    params[elec_type]["efficiency"]["min"], 
                                    params[elec_type]["efficiency"]["max"]
                                    )# [kWh/KgH2]
    # Capital cost of the electrolyser stack
    CAPEX_o = E_o * np.random.uniform(
                                    params[elec_type]["stack cost"]["min"], 
                                    params[elec_type]["stack cost"]["max"]
                                    )# [USD]
    
    # Capital cost of the electrolyser system
    
    CAPEX_sys = E_o * np.random.uniform(
                                params[elec_type]["full system cost"]["min"], 
                                params[elec_type]["full system cost"]["max"]
                                ) # [USD]
    # Now we calculate the operating cost of the electrolyser
    # As a fraction of the CAPEX based on the operating energy
    # Source (https://www.fch.europa.eu/sites/default/files/FCH%20Docs/171121_FCH2JU_Application-Package_WG5_P2H_Green%20hydrogen%20%28ID%202910583%29%20%28ID%202911641%29.pdf)
    OPEX_frac_fun = interpolate.interp1d(
                                        [1000, 5000, 20000], 
                                        [0.04, 0.03, 0.02], ) 
    Opex_frac = OPEX_frac_fun(E_o)
    
    OPEX_o = Opex_frac * CAPEX_o # [USD/year]
    OPEX_sys = Opex_frac * CAPEX_sys # [USD/year]

    lifetime_hours, lifetime_years = calculate_lifetime(
                                elec_type,
                                rate_of_use
    )
    
    return {"efficiency": efficiency,
            "CAPEX_o": CAPEX_o,
            "CAPEX_sys": CAPEX_sys,
            "OPEX_o": OPEX_o,
            "OPEX_sys": OPEX_sys,
            "lifetime hours": lifetime_hours,
            "lifetime years": lifetime_years}


def cash_flow(  E_year:float, 
                E_cost:float, 
                efficiency:float, 
                OPEX:float, 
                H2_price:float,
                Water_price) -> float:
    """
    Calculates the cashflow of the electrolyser at the time period t

    Arguments:
    ---------
    t: float -> Time in years from the initial investment.

    E_year: float -> Energy produced in one year.

    E_cost: float -> Energy production cost.

    OPEX: float -> Yearly operational cost.

    Returns:
    -------
    float -> Cashflow of the electrolyser at time t. (In USD)
    
    Implementation: [TODO]
    """

    yearly_income = E_year * (H2_price/efficiency - E_cost - 9*Water_price/(997*efficiency)) - OPEX # [USD] 
    
    return yearly_income


def h2_cost(    E_year:float, 
                E_cost:float, 
                efficiency:float, 
                OPEX:float, 
                Water_price) -> float:
    """
    Calculates the hydrogen cost at a given time period

    Arguments:
    ---------
    t: float -> Time in years from the initial investment.

    E_year: float -> Energy produced in one year.

    E_cost: float -> Energy production cost.

    OPEX: float -> Yearly operational cost.

    Returns:
    -------
    float ->  Hydrogen cost. (In USD)
    
    """

    h2_price = (E_year * (E_cost + 9*Water_price/(997*efficiency)) + OPEX )/\
                            (E_year/efficiency)# [USD/Kg]] 
    
    return h2_price

    

def total_return(lifetime_years:int, 
                 E_o: float, 
                 rate_of_use:float,
                 efficiency:float,
                 efficiency_reduction_rate_per_year:float, 
                 OPEX:float, 
                 discount_rate:float,
                 E_cost:Callable,
                 hydrogen_price:Callable,
                 water_price:Callable
                 )->float:
    """
    Calculates the total return of the electrolyser

    Arguments:
    ---------
    lifetime_years: int -> Lifetime of the electrolyser in years
    
    """
    cumulative_return = np.zeros(lifetime_years +2)
    yearly_return = np.zeros(lifetime_years +2)
    life_span = np.arange(2022, 2022 + lifetime_years + 2, 1)

    total_income = 0

    E_year = E_o * rate_of_use * 365 * 24 # [kWh]

    efficiency_i = efficiency
    
    for i, year in enumerate(life_span[1:]):

        yearly_income = cash_flow(E_year, 
                                  E_cost(year), 
                                  efficiency_i, 
                                  OPEX, 
                                  hydrogen_price(year), 
                                  water_price(year))/(1+discount_rate)**(i+1)
        
        total_income += yearly_income
        
        yearly_return[i+1] = yearly_income
        
        cumulative_return[i+1] = total_income

        # Now we account for the efficiency reduction
        efficiency_i += efficiency_i * efficiency_reduction_rate_per_year

    

    return cumulative_return, yearly_return, life_span



def total_return_V2(lifetime_years:int, 
                 E_o: float, 
                 rate_of_use:float,
                 efficiency:float,
                 efficiency_reduction_rate_per_year:float,
                 CAPEX:float, 
                 OPEX:float, 
                 discount_rate:float,
                 E_cost:Callable,
                 hydrogen_price:Callable,
                 water_price:Callable
                 )->float:
    """
    Calculates the total return of the electrolyser

    Arguments:
    ---------
    lifetime_years: int -> Lifetime of the electrolyser in years
    
    """
    
    h2_cost_arr = np.zeros(lifetime_years +2)
    life_span = np.arange(2022, 2022 + lifetime_years + 2, 1)

    total_income = -CAPEX

    E_year = E_o * rate_of_use * 365 * 24 # [kWh]

    cash_flow_arr = np.zeros(lifetime_years +2)
    
    cash_flow_arr[0] = -CAPEX

    return_time = False

    efficiency_i = efficiency

    for i, year in enumerate(life_span[1:]):

        cf =  cash_flow(E_year, 
                        E_cost(year),
                        efficiency_i, OPEX, 
                        hydrogen_price(year), 
                        water_price(year)
                        )
        h2_cost_arr[i+1] = h2_cost(E_year,
                                    E_cost(year),
                                    efficiency_i, OPEX,
                                    water_price(year)
                                    )
        yearly_income =cf/(1+discount_rate)**(i+1)
        
        total_income += yearly_income

        cash_flow_arr[i+1] = cf
        

        if not return_time and total_income > 0:
            return_time = year

        # Now we account for the efficiency reduction
        efficiency_i += efficiency_i * efficiency_reduction_rate_per_year


    IRR = round(npf.irr(cash_flow_arr), 5)
    
    NPV = total_income

    avg_h2_cost = np.mean(h2_cost_arr)

    return IRR, NPV, return_time, avg_h2_cost




def calculate_profitability(
    E_o:float,
    electrolyser_type: str,
    rate_of_use:float,
    discount_rate:float,
    E_cost: Callable,
    hydrogen_price:Callable,
    water_price:Callable
    )-> tuple:
    
    # Step 1: Get the electrolyser parameters
    params = electrolyser_params(E_o, electrolyser_type, rate_of_use)

    # Step 2: Calculate the total return of the electrolyser
    cumulative_return, yearly_return, life_span = total_return(
                                                params['lifetime years'], 
                                                E_o, 
                                                rate_of_use,
                                                params['efficiency'], 
                                                params['OPEX_sys'], 
                                                discount_rate,
                                                E_cost,
                                                hydrogen_price,
                                                water_price
                                                )
    
    # Step 3: Calculate other parameters of the elecrolyser
    cumulative_return = cumulative_return - params['CAPEX_sys']
                                                    
    return cumulative_return, yearly_return, life_span, params

def calculate_profitability_V2(
    efficiency:float,
    efficiency_reduction_rate:float,
    CAPEX_sys:float,
    lifetime:float,
    E_o:float,
    electrolyser_type: str,
    rate_of_use:float,
    discount_rate:float,
    E_cost: Callable,
    hydrogen_price:Callable,
    water_price:Callable
    )-> tuple:
    """
    
    """

    efficiency_reduction_rate_per_year = efficiency_reduction_rate * \
                                         rate_of_use * 365 * 24/10000
    # Step 1: Get the electrolyser parameters
    OPEX_frac_fun = interpolate.interp1d(
                                        [1000, 5000, 20000], 
                                        [0.04, 0.03, 0.02], 
                                        fill_value=(0.04, 0.02)
                                        ) 
    Opex_frac = OPEX_frac_fun(E_o)

    OPEX_sys = Opex_frac * CAPEX_sys

    lifetime_hours = lifetime * 1000 # hours
    
    # Step 2: Using the rate of use, calculate the lifetime of the electrolyser
    # in years.
    lifetime_years = int(np.floor(lifetime_hours /(rate_of_use * 24 *365)))

    # Step 2: Calculate the total return of the electrolyser
    cumulative_return, yearly_return, life_span = total_return(
                                                lifetime_years, 
                                                E_o, 
                                                rate_of_use,
                                                efficiency,
                                                efficiency_reduction_rate_per_year, 
                                                OPEX_sys, 
                                                discount_rate,
                                                E_cost,
                                                hydrogen_price,
                                                water_price
                                                )
    
    # Step 3: Calculate other parameters of the elecrolyser
    cumulative_return = cumulative_return - CAPEX_sys
                                                    
    return cumulative_return, yearly_return, life_span


def calculate_profitability_V3(
    efficiency:float,
    efficiency_reduction_rate:float,
    CAPEX_sys:float,
    lifetime:float,
    E_o:float,
    electrolyser_type: str,
    rate_of_use:float,
    discount_rate:float,
    E_cost: Callable,
    hydrogen_price:Callable,
    water_price:Callable
    )->tuple:
    """
    Calculates the Return on invesment, Internal rate of return, return time,
    and hydrogen cost of production.

    Arguments:
    ----------

    """
    efficiency_reduction_rate_per_year = efficiency_reduction_rate * \
                                         rate_of_use * 365 * 24/10000
    # Step 1: Get the electrolyser parameters
    OPEX_frac_fun = interpolate.interp1d(
                                        [1000, 5000, 20000], 
                                        [0.04, 0.03, 0.02], 
                                        fill_value=(0.04, 0.02),
                                        bounds_error = False
                                        ) 
    Opex_frac = OPEX_frac_fun(E_o)

    OPEX_sys = Opex_frac * CAPEX_sys

    lifetime_hours = lifetime * 1000 # hours
    
    # Step 2: Using the rate of use, calculate the lifetime of the electrolyser
    # in years.
    lifetime_years = int(np.floor(lifetime_hours /(rate_of_use * 24 *365)))

    # Step 2: Calculate the total return of the electrolyser
    IRR, NPV, return_time, avg_h2_cost = total_return_V2(   
                                                        lifetime_years, 
                                                        E_o, 
                                                        rate_of_use,
                                                        efficiency, 
                                                        efficiency_reduction_rate_per_year,
                                                        CAPEX_sys,
                                                        OPEX_sys, 
                                                        discount_rate,
                                                        E_cost,
                                                        hydrogen_price,
                                                        water_price
                                                        )
                                                        
                                                        
    
    ROI = NPV/CAPEX_sys *100
                                                    
    return ROI, IRR, return_time, avg_h2_cost


@np.vectorize
def triangular_dist_density(x, x_min, x_max, x_mode):
    """
    Returns the density of a triangular distribution.

    Arguments:
    ----------
    x: float -> value to evaluate the density
    x_min: float -> minimum value of the distribution
    x_max: float -> maximum value of the distribution
    x_mode: float -> mode of the distribution
    
    Returns:
    --------
    float -> density of the distribution at x
    """
    if x < x_min:
        return 0    # 0% probability
    elif x > x_max:
        return 0   # 0% probability
    elif x_min <= x <= x_mode:
        return 2 * (x - x_min) / ((x_mode - x_min) * (x_max - x_min))
    elif x_mode < x <= x_max:
        return 2 * (x_max - x) / ((x_max - x_min) * (x_max - x_mode))