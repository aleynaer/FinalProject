# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 21:36:26 2021

@author: Aleyna Er

"""
#%% load the manipulated data

import pandas as pd

adr = r"C:\Users\Asus\Desktop\gene_mutation_disease_analysis\MUT_EX_CENSUS\MutExpCensus.csv"
data = pd.DataFrame(pd.read_csv(adr))

#%% convert dtpye for labeling

data = data.astype("string")

#%% merge the data x and y

x_cols = data.drop(columns = ["Chromosome ID"]) # features
# x_cols = data.iloc[:,:7]
# y_cols = data.iloc[:,7:] # tumour origin için eğitmek istersek
y_cols = pd.DataFrame(data["Chromosome ID"]) # predict value

#%% auto label encoding 

from sklearn.preprocessing import LabelEncoder

leX = LabelEncoder()
leY = LabelEncoder()

x_cols = x_cols.apply(leX.fit_transform)
y_cols = y_cols.apply(leY.fit_transform)

#%% train with KNN algorithm

from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn import metrics

X_train, X_test, y_train, y_test =train_test_split(x_cols, y_cols, test_size=.25, random_state=17)

clf = neighbors.KNeighborsClassifier()
clf.fit(X_train, y_train)
print(clf)

#%% knn evaluate
y_pred= clf.predict(X_test)
y_expect = y_test

print(metrics.classification_report(y_expect, y_pred))

#%% save model for test phase

import pickle

pickle.dump(clf, open("mutexcen_chromosome.pkl","wb"))
model = pickle.load(open("mutexcen_chromosome.pkl","rb"))

#%%

# kromozom_labeled = y_cols["Chromosome ID"].unique()
# kromozom = leY.inverse_transform(y_cols["Chromosome ID"].unique())
# leY.inverse_transform([12])

# a = leY.inverse_transform([12])
# a[0]

#%%

# gene_name = pd.DataFrame(data["Gene name"].unique())


# prim_site = pd.DataFrame(data["Primary site"].unique())
# prim_hist = pd.DataFrame(data["Primary histology"].unique())
# histSub1 = pd.DataFrame(data["Histology subtype 1"].unique())
# mut_desc = pd.DataFrame(data["Mutation Description"].unique())
# fathmm = pd.DataFrame(data["FATHMM prediction"].unique())
# tumour_org = pd.DataFrame(data["Tumour origin"].unique())
    
# chromosome = data["Chromosome ID"].unique()
    
# column_labels = [gene_name,prim_site,prim_hist,histSub1,mut_desc,fathmm,tumour_org,chromosome]

#%%% save the labels for using in test.py

gene_name = pd.DataFrame(columns=["unlabeled","labeled"])
gene_name["unlabeled"] = data["Gene name"].unique()
gene_name["labeled"] = x_cols["Gene name"].unique()
gene_name.to_csv("1_geneName.csv", index = False)



prim_site = pd.DataFrame(columns=["unlabeled","labeled"])
prim_site["unlabeled"] = data["Primary site"].unique()
prim_site["labeled"] = x_cols["Primary site"].unique()
prim_site.to_csv("2_prim_site.csv", index = False)


prim_hist = pd.DataFrame(columns=["unlabeled","labeled"])
prim_hist["unlabeled"] = data["Primary histology"].unique()
prim_hist["labeled"] = x_cols["Primary histology"].unique()
prim_hist.to_csv("3_prim_hist.csv", index = False)


histSub1 = pd.DataFrame(columns=["unlabeled","labeled"])
histSub1["unlabeled"] = data["Histology subtype 1"].unique()
histSub1["labeled"] = x_cols["Histology subtype 1"].unique()
histSub1.to_csv("4_histSub1.csv", index = False)


mut_desc = pd.DataFrame(columns=["unlabeled","labeled"])
mut_desc["unlabeled"] = data["Mutation Description"].unique()
mut_desc["labeled"] = x_cols["Mutation Description"].unique()
mut_desc.to_csv("5_mut_desc.csv", index = False)


fathmm = pd.DataFrame(columns=["unlabeled","labeled"])
fathmm["unlabeled"] = data["FATHMM prediction"].unique()
fathmm["labeled"] = x_cols["FATHMM prediction"].unique()
fathmm.to_csv("6_fathmm.csv", index = False)


tumour_org = pd.DataFrame(columns=["unlabeled","labeled"])
tumour_org["unlabeled"] = data["Tumour origin"].unique()
tumour_org["labeled"] = x_cols["Tumour origin"].unique()
tumour_org.to_csv("7_tumour_org.csv", index = False)


chromosome = pd.DataFrame(columns=["unlabeled","labeled"])
chromosome["unlabeled"] = data["Chromosome ID"].unique()
chromosome["labeled"] = y_cols["Chromosome ID"].unique()
chromosome.to_csv("8_chromosome.csv", index = False)
