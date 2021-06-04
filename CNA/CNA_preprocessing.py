# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 17:46:24 2021

@author: Asus
"""
import pandas as pd

addr = r"C:\Users\Asus\Desktop\genxmutasyonxhastalık analizi\original datasets\CosmicCompleteCNA.tsv"

cols = ["gene_name","Primary site","Primary histology","TOTAL_CN","MINOR_ALLELE","MUT_TYPE","ID_STUDY","Chromosome:G_Start..G_Stop"]
data = pd.DataFrame(pd.read_csv(addr, sep = "\t", usecols = cols))

#%% 

dhead = data.head(100)
print(data.isna().sum())

# TOTAL CN -> 17044470 null -> ortalama al veya null olan satırları sil
# MINOR_ALLELE -> 55340228 null -> büyük oranda kayıp -> sütunu sil

#%%

data.drop(["MINOR_ALLELE"], axis = 1, inplace = True)

#%%

data.dropna(inplace = True)
print(data.isna().sum())
#%%

data.sort_values(["ID_STUDY"], ascending = True, ignore_index = True, inplace = True)

#%%   unique value counts / keşif için

#genes = data["gene_name"].value_counts()
genes = len(data["gene_name"].unique())
sites = len(data["Primary site"].unique())
hists = len(data["Primary histology"].unique())
CNs = len(data["TOTAL_CN"].unique())
mut_types = len(data["MUT_TYPE"].unique())
chromos = len(data["Chromosome:G_Start..G_Stop"].unique())

#%%
data.set_index(data["ID_STUDY"], inplace = True)
data.drop(["ID_STUDY"], axis = 1, inplace = True)

dtail = data.tail(100)
#%% keşif için

print(data["Primary site"].value_counts(), "\n")
print(data["Primary histology"].value_counts())

#%% gerekli değil ,kşif için

group = pd.DataFrame(data.groupby(["Chromosome:G_Start..G_Stop"])["gene_name"].apply(list))
#%% get only chromosome name from genomic location

chromosomes = []

for i in range(len(data)):
    chro = data["Chromosome:G_Start..G_Stop"].values[i]
    chro = chro.split(":")
    data["Chromosome:G_Start..G_Stop"].values[i] = chro[0]
    
data = data.rename(columns = {"Chromosome:G_Start..G_Stop": "Chromosome"})
#%% save unlabeled data

data.to_csv("cna.csv", index = False)

#%% chromosome labeling: 23:X 24:Y

data["Chromosome"].replace({"X": 23, "Y":24}, inplace = True)

#%% manuel labeling

convert_dict = {"gene_name" : 'string',
                "Primary site" : 'string',
                "Primary histology": 'string',
                "TOTAL_CN" : int,
                "MUT_TYPE" : 'string',
                 "Chromosome" : int,}

data = data.astype(convert_dict)
#%% auto label encoding 

data.info()
data_copy = data.drop(columns = ["TOTAL_CN", "Chromosome"])
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
data_copy = data_copy.apply(le.fit_transform)

#%%

data_c2 = pd.DataFrame(data, columns = ["TOTAL_CN", "Chromosome"])
final_data = pd.concat([data_copy, data_c2], axis = 1) 

#%% save labeled data

final_data.to_csv("cna_labeled.csv", index = False)

#%%

# label decode edilebiliyor ama eğitimde direkt kaydedilmişini alıp kullanırsam sorun olur mu?