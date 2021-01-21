#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script calculated the 24 hour and 48 hour percentage survival of the
virus in water. It uses the temperature model described in section 2.5 and
equations 6 and 7. Results are presented in figure 1c and table 1.
"""

#import numpy as np;
import pandas as pd;
import numpy as np;
from os import path;


df = pd.read_csv("output/viral_counts.csv");
temperatures = df["laketemp_med"];
r = 10**(0.05*temperatures - 1.32);
survival24 = 10**(-r*1.0); #Proportion surviving after 24 hours
survival48 = 10**(-r*2.0); #Proportion surviving after 48 hours


#load country codes
output = pd.DataFrame(df.iloc[:,0].copy());
output["laketemp_med"] = df["laketemp_med"];
output["24h_survival_proportion"] = survival24;
output["48h_survival_proportion"] = survival48;


for column in ["viral_copies_vlowIU_lowDF",
               "viral_copies_vlowIU_medDF",
               "viral_copies_vlowIU_highDF",
               "viral_copies_lowIU_lowDF",
               "viral_copies_lowIU_medDF",
               "viral_copies_lowIU_highDF",
               "viral_copies_medIU_lowDF",
               "viral_copies_medIU_medDF",
               "viral_copies_medIU_highDF",
               "viral_copies_highIU_lowDF",
               "viral_copies_highIU_medDF",
               "viral_copies_highIU_highDF",
               ]:
    vals = df[column];
    
    vals24 = vals*survival24;
    vals48 = vals*survival48;
    
    output["0h_"+column] = vals;
    output["24h_"+column] = vals24;
    output["48h_"+column] = vals48;
               

output.to_csv("output/viral_counts_survival.csv", sep=",", index=False);

