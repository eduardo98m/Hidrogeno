from calendar import c
from scipy import interpolate
import numpy as np
import json
from typing import *

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
    CAPEX_o = E_o *np.random.uniform(
                                    params[elec_type]["stack cost"]["min"], 
                                    params[elec_type]["stack cost"]["max"]
                                    )# [USD]
    
    # Capital cost of the electrolyser system
    CAPEX_sys = E_o *np.random.uniform(
                                params[elec_type]["full system cost"]["min"], 
                                params[elec_type]["full system cost"]["max"]
                                ) # [USD]
    # Now we calculate the operating cost of the electrolyser
    # As a fraction of the CAPEX based on the operating energy
    # Source (https://www.fch.europa.eu/sites/default/files/FCH%20Docs/171121_FCH2JU_Application-Package_WG5_P2H_Green%20hydrogen%20%28ID%202910583%29%20%28ID%202911641%29.pdf)
    OPEX_frac_fun = interpolate.interp1d(
    [1000, 5000, 20000], [0.04, 0.03, 0.02], ) 
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


def cash_flow(t:float, 
                E_year:float, 
                E_cost:float, 
                efficiency:float, 
                OPEX:float, 
                H2_price:float) -> float:
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

    yearly_income = E_year * (H2_price/efficiency - E_cost) - OPEX # [USD] 
    
    return yearly_income

    

def total_return(lifetime_years:int, 
                 E_o: float, 
                 rate_of_use:float,
                 efficiency:float, 
                 OPEX:float, 
                 discount_rate:float,
                 E_cost:Callable,
                 hydrogen_price:Callable
                 )->float:
    """
    Calculates the total return of the electrolyser

    Arguments:
    ---------
    lifetime_years: int -> Lifetime of the electrolyser in years
    
    """
    cumulative_return = np.zeros(lifetime_years +1)
    yearly_return = np.zeros(lifetime_years +1)
    life_span = np.arange(2022, 2022 + lifetime_years + 1, 1)

    total_income = 0
    
    for i, year in enumerate(life_span):
        E_year = E_o * rate_of_use * 365 * 24 # [kWh]

        yearly_income = cash_flow(year, E_year, E_cost(year), efficiency, OPEX, hydrogen_price(year))/(1+discount_rate)**(i+1)
        
        total_income += yearly_income
        
        yearly_return[i] = yearly_income
        
        cumulative_return[i] = total_income

    return cumulative_return, yearly_return, life_span




def calculate_profitability(
    E_o:float,
    electrolyser_type: str,
    rate_of_use:float,
    discount_rate:float,
    E_cost: Callable,
    hydrogen_price:Callable
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
                                                hydrogen_price
                                                )
    
    # Step 3: Calculate other parameters of the elecrolyser
    cumulative_return = cumulative_return - params['CAPEX_sys']
                                                    
    return cumulative_return, yearly_return, life_span

