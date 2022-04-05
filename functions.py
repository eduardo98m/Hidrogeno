from scipy import interpolate
import numpy as np
import json

# We load the parameters of the electrolysers
# Data from IRENA:Green hydrogen cost reduction
with open('electrolyser_params.json') as json_file:
    params = json.load(json_file)

def hydrogen_price(t) -> float:
    """
    Calculates the price of the hydoguen

    Arguments:
    ---------
    t: float -> Time in years from the initial investment

    Returns:
    -------
    float -> Price of the hydoguen at time t.
    
    Implementation: [TODO]
    """

    return None

def electrolyser_params(elec_type, E_o) -> dict:
    """
    Calculates the parameters of the electrolyser

    Arguments:
    ---------
    elec_type: str -> Electrolyser type

    E_o: float -> Operating energy of the electrolyser (kW)
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
    OPEX_frac_fun = interpolate.interpolate1d(
    [1000, 5000, 20000], [0.04, 0.03, 0.02], ) 
    Opex_frac = OPEX_frac_fun(E_o)
    
    OPEX_o = Opex_frac * CAPEX_o # [USD/year]
    OPEX_sys = Opex_frac * CAPEX_sys # [USD/year]

    lifetime = np.random.uniform(params[elec_type]["lifetime"]["min"],
                                params[elec_type]["lifetime"]["max"])
    
    return {"efficiency": efficiency,
            "CAPEX_o": CAPEX_o,
            "CAPEX_sys": CAPEX_sys,
            "OPEX_o": OPEX_o,
            "OPEX_sys": OPEX_sys,
            "lifetime": lifetime}


def cash_flow(t:float, 
                E_year:float, 
                E_cost:float, 
                efficiency:float, 
                OPEX:float, 
                hydrogen_price:callable) -> float:
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
    H2_price = hydrogen_price(t) # [USD/kg]

    yearly_income = E_year * (H2_price/efficiency - E_cost) - OPEX # [USD] 
    
    return yearly_income

    

def total_return(lifetime, OPEX, CAPEX, discount_rate)->float:
    """
    Calculates the total return of the electrolyser

    Arguments:
    ---------
    lifetime: int -> Lifetime of the electrolyser in years
    
    """
    cumulative_return = []
    yearly_return = []
    for year in range(lifetime):
        E_year = E_o * surpluss_time_fraction * 365 * 24 # [kWh]
        yearly_income = cash_flow(year, E_year, E_cost, efficiency, OPEX)\
                        /(1+discount_rate)**year
        total_income += yearly_income
        yearly_return.append(yearly_income)
        cumulative_return.append(total_income)

    return

