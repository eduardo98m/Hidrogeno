# Introduction

Hidrogen production via electrolys has the potential to contributte greatly to the electric grid balance. Combined with renewvable, variable energy sources like solar and wind power, hydrogen has a enourmus potential to contributte to the transition to green energy.


# Objective

* The main objective of this project is to develop a tool that helps with the selection of electrolysers based on it's economic potential.

# Methodology
In order to determine the electrolyser viability, we will calculate the electrolyser
net present value (NPV) given by the following formula:

$$
\text{NPV} = - \text{CAPEX} + \sum_{i=1}^{n} \frac{R_t}{(1+d_r)^i} 
$$

* $R_t$: Net cashflow
* $\text{CAPEX}$: The capital cost of the electrolyser.
* $d_r$: Discount rate.
* $n$: Number of years the electrolyser is expected to be used.

## CAPEX: Capital costs
The capital cost of the electrolyser are determined from [cite]
, according to the selected electrolyser type and as a function of the electrolyser energy input.

## Net Cashflow ($R_t$)

In a year of operation the cashflow of the electrolyser is given by the ammount 
of hidrogen produced times its expected market price minus the cost of the 
electricity used to power the electrolyser, the costs of water and the operating
expenses of the system.

$$
R_t =  m_{H_2} p_{H_2} - E_{year}\cdot C_{\text{energy}} - V_{\text{water}} \cdot p_{\text{water}} - \text{OPEX}
$$

The total energy used in a year to power the electrolyser can be calculated 
using the daily rate of use of the electrolyser, this is the percentage of the 
day that the electrolyser is used,(for example the time of the day there is a surpluss of energy):

$$
E_{year} = P_o \cdot r \cdot 24 \left[\frac{\text{h}}{\text{day}} \right] \cdot 365 \left[\frac{\text{day}}{\text{year}} \right]
$$

* $P_o$: The power input of the electrolyser.
* $r$: The rate of use of the electrolyser.

### Anual Hydrogen Production ($m_{H_2}$)
The total mass of hidrogen produced in a year is also calculated in function of
the energy intput:

$$
m_{H_2} = \frac{ E_{year}}{\eta_{H_2}}
$$ 

* $\eta_{H_2}$: Efficiency of the electrolyser system, it is the ratio between the energy input of the electrolyser and the mass of hidrogen produced, given in $\left[\frac{\text{kWh}}{\text{Kg}}\right]$

The efficiency of the electrolyser system is determined from[cite]

### Anual Water consumption ($V_{\text{water}}$)
From stoichiometry we can also calculate the volume of water required for the 
electrolysis process, 9 kg of water are required for each kg of hydrogen 
produced:

$$
V_{\text{water}} = \frac{m_{H_2}9}{\rho_{H_2O}} = \frac{ E_{year}}{\eta_{H_2}} \frac{9}{\rho_{H_2O}}
$$

The water consumption is calculated in cubic meters.

### OPEX: Operating expenses

The operating expenses are calculated as a fraction of the Capital expenditures,
we use an estimate from [cite] between 5% and 2% of the CAPEX:
$$
\text{OPEX} = k_{\%} \cdot \text{CAPEX} 
$$


Thus we end with the following formula:

$$
R_t =  \frac{ E_{year}}{\eta_{H_2}} p_{H_2} - E_{year}\cdot C_{\text{energy}} -\frac{ E_{year}}{\eta_{H_2}} \frac{9}{\rho_{H_2O}} \cdot p_{\text{water}} - \text{OPEX}
$$

$$
R_t = P_o \cdot r \cdot 24  \cdot 365  \cdot \left( \frac{1}{\eta_{H_2}} \left( p_{H_2} - \frac{9}{\rho_{H_2O}} \cdot p_{\text{water}}  \right) -  C_{\text{energy}} \right) - \text{OPEX}
$$


## Lifetime ($n$)

The lifetime of the electrolyser is determined based on the data from the IRENA
report[cite], this is given in lifecicle hours, so it must be converted to years,
using the user given daily rate of use:

$$
n = \frac{\text{lifetime}_{\text{hours}}}{(364 \cdot 24)(r)}
$$

## Return on Investment ($\text{ROI}$)

The return on investment is calculated using the value obtained from the NPV:

$$
\text{ROI} = \frac{\text{NPV}-\text{CAPEX}}{\text{\text{CAPEX}}} 
$$

## Other variables

Apart from the economic potential of the system, we also need to know other 
variables, such as water consumption (flow rate), hydrogen flow rate, these are
given by the following formulas:

$$
Q_{\text{water}} = P_o \frac{9}{\eta_{H_2} \rho_{H_2O}}
$$

$$
Q_{H_2} = P_o \frac{1}{\eta_{H_2} \rho_{H_2}}
$$

Note: The density of the hidrogen is at standard conditions.







