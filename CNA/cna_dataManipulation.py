# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 20:39:22 2021

@author: Aleyna Er
"""
#%% loading data

import pandas as pd
import numpy as np

addr = r"C:\Users\Asus\Desktop\gene_mutation_disease_analysis\original datasets\CosmicCompleteCNA.tsv"

cols = ["gene_name","Primary site","Primary histology","TOTAL_CN","MINOR_ALLELE","MUT_TYPE","ID_STUDY","Chromosome:G_Start..G_Stop"]

data = pd.DataFrame(pd.read_csv(addr, sep= "\t", usecols = cols))
#%% 

dhead = data.head(100)
print(data.isna().sum())

# TOTAL CN -> 17044470 null -> ortalama al veya null olan satırları sil
# MINOR_ALLELE -> 55340228 null -> büyük oranda kayıp -> sütunu sil

#%% delete the minor allele column

data.drop(["MINOR_ALLELE"], axis = 1, inplace = True)

#%% delete rest of nans

data.dropna(inplace = True)
print(data.isna().sum())

#%% sort values by study id 

data.sort_values(["ID_STUDY"], ascending = True, ignore_index = True, inplace = True)

#%%   unique value counts / keşif için

#genes = data["gene_name"].value_counts()
genes = len(data["gene_name"].unique())
sites = len(data["Primary site"].unique())
hists = len(data["Primary histology"].unique())
CNs = len(data["TOTAL_CN"].unique())
mut_types = len(data["MUT_TYPE"].unique())
chromos = len(data["Chromosome:G_Start..G_Stop"].unique())

#%% use id study info as index, then drop id study column

data.set_index(data["ID_STUDY"], inplace = True)
data.drop(["ID_STUDY"], axis = 1, inplace = True)

#dtail = data.tail(100)
#%% keşif için

print(data["Primary site"].value_counts(), "\n")
print(data["Primary histology"].value_counts())

#%% gerekli değil ,keşif için

#group = pd.DataFrame(data.groupby(["Chromosome:G_Start..G_Stop"])["gene_name"].apply(list))
#%% get only chromosome name from genomic location


for i in range(len(data)):
    chro = data["Chromosome:G_Start..G_Stop"].values[i]
    chro = chro.split(":")
    data["Chromosome:G_Start..G_Stop"].values[i] = chro[0]
    
data = data.rename(columns = {"Chromosome:G_Start..G_Stop": "Chromosome"})

#%% 

print(data["Primary site"].unique())

#print(data["gene_name"].unique())
#print(data["Primary histology"].unique())

# some of values like 'intestine' contains " _ "
# delete marks and use space instead 

#%% replace marks with space for ui friendly design

for i in range(len(data)):
    
    gene = data["gene_name"].values[i]
    gene = gene.replace("_"," ")
    #print(gene)
    data["gene_name"].values[i] = gene
    
     
    primS = data["Primary site"].values[i]
    primS = primS.replace("_"," ")
    data["Primary site"].values[i] = primS
    
    primH = data["Primary histology"].values[i]
    primH = primH.replace("_"," ")
    data["Primary histology"].values[i] = primH

#%% convert all the variables to lower case - for friendly ui
    
data["gene_name"] = data["gene_name"].str.lower()
data["Primary site"] = data["Primary site"].str.lower()
data["Primary histology"] = data["Primary histology"].str.lower()
data["Chromosome"] = data["Chromosome"].str.lower()

#%% save the processed version of data

data.to_csv("CNA.csv", index = False)