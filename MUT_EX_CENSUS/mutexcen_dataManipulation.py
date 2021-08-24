# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 20:40:06 2021

@author: Aleyna Er
"""

#%% loading data

import pandas as pd
import numpy as np

addr = r"C:\Users\Asus\Desktop\gene_mutation_disease_analysis\original datasets\CosmicMutantExportCensus.tsv"

cols = ["Gene name","ID_sample","Primary site","Primary histology","Histology subtype 1","Mutation Description","Mutation genome position","FATHMM prediction","Tumour origin"]

data = pd.DataFrame(pd.read_csv(addr, sep= "\t", usecols = cols))

#%% sorting values by sample id

data.sort_values(["ID_sample"], ascending = True, inplace = True, ignore_index = True)
data.set_index(data["ID_sample"], inplace = True)

#%% checking for null values

data.drop(["ID_sample"], inplace = True, axis = 1)
data.info()
# Mutation genome position 126803 and
# FATHMM prediction contains null values

#%% handling with nulls

# FATHMM için yeni bir değer oluştutulur ve nan yerine konur
data["FATHMM prediction"].replace({np.nan:"unknown"}, inplace = True)

# genome position eğitimde kullanılacaksa null barındıran satırlar silinir
data.dropna(inplace = True) # null bulunduran satırlar silinir

# eğitimde kullanılmayacaksa direkt genome pos sütunu silinir
# data.drop(["Mutation genome position"], inplace = True, axis = 1)

print(data.isna().sum())

#%%

print(data["Mutation genome position"].value_counts())

# 1.5 milyon satırlık veride 936bin çeşit genome pozisyonu var
# pek kullanışlı değil -> sadece kromozom bilgisini al

#%% changing genome position columnn into chromosome id 

for i in range(len(data)):
    chro = data["Mutation genome position"].values[i]
    chro = chro.split(":")
    data["Mutation genome position"].values[i] = chro[0]
    
data = data.rename(columns = {"Mutation genome position": "Chromosome ID"})

#%% 

print(data["Mutation Description"].unique()
# some of values like 'Substitution - Missense'contains - 
# delete - mark and use space instead 

#%% replace "-" mark with space for ui friendly design


for i in range(len(data)):
    
    primS = data["Primary site"].values[i]
    primS = primS.replace("_"," ")
    #print(primS)
    data["Primary site"].values[i] = primS
     
    primH = data["Primary histology"].values[i]
    primH = primH.replace("_"," ")
    data["Primary histology"].values[i] = primH
    
    histS1 = data["Histology subtype 1"].values[i]  
    histS1 = histS1.replace("_"," ")
    data["Histology subtype 1"].values[i] = histS1 

#%% convert all the variables to lower case - for friendly ui
    
data["Gene name"] = data["Gene name"].str.lower()
data["Primary site"] = data["Primary site"].str.lower()
data["Primary histology"] = data["Primary histology"].str.lower()
data["Histology subtype 1"] = data["Histology subtype 1"].str.lower()
data["Mutation Description"] = data["Mutation Description"].str.lower()
data["Chromosome ID"] = data["Chromosome ID"].str.lower()
data["FATHMM prediction"] = data["FATHMM prediction"].str.lower()
data["Tumour origin"] = data["Tumour origin"].str.lower()

#%%   unique value counts / keşif için -> to select the predict (y) variable

#genes = data["gene_name"].value_counts()
genes = len(data["Gene name"].unique())  # 710
sites = len(data["Primary site"].unique()) # 45
hists = len(data["Primary histology"].unique()) # 127
hist_subs = len(data["Histology subtype 1"].unique()) # 587
mut_desc = len(data["Mutation Description"].unique()) # 13
chromos = len(data["Chromosome ID"].unique()) # 24
fathmms = len(data["FATHMM prediction"].unique()) # 3
tumour_org = len(data["Tumour origin"].unique()) # 7
    
#%% save the processed version of data

data.to_csv("MutExpCensus.csv", index = False)


