# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:36:58 2021

@author: Aleyna Er
"""
#%% load dataset

import pandas as pd

adr = r"C:\Users\Asus\Desktop\gene_mutation_disease_analysis\CNA\CNA.csv"
data = pd.DataFrame(pd.read_csv(adr))

#%% convert dtpye for labeling

data = data.astype("string")

#%% merge the data x and y

x_cols = data.drop(columns = ["Primary histology"])
# x_cols = data.iloc[:,:5]
# y_cols = data.iloc[:,5:] # kromozom için eğitmek istersek
y_cols = pd.DataFrame(data["Primary histology"])

#%% auto label encoding 


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

x_cols = x_cols.apply(le.fit_transform)
y_cols = y_cols.apply(le.fit_transform)


#%% naive bayes algorithm

from sklearn.naive_bayes import CategoricalNB

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(x_cols, y_cols, test_size=.25, random_state=17)

CatNB = CategoricalNB()
CatNB.fit(X_train, y_train)

#%%
y_expect = y_test
y_pred = CatNB.predict(X_test)

print(accuracy_score(y_expect, y_pred))

print(metrics.classification_report(y_expect, y_pred))

#%% save model for test phase

import pickle

pickle.dump(CatNB, open("cna_primHist.pkl","wb"))
model = pickle.load(open("cna_primHist.pkl","rb"))

#%%% save the labels for using in test.py

gene_name = pd.DataFrame(columns=["unlabeled","labeled"])
gene_name["unlabeled"] = data["gene_name"].unique()
gene_name["labeled"] = x_cols["gene_name"].unique()
gene_name.to_csv("1_geneName.csv", index = False)



prim_site = pd.DataFrame(columns=["unlabeled","labeled"])
prim_site["unlabeled"] = data["Primary site"].unique()
prim_site["labeled"] = x_cols["Primary site"].unique()
prim_site.to_csv("2_prim_site.csv", index = False)


copyNum = pd.DataFrame(columns=["unlabeled","labeled"])
copyNum["unlabeled"] = data["TOTAL_CN"].unique()
copyNum["labeled"] = x_cols["TOTAL_CN"].unique()
copyNum.to_csv("3_copyNum.csv", index = False)


mut_type = pd.DataFrame(columns=["unlabeled","labeled"])
mut_type["unlabeled"] = data["MUT_TYPE"].unique()
mut_type["labeled"] = x_cols["MUT_TYPE"].unique()
mut_type.to_csv("4_mut_type.csv", index = False)


chromosome = pd.DataFrame(columns=["unlabeled","labeled"])
chromosome["unlabeled"] = data["Chromosome"].unique()
chromosome["labeled"] = x_cols["Chromosome"].unique()
chromosome.to_csv("5_chromosome.csv", index = False)


prim_hist = pd.DataFrame(columns=["unlabeled","labeled"])
prim_hist["unlabeled"] = data["Primary histology"].unique()
prim_hist["labeled"] = y_cols["Primary histology"].unique()
prim_hist.to_csv("6_prim_hist.csv", index = False)