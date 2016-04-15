# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:25:43 2016
@authors: Victor
"""

import pandas as pd

pd.set_option('display.line_width', 5000)
pd.set_option('display.max_columns', 60)

###########################################################################################
# ---------------------------------------Only Ascii---------------------------------------#
def onlyascii(s):
    if isinstance(s, int) or isinstance(s, float):
        clist = list(str(s))
    else:
        clist = list(s)
    s =""
    for i in range(0,len(clist)):
        if ord(clist[i]) >=0 and ord(clist[i]) < 128:
            s +=clist[i]
    return s
###########################################################################################
# ---------------------------------------process attr-------------------------------------#

def process_attr(df):
    # the goal of this function is to extract raw text from attr
    res = pd.DataFrame({"product_uid": pd.unique(df.product_uid)})
    res['attr_text'] = 'null'
    for i in range(0, len(res['product_uid'])):
        pid = res.iat[i, 0]
        name = df[df.product_uid == pid]['name']
        value = df[df.product_uid == pid]['value']
        index = name.index.tolist()
        s = ""
        for j in range(0,len(index)):
            s += str(name[index[j]]) + " " + str(value[index[j]]) + " "

        #print s
        res.iat[i, 1] = s
    return res

###########################################################################################
# --------------------------------------------Main----------------------------------------#

attr = pd.read_csv("attributes.csv", encoding="ISO-8859-1")
attr = attr[attr.product_uid.notnull()]
attr = attr[attr.name != "MFG Brand Name"]
attr = attr[attr.name != "Material"]
attr = attr[attr.name != "Bullet01"]
attr = attr[attr.name != "Bullet02"]
attr = attr[attr.name != "Bullet03"]
attr = attr[attr.name != "Bullet04"]
attr = attr[attr.name != "Bullet05"]
attr = attr[attr.name != "Bullet06"]
attr = attr[attr.name != "Bullet07"]
attr = attr[attr.name != "Bullet08"]
attr = attr[attr.name != "Bullet09"]
attr = attr[attr.name != "Bullet10"]
attr = attr[attr.name != "Bullet11"]
attr = attr[attr.name != "Bullet12"]
attr = attr[attr.name != "Bullet13"]
attr = attr[attr.name != "Bullet14"]
attr = attr[attr.name != "Bullet15"]
attr = attr[attr.name != "Bullet16"]
attr = attr[attr.name != "Bullet17"]
attr = attr[attr.name != "Bullet18"]
attr = attr[attr.name != "Bullet19"]
attr = attr[attr.name != "Bullet20"]
attr = attr[attr.name != "Bullet21"]
attr = attr[attr.name != "Bullet22"]
attr = attr[attr.name != "Bullet23"]
attr = attr[attr.name != "Bullet24"]
attr = attr[attr.name != "Bullet25"]
attr = attr[attr.name != "Bullet26"]
attr = attr[attr.name != "Bullet27"]
attr = attr[attr.name != "Bullet28"]
attr = attr[attr.name != "Bullet29"]
attr = attr[attr.name != "Bullet30"]
attr = attr[attr.name != "Bullet31"]

attr['name'] = attr['name'].map(lambda x: onlyascii(x))
attr['value'] = attr['value'].map(lambda x: onlyascii(x))
print "finishing removing non ascii"
df = process_attr(attr)
df.to_csv("attr1.csv")
