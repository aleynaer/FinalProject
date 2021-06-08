# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 20:27:48 2021

@author: Asus
"""
import pandas as pd

adr = r"C:\Users\Asus\Desktop\genxmutasyonxhastalık analizi\CNA\cna.csv"
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

# lab = y_label.head(100)
# a = le.inverse_transform([4])
# a[0]

#%% concat encoded columns for training

final_df = pd.concat([x_cols, y_cols], axis = 1)

#%%  *** your ml code here ***