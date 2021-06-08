# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 22:20:08 2021

@author: Asus
"""

import pandas as pd

addr =  r"C:\Users\Asus\Desktop\genxmutasyonxhastalık analizi\original datasets\CosmicNCV.tsv"
cols =  ["Primary site","Primary histology","Histology subtype 1","zygosity","genome position","WT_SEQ","MUT_SEQ","FATHMM_MKL_NON_CODING_SCORE"]

data = pd.DataFrame(pd.read_csv(addr, sep = "\t", usecols = cols))

#%%

dhead = data.head(100)
data.info()
#%% finding out null variables and delete the rows that contain nan

print(data.isnull().sum())
# WT_SEQ column has 545493 null variable
# MUT_SEQ column has 739108 null var
# FATHMM_MKL_NON_CODING_SCORE column has 1312356 null var

data = data.dropna() # delete rows that contains nuan

#%% FATHMM_MKL_NON_CODING_SCORE column will be encoded 0-1
# given that, FATMM non-coding score value > .7 is functionally significant (for further info:  COSMIC database)
# 1: significant 0: non-significant

for i in range(len(data)):
    if(data["FATHMM_MKL_NON_CODING_SCORE"].values[i] > 0.7):
        data["FATHMM_MKL_NON_CODING_SCORE"].values[i] = 1
    else:
        data["FATHMM_MKL_NON_CODING_SCORE"].values[i] = 0
        
#%%   unique value counts / keşif için

#genes = data["gene_name"].value_counts()
sites = len(data["Primary site"].unique())
hists = len(data["Primary histology"].unique())
hist_subs = len(data["Histology subtype 1"].unique())
zygosity = len(data["zygosity"].unique())
WT_SEQ = len(data["WT_SEQ"].unique())
MUT_SEQ = len(data["MUT_SEQ"].unique())
chromos = len(data["Chromosome ID"].unique())

#%% only get chromosome id

for i in range(len(data)):
    chro = data["genome position"].values[i]
    chro = chro.split(":")
    data["genome position"].values[i] = chro[0]
    
data = data.rename(columns = {"genome position": "Chromosome ID"})
        
#%%

data.to_csv("NCV.csv", index = False)

        
#%% label encoding for nucleotides

data["MUT_SEQ"].replace({"A": 0, "T": 1, "G": 2, "C":3}, inplace=True)
data["WT_SEQ"].replace({"A": 0, "T": 1, "G": 2, "C":3}, inplace=True)
        
#print(data.head())


#%%  converting dtype for label encoding

convert_dict = {'Primary site': 'string',
                'Primary histology': 'string',
                'Histology subtype 1' : 'string',
                'zygosity' : 'string',
                'genome position' : int,
                "WT_SEQ" : int,
                "MUT_SEQ": int,
                "FATHMM_MKL_NON_CODING_SCORE" : int
                }

data = data.astype(convert_dict)
data.info()


#%% labeling the rest automatically

data_copy = pd.DataFrame(data.iloc[:,:5])

from sklearn import preprocessing

le = preprocessing.LabelEncoder()
data_copy = data_copy.apply(le.fit_transform)

#%% drop the columns in data that not-encoded

cols = data.iloc[:,:5]
data.drop(cols, axis=1, inplace = True)

#%% combine the encoded columns

frames = [data_copy,data]
final_df = pd.concat(frames, axis = 1)

#%% save the final df, encoded version

final_df.to_csv("ncv_encoded.csv",index = False)