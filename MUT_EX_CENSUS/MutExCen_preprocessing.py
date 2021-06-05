# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:43:37 2021

@author: Asus
"""

import pandas as pd
import numpy as np

addr = r"C:\Users\Asus\Desktop\genxmutasyonxhastalık analizi\original datasets\CosmicMutantExportCensus.tsv"

cols = ["Gene name","ID_sample","Primary site","Primary histology","Histology subtype 1","Mutation Description","Mutation genome position","FATHMM prediction","Tumour origin"]

data = pd.DataFrame(pd.read_csv(addr, sep= "\t", usecols = cols))

#%%

data.sort_values(["ID_sample"], ascending = True, inplace = True, ignore_index = True)
data.set_index(data["ID_sample"], inplace = True)

#%% checking for null values

data.drop(["ID_sample"], inplace = True, axis = 1)
data.info()
# Mutation genome position
# FATHMM prediction contains null

#%% handling with nulls

# FATHMM için yeni bir değer oluştutulur ve nan yerine konur
data["FATHMM prediction"].replace({np.nan:"unknown"}, inplace = True)

# genome position eğitimde kullanılacaksa null barındıran satırlar silinir
# eğitimde kullanılmayacaksa direkt genome pos sütunu silinir

data.dropna(inplace = True) # null bulunduran satırlar silinir
# data.drop(["Mutation genome position"], inplace = True, axis = 1)

print(data.isna().sum())

#%%

print(data["Mutation genome position"].value_counts())

# 1.5 milyon satırlık veride 936bin çeşit genome pozisyonu var
# pek kullanışlı değil -> sadece kromozomu al

#%%

for i in range(len(data)):
    chro = data["Mutation genome position"].values[i]
    chro = chro.split(":")
    data["Mutation genome position"].values[i] = chro[0]
    
data = data.rename(columns = {"Mutation genome position": "Chromosome ID"})

#%%   unique value counts / keşif için

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

data.to_csv("MutExpCensus.csv")

#%% labeling for train part

# all the dtypes are object as default, 
# and all our variables are categorical
# so apply automatic labeling 

data = data.astype("string")

from sklearn import preprocessing

le = preprocessing.LabelEncoder()
data_copy = data.apply(le.fit_transform)

# predict ve diğerlerini ayrı mı labellamak lazım acaba? -- evet !!!!!!!!!!!!
#%%

data_copy.to_csv("MutExpCensusLabeled.csv", index = False)