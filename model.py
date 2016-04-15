# -*- coding: utf-8 -*-
# created on Thu Apr 07 17:00:00 2016
# @authors: Victor

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import Imputer


pd.set_option('display.line_width', 5000)
pd.set_option('display.max_columns', 60)

###########################################################################################
# ----------------------------------------Functions---------------------------------------#
def RMSE(y,y_pred):
    return mean_squared_error(y, y_pred)**0.5

def dropfeature(data):
    data = data.drop('product_title',1)
    data = data.drop('search_term',1)
    data = data.drop('brand',1)
    data = data.drop('material',1)
    data = data.drop('bullet',1)
    data = data.drop('product_description',1)
    data = data.drop('attr_text',1)
    data = data.drop('product_uid',1)
    #data = data.drop('id',1)
    #data = data.drop('ratio_attr',1)
   # data = data.drop('len_of_attr',1)
   # data = data.drop('ratio_des',1)
   # data = data.drop('ratio_title',1)
   # data = data.drop('ratio_bullet',1)

    return data
###########################################################################################
# -------------------------------------------Main-----------------------------------------#
'''
data = pd.read_csv("dataframe.csv").ix[:, 1:]
data = fixbug(data)
print data.head()
'''


train = pd.read_csv("dataframe_train.csv").ix[:, 1:]
test = pd.read_csv("dataframe_test.csv").ix[:, 1:]

train = dropfeature(train)
test = dropfeature(test)




'''
print test.head()
print ''
print train.head()

print np.isnan(train.any())
print np.isfinite(train.all())
'''
Ytrain = train.relevance
Xtrain = train.drop('relevance',1)
Xtrain = Imputer().fit_transform(Xtrain)

print "start to build random forest model"
model1= RandomForestRegressor(n_estimators=100, n_jobs=-1).fit(Xtrain, Ytrain)
predicted= model1.predict(Xtrain)
print "random forest (train):",RMSE(Ytrain,predicted)
Xtest = Imputer().fit_transform(test)
predicted = model1.predict(Xtest)
res = pd.DataFrame({'id': test.id, 'relevance': predicted})

res.to_csv("submit3.csv")


