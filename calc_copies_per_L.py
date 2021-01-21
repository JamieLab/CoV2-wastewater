#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script calculates the number of viable virus copies in natural water
systems resulting from an untreated sewage spill (Cspill, equation 5).
The output is presented in figure 2.

An excel tool is provided in the GitHub repository which performs the same
calculation.
"""

#import numpy as np;
import pandas as pd;
import numpy as np;


inputDir = "input_data/";
outputDir = "output/";

#load country codes
output = pd.read_csv(inputDir+"countries.txt", sep=" ", header=None, names=["country"]);


mu = 5.22; sigma = 1.86; #From Jones et al 2020
mu_e = np.log(10**mu); #convert from log10 to natural log
sigma_e = np.log(10**sigma); #convert from log10 to natural log
viralRnaInExcrement = np.e**( mu_e + 0.5*(sigma_e**2) ); #606752666857
viralRnaInExcrement *= 1000; #copies l^-1
viralRnaInExcrementVariance = np.e**((sigma_e**2)-1) * np.e**(2*mu_e + (sigma_e**2)); #from wikipedia
viralRnaInExcrementSD = np.sqrt(viralRnaInExcrementVariance);
viralRnaInExcrementSD *= 1000; #copies l^-1
viralRnaInExcrementSD=0.0;


#Per capita daily faeces production. Previous ballpark figure from http://helid.digicollection.org/en/d/Jh0210e/3.1.1.html
#Using 'rich' country values from table3 of Rose2015: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4500995/
#because the PCR and viral genome copy data is from 'rich' countries.
estimatedDailyExcrementWeight = 0.149; #kg, mean from table3 of Rose2015: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4500995/
estimatedDailyExcrementWeightSd = 0.095; #kg, standard deviation from table3 of Rose2015: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4500995/
#Convert to volume. Assuming density = 1, see Table 1 of https://www.eawag.ch/fileadmin/Domain1/Abteilungen/sandec/publikationen/EWM/FS_Quantification_Characterisation/synthetic_human_faeces.pdf
estimatedDailyExcremenetVolume = estimatedDailyExcrementWeight * 1; #Litres
estimatedDailyExcremenetVolumeSD = estimatedDailyExcrementWeightSd * 1; #Litres


#Estimate of proportion of viral RNA copies that represent viable virus in stool
proportionViralRnaViable = [1.0/10**1, 1.0/10**2, 1.0/10**3, 1.0/10**4]; #Large uncertainty here so repeat calculating using multiple values


#Scale shedding by excrement amount
perCapitaDailySheddingNormal = estimatedDailyExcremenetVolume*viralRnaInExcrement; #copies per litre excrement
output["dailyPerCapitaCopiesInExcrement"] = perCapitaDailySheddingNormal;
perCapitaDailySheddingNormalUncertaintyRatio = np.sqrt((estimatedDailyExcremenetVolumeSD/estimatedDailyExcremenetVolume)**2 + (viralRnaInExcrementSD/viralRnaInExcrement)**2);
output["dailyPerCapitaCopiesInExcrementUncertaintyRatio"] = perCapitaDailySheddingNormalUncertaintyRatio;


#calculte domestic water usage per capita
domWater = pd.read_csv(inputDir+"dom_waterusage_keller.txt", sep=",", header=None);
domWaterUncertaintyRatio = 0.1; #10%
domWater = domWater.values[:,1]; #m^3 / yr / person
domWater = domWater / (365.25) * 1000; #L / day / person
output["domesticWaterUse"] = domWater


#number of viral particles per litre of raw sewage
copiesInWasteWater = perCapitaDailySheddingNormal/domWater; #copies / L waste water
output["copiesInWasteWater_of_infected_individual"] = copiesInWasteWater;
copiesInWasteWaterUncertaintyRatio = np.sqrt(perCapitaDailySheddingNormalUncertaintyRatio**2 + domWaterUncertaintyRatio**2);

#scale for the proportion of the population that are infectious
countryPopulation = pd.read_csv(inputDir+"population.txt", sep=" ", header=None).values[:,1];
countryPopulation *= 10**6; #Convert from million pop to per one pop
countryPopulationUncertaintyRatio = 0.01;
activeCases = pd.read_csv(inputDir+"active_cases.txt", sep=" ", header=None).values[:,0];
activeCasesUncertaintyRatio = 0.20;


prevalence = activeCases/countryPopulation;
output["prevalence"] = prevalence;
prevalenceUncertaintyRatio = np.sqrt(activeCasesUncertaintyRatio**2 + countryPopulationUncertaintyRatio**2);
output["prevalenceUncertaintyRatio"] = prevalenceUncertaintyRatio;

copiesInWasteWater *= prevalence;
output["copiesInWasteWater"] = copiesInWasteWater;
copiesInWasteWaterUncertaintyRatio = np.sqrt(copiesInWasteWaterUncertaintyRatio**2 + prevalenceUncertaintyRatio**2);


viableCopiesInWasteWaterHighIU = copiesInWasteWater*proportionViralRnaViable[0];
viableCopiesInWasteWaterMedIU = copiesInWasteWater*proportionViralRnaViable[1];
viableCopiesInWasteWaterLowIU = copiesInWasteWater*proportionViralRnaViable[2];
viableCopiesInWasteWaterVLowIU = copiesInWasteWater*proportionViralRnaViable[3];
viableCopiresInWastWaterAllUncertaintyRatio = copiesInWasteWaterUncertaintyRatio;

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
#very low infectious units
pecRiverVLowIULowDf = viableCopiesInWasteWaterVLowIU / dilutionFactorLow;
output["viral_copies_vlowIU_lowDF"] = pecRiverVLowIULowDf;
pecRiverVLowIUMedDf = viableCopiesInWasteWaterVLowIU / dilutionFactor;
output["viral_copies_vlowIU_medDF"] = pecRiverVLowIUMedDf;
pecRiverVLowIUHighDf = viableCopiesInWasteWaterVLowIU / dilutionFactorHigh;
output["viral_copies_vlowIU_highDF"] = pecRiverVLowIUHighDf;

#low infectious units
pecRiverLowIULowDf = viableCopiesInWasteWaterLowIU / dilutionFactorLow;
output["viral_copies_lowIU_lowDF"] = pecRiverLowIULowDf;
pecRiverLowIUMedDf = viableCopiesInWasteWaterLowIU / dilutionFactor;
output["viral_copies_lowIU_medDF"] = pecRiverLowIUMedDf;
pecRiverLowIUHighDf = viableCopiesInWasteWaterLowIU / dilutionFactorHigh;
output["viral_copies_lowIU_highDF"] = pecRiverLowIUHighDf;
#med infectious units
pecRiverMedIULowDf = viableCopiesInWasteWaterMedIU / dilutionFactorLow;
output["viral_copies_medIU_lowDF"] = pecRiverMedIULowDf;
pecRiverMedIUMedDf = viableCopiesInWasteWaterMedIU / dilutionFactor;
output["viral_copies_medIU_medDF"] = pecRiverMedIUMedDf;
pecRiverMedIUHighDf = viableCopiesInWasteWaterMedIU / dilutionFactorHigh;
output["viral_copies_medIU_highDF"] = pecRiverMedIUHighDf;
#high infectious units
pecRiverHighIULowDf = viableCopiesInWasteWaterHighIU / dilutionFactorLow;
output["viral_copies_highIU_lowDF"] = pecRiverHighIULowDf;
pecRiverHighIUMedDf = viableCopiesInWasteWaterHighIU / dilutionFactor;
output["viral_copies_highIU_medDF"] = pecRiverHighIUMedDf;
pecRiverHighIUHighDf = viableCopiesInWasteWaterHighIU / dilutionFactorHigh;
output["viral_copies_highIU_highDF"] = pecRiverHighIUHighDf;

viralCopiesAllUncertaintyRatio = viableCopiresInWastWaterAllUncertaintyRatio;
output["viral_copies_uncertainty_ratio"] = viralCopiesAllUncertaintyRatio;

#temperature
lakeTempDF = pd.read_csv(inputDir+"laketemp.txt", sep=" ", header=None);
output["laketemp_low"] = lakeTempDF.values[:,1];
output["laketemp_med"] = lakeTempDF.values[:,2];
output["laketemp_high"] = lakeTempDF.values[:,3];
seaTempDF = pd.read_csv(inputDir+"seatemp.txt", sep=" ", header=None);
output["seatemp_low"] = seaTempDF.values[:,1];
output["seatemp_med"] = seaTempDF.values[:,2];
output["seatemp_high"] = seaTempDF.values[:,3];


#tmp add:
output["active_cases"] = activeCases;
output["country_population"] = countryPopulation;

#remove countries on blacklist (i.e. that aren't suitable for inclusion)
blacklist = pd.read_csv(inputDir+"blacklist.txt", sep=" ", header=None);
output = output.loc[blacklist[0]==3]

output.to_csv(outputDir+"viral_counts.csv", sep=",", index=False);