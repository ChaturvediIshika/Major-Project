# -*- coding: utf-8 -*-
"""Disease_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-ThiQAdsy-Fqm_YKzmFPwloJ8HlvGYwq

**Importing necessory libraries**
"""

import numpy as np
import pandas as pd
import math

"""**Reading DataSet containing symptoms and diseases**"""

df=pd.read_csv("./data/dataset.csv")
df.head()

"""**Describing data to understand it**"""

df.describe()

# df.info()

"""**Reading symptom weights**"""

df2=pd.read_csv("./data/Symptom-severity.csv")
df2=df2.set_index('Symptom')
df2.head()

"""Reading Disease Precautions"""

precaution=pd.read_csv("./data/symptom_precaution.csv")
precaution=precaution.set_index('Disease')
precaution.head()

"""Reading Disease Description"""

description=pd.read_csv("./data/symptom_Description.csv")
description=description.set_index('Disease')
description.head()

"""**Extracting unique symptoms**"""

columns=df[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
       'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
       'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
       'Symptom_15', 'Symptom_16', 'Symptom_17']].values.flatten()
columns=pd.unique(columns)
columns=[str(s).strip().replace(" ","_").replace("__","_") for s in columns]
columns.remove('nan')
columns

"""**Creating new DataFrame**
**Performing Data Pre Processing and data cleaning**
"""

new_df=pd.DataFrame(columns=columns,index=df.index)
new_df

diseases=[]
for i in range(len(df)):
  row=df.iloc[i]
  diseases.append(row['Disease'])
  for s in row[1:]:
    sym=str(s).strip().replace(" ","_").replace("__","_")
    if sym == 'nan':
      continue
    new_df.loc[i][sym]=1
    if sym in df2.index:
      if isinstance(df2.loc[sym]['weight'],np.int64):
        new_df.loc[i][sym]=int(df2.loc[sym]['weight'])

symptoms=new_df.fillna(0)
symptoms

diseases

"""**Import Classifier model and metrics from sklearn library**"""

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score



"""**Splitting into training and testing data**"""

x_train,x_test,y_train,y_test=train_test_split(symptoms,diseases,test_size=0.33,random_state=42)
x_train

y_train

"""**Using Decision Tree Classifier, fitting the model to training data and predicting result for test data**"""

model=DecisionTreeClassifier(criterion="gini")
model.fit(x_train,y_train)
y_pred=model.predict(x_test)
y_pred

"""**Checking accuracy of our model**"""

accuracy_score(y_pred,y_test)

confusion_matrix(y_pred,y_test)








"""Creating python flask server

"""

from flask import Flask,jsonify,request,Response,json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def getSymptoms():
    return jsonify(columns)

@app.route("/",methods=['POST'])
def predict():
  symptoms=json.loads(request.data)
  ndf=pd.DataFrame(index=[1],columns=columns)
  for s in symptoms:
    sym=str(s).strip().replace(" ","_").replace("__","_")
    ndf[sym]=1
    if sym in df2.index:
      if isinstance(df2.loc[sym]['weight'],np.int64):
        ndf[sym]=int(df2.loc[sym]['weight'])
  ndf=ndf.fillna(0)
  disease=str(model.predict(ndf)[0]).strip();
  print(disease)

  pre=precaution.loc[disease]
  pre=pre.dropna()
  pre=pre.values.tolist()
  print(pre)
  desc=description.loc[disease]
  desc=desc.values.tolist()
  print(desc)

  obj={}
  obj['disease']=disease
  obj['precautions']=pre
  obj['description']=desc

  print(obj)
  return jsonify(obj)

# app.run()





