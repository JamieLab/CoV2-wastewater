# Transmission risk and temperature driven survival of SARS-CoV-2 from and within faecally contaminated water

This repository contains tools for calculating the relative transmission risk, temperature related virus survival and expected number of infectious virus copies in waste water for SARS CoV-2. The approach is described within a published (and extensively peer-reviewed!) journal paper (Shutler et al., 2021). An earlier version of the work was also published as pre-print, but the fully open access paper, Shutler et al (2021) linked below, should be referenced when viewing and using the software tools listed here.

Shutler JD, Zaraska K, Holding T, Machnik M, Uppuluri K, Ashton IGC, Migdał Ł, Dahiya RS (2021). Rapid Assessment of SARS-CoV-2 Transmission Risk for Fecally Contaminated River Water. ACS ES&T Water, https://pubs.acs.org/doi/10.1021/acsestwater.0c00246


## File descriptions

calc_relative_risk.py - calculates the relative risk of CoV-2 transmission from waste water spills for different countries.

calc_copies_per_L.py - estimates the number of copies of infectious SARS CoV-2 expected in waste water and waste water spills for different countries.

calc_copies_survival.py - example 24 and 48 hour virus (temperature dependent) survival calculation for different countries.

waste_water_spill_pathogens.xlsx - an Excel spreadsheet implementation of the calc_copies_per_L.py script. This is intended to be easily accessible and allow testing / further exploration of the parameters. This also includes calculations for the 24 and 48 hours virus survival in water (i.e. a reimplementation of calc_copies_survival.py). The file contains three sheets providing example calculations for low (0.1%), medium (1%) and high (10%) viable:non-viable virus ratios.
