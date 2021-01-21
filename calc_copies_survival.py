#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:42:11 2020

@author: verwirrt
"""

#import numpy as np;
import pandas as pd;
import numpy as np;
from os import path;


indivDataPath = "../individual_data_files/";


df = pd.read_csv("output/viral_counts.csv");
temperatures = df["laketemp_med"];
temperatures_low = df["laketemp_low"];
temperatures_high = df["laketemp_high"];

r = 10**(0.05*temperatures - 1.32);
survival24 = 10**(-r*1.0); #Proportion surviving after 24 hours using med temperature
survival48 = 10**(-r*2.0); #Proportion surviving after 48 hours using med temperature
rlow = 10**(0.05*temperatures_low - 1.32);
survival24low = 10**(-rlow*1.0); #Proportion surviving after 24 hours using low temperature
survival48low = 10**(-rlow*2.0); #Proportion surviving after 48 hours using low temperature
rhigh = 10**(0.05*temperatures_high - 1.32);
survival24high = 10**(-rhigh*1.0); #Proportion surviving after 24 hours using high temperature
survival48high = 10**(-rhigh*2.0); #Proportion surviving after 48 hours using high temperature


#load country codes
output = pd.DataFrame(df.iloc[:,0].copy());
output["laketemp_lower"] = df["laketemp_low"];
output["laketemp_med"] = df["laketemp_med"];
output["laketemp_upper"] = df["laketemp_high"];
output["24h_survival_proportion_lower"] = survival24low;
output["24h_survival_proportion"] = survival24;
output["24h_survival_proportion_upper"] = survival24high;
output["48h_survival_proportion_lower"] = survival48low;
output["48h_survival_proportion"] = survival48;
output["48h_survival_proportion_upper"] = survival48high;


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
    vals24_Tlow = vals*survival24low;
    vals24_Thigh = vals*survival24high;
    
    vals48 = vals*survival48;
    vals48_Tlow = vals*survival48low;
    vals48_Thigh = vals*survival48high;
    
    output["0h_"+column] = vals;
    
    output["24h_"+column+" lowT"] = vals24_Tlow;
    output["24h_"+column+" medT"] = vals24;
    output["24h_"+column+" highT"] = vals24_Thigh;
    output["48h_"+column+" lowT"] = vals48_Tlow;
    output["48h_"+column+" medT"] = vals48;
    output["48h_"+column+" highT"] = vals48_Thigh;


output.to_csv("output/viral_counts_survival.csv", sep=",", index=False);

