#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script calculates the relative risk (Hc*, equation 1) and
normalised relative risk metrics (Hc, equation 2, figure 1a and 1b)
"""


#import numpy as np;
import pandas as pd;
import numpy as np;


inputDir = "input_data/";
outputDir = "output/";

#load country codes
output = pd.read_csv(inputDir+"countries.txt", sep=" ", header=None, names=["country"]);


#calculte domestic water usage per capita
domWater = pd.read_csv(inputDir+"/dom_waterusage.txt", sep=" ", header=None);
domWater = domWater.values[:,0]; #m^3 / yr / person
domWater = domWater / (365.25) * 1000; #L / day / person
output["domesticWaterUse"] = domWater


#number of viral particles per litre of raw sewage
dailyPerCapitaShedding = 1.0; #Always 1.0 for relative hazard
relativeConcentrationInWasteWater = dailyPerCapitaShedding/domWater; #copies / L waste water
output["relativeConcentrationInWasteWater"] = relativeConcentrationInWasteWater;


#dilution factors from Keller 2014. This is water flux / waste water flux
dilutionFactorDf = pd.read_csv(inputDir+"dilution.txt", sep=" ", header=None);
dilutionFactorLow = dilutionFactorDf.values[:,1];
dilutionFactorLow = 10**dilutionFactorLow; #Assuming the input data was log10(dilution)
dilutionFactor = dilutionFactorDf.values[:,2];
dilutionFactor = 10**dilutionFactor; #Assuming the input data was log10(dilution)
dilutionFactorHigh = dilutionFactorDf.values[:,3];
dilutionFactorHigh = 10**dilutionFactorHigh; #Assuming the input data was log10(dilution)
output["dilutionFactor_low"] = dilutionFactorLow;
output["dilutionFactor_med"] = dilutionFactor;
output["dilutionFactor_high"] = dilutionFactorHigh;


#Riverine concentration
pecRiverLow = relativeConcentrationInWasteWater / dilutionFactorLow;
output["pecRiver_notnomalised_low"] = pecRiverLow;
pecRiverMed = relativeConcentrationInWasteWater / dilutionFactor;
output["pecRiver_notnomalised_med"] = pecRiverMed;
pecRiverHigh = relativeConcentrationInWasteWater / dilutionFactorHigh;
output["pecRiver_notnomalised_high"] = pecRiverHigh;

#combined all values to calculate min and max and normalise by same constant
#allPecVals = np.array([pecRiverLow, pecRiverMed, pecRiverHigh]);
#normalisingConstant = np.nanmax(allPecVals) - np.nanmin(allPecVals);
normalisingConstant = np.nanmax(pecRiverMed) - np.nanmin(pecRiverMed);
output["pecRiver_low"] = pecRiverLow / normalisingConstant;
output["pecRiver_med"] = pecRiverMed / normalisingConstant;
output["pecRiver_high"] = pecRiverHigh / normalisingConstant;


output.to_csv("output/relative_risk.csv", sep=",", index=False);

