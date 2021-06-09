# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 21:24:57 2021

@author: Asus
"""
import pandas as pd

adr = r"C:\Users\Asus\Desktop\genxmutasyonxhastalık analizi\MUT_EX_CENSUS\MutExpCensus.csv"
data = pd.DataFrame(pd.read_csv(adr))

#%% convert dtpye for labeling

data = data.astype("string")

#%% merge the data x and y

x_cols = data.drop(columns = ["FATHMM prediction"])
# x_cols = data.iloc[:,:7]
# y_cols = data.iloc[:,7:] # tumour origin için eğitmek istersek
y_cols = pd.DataFrame(data["FATHMM prediction"])

#%% auto label encoding 


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

x_cols = x_cols.apply(le.fit_transform)
y_cols = y_cols.apply(le.fit_transform)

# lab = y_label.head(100)
# a = le.inverse_transform([4])
# a[0]

#%% concat encoded columns for training

#final_df = pd.concat([x_cols, y_cols], axis = 1)

#%% KNN algorithm

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

#%% knn save model

import joblib
  
# Save the model as a pickle in a file
joblib.dump(clf, 'MutExcCen-knn-fathmm.pkl')

#%% random forest algorithm

#import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test =train_test_split(x_cols, y_cols, test_size=.25, random_state=17)

classifier = RandomForestClassifier(n_estimators=200, random_state=0)

#y_train_array = np.ravel(y_train)

classifier.fit(X_train, y_train)
#%% random forest evaluate
yy_pred = classifier.predict(X_test)
print(metrics.classification_report(y_test, yy_pred))
#%% random forest save model
import joblib
  
# Save the model as a pickle in a file
joblib.dump(classifier, 'MutExcCen-rforest-fathmm.pkl')


#%% kmeans algorithm

from sklearn.cluster import KMeans
import sklearn.metrics as sm
from sklearn.metrics import confusion_matrix, classification_report


clustering = KMeans(n_clusters=3, random_state=5)

clustering.fit(x_cols)

#%% kmeans evaluate
print(classification_report(y_cols, clustering.labels_))




#%% naive bayes algorithm

from sklearn.naive_bayes import CategoricalNB

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(x_cols, y_cols, test_size=.25, random_state=17)

CatNB = CategoricalNB()
CatNB.fit(X_train, y_train)

y_expect = y_test
y_pred = CatNB.predict(X_test)

print(accuracy_score(y_expect, y_pred))

print(metrics.classification_report(y_expect, y_pred))


#%% naive bayes save model

import joblib
  
# Save the model as a pickle in a file
joblib.dump(CatNB, 'MutExcCen-naiveBayes-fathmm.pkl')

#%% logistic regression algorithm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(x_cols, y_cols, test_size=.25, random_state=17)

LogReg = LogisticRegression(solver='liblinear',multi_class='ovr', random_state=200)
LogReg.fit(X_train, y_train)

#%% Log Reg evaluate 
from sklearn.metrics import classification_report

y_pred = LogReg.predict(X_test)
print(classification_report(y_test, y_pred))

print('Training accuracy:', LogReg.score(X_train, y_train))
print('Test accuracy:', LogReg.score(X_test, y_test))
#%% Log reg save model

import joblib
  
# Save the model as a pickle in a file
joblib.dump(LogReg, 'MutExcCen-LogReg-fathmm.pkl')

#%% FATHMM tahmininde accuracy'ler;

# KNN = %84
# Random forest = %86
# naive bayes = %82
# logistic reg = %78

# kmeans = %39 -> muhtemelen kümeleme yapmayız daha





















