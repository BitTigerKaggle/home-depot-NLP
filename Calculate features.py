# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 08:00:00 2016
@authors: Victor, yogaaa
"""
import numpy as np
import pandas as pd

pd.set_option('display.line_width', 5000)
pd.set_option('display.max_columns', 60)

###########################################################################################
# ----------------------------------------Query Match-------------------------------------#

def search(query, title, description, brand, bullet, material,attr):
    des_list = list()
    title_list = list()
    brand_list = list()
    mat_list = list()
    bullet_list = list()
    attr_list = list()
    xbi = list()
    count = 0
    last_in_title = 0
    last_in_des = 0
    last_in_bullet = 0
    title_res = 0
    des_res = 0
    brand_res = 0
    mat_res = 0
    bullet_res = 0
    attr_res = 0
    len_of_query = len(query)
    for element in query:
        if element == "xbi":
            xbi.append(count)
            title_list.append(0)
            des_list.append(0)
            brand_list.append(0)
            mat_list.append(0)
            bullet_list.append(0)
        else:
            if element in title:
                title_list.append(1)
                if count == len_of_query - 1:
                    last_in_title = 1
            if element not in title:
                title_list.append(0)
            if element in description:
                des_list.append(1)
                if count == len_of_query - 1:
                    last_in_des = 1
            if element not in description:
                des_list.append(0)
            if element in brand:
                brand_list.append(1)
            if element not in brand:
                brand_list.append(0)
            if element in attr:
                attr_list.append(1)
            if element not in attr:
                attr_list.append(0)
            if element in material:
                mat_list.append(1)
            if element not in material:
                mat_list.append(0)
            if element in bullet:
                bullet_list.append(1)
                if count == len_of_query - 1:
                    last_in_bullet = 1
            if element not in bullet:
                bullet_list.append(0)
        count += 1

        # if title_list[len(title_list) - 1] == 1:
        #     last_in_title = 1
        # if des_list[len(des_list) - 1] == 1:
        #     last_in_des = 1
        # if bullet_list[len(bullet_list) - 1] == 1:
        #     last_in_bullet = 1

        title_res = sum(title_list)
        des_res = sum(des_list)
        brand_res = sum(brand_list)
        mat_res = sum(mat_list)
        bullet_res = sum(bullet_list)
        attr_res = sum(attr_list)

    return [des_list, title_list, brand_list, mat_list, bullet_list, attr_list,
            title_res, des_res, brand_res, mat_res, bullet_res, attr_res,
            xbi, last_in_title, last_in_des, last_in_bullet]


###########################################################################################
# -------------------------------------------Main-----------------------------------------#

def main(name):
    df = pd.read_csv("data_"+name+".csv").ix[:, 1:]
    print df.shape
    df.set_index(df.id)
    search_term = df.search_term
    brand = df.brand
    material = df.material
    bullet = df.bullet
    title = df.product_title
    attr = df.attr_text
    description = df.product_description
    units = ["in", "ft", "lb","sq","cu","gal","oz","cm","mm","ac","deg","volt","watt","amp"]
    positions = ["d", "l", "h", "w"]

    for i in range(0, len(title)):
        if pd.isnull(title[i]):
            title[i] = "not available"
    for i in range(0, len(description)):
        if pd.isnull(description[i]):
            description[i] = "not available"
    for i in range(0, len(material)):
        if pd.isnull(material[i]):
            material[i] = "not available"
    for i in range(0, len(bullet)):
        if pd.isnull(bullet[i]):
            bullet[i] = "not available"
    for i in range(0, len(brand)):
        if pd.isnull(brand[i]):
            brand[i] = "not available"
    for i in range(0, len(attr)):
        if pd.isnull(attr[i]):
            attr[i] = "not available"

    len_of_query = df.len_of_query
    # create an empty dataframe to store the results after searching query terms
    columns = ['title_res', 'des_res', 'brand_res','mat_res', 'bullet_res', 'attr_res',
               'last_in_title', 'last_in_des','last_in_bullet',
               'ratio_query', 'ratio_title', 'ratio_des', 'ratio_brand', 'ratio_bullet','ratio_attr',
               'xbi_mark', 'xbi_ratio']
    result = pd.DataFrame(data=np.zeros((0, len(columns))), columns=columns)

    for i in range(0, len(search_term)):
        [des_list, title_list, brand_list, mat_list, bullet_list, attr_list,
         title_res, des_res, brand_res, mat_res, bullet_res, attr_res,
         xbi, last_in_title, last_in_des, last_in_bullet] \
            = search(str(search_term[i]).split(), str(title[i]).split(), str(description[i]).split(), str(brand[i]).split(),
                     str(bullet[i]).split(), str(material[i]).split(), str(attr[i]).split())

        ratio_title = float(title_res)/len_of_query[i]
        ratio_des = float(des_res)/len_of_query[i]
        ratio_brand = float(brand_res)/len_of_query[i]
        ratio_bullet = float(bullet_res)/len_of_query[i]
        ratio_attr = float(attr_res)/len_of_query[i]

        # find the inverted list of the query across all product information
        final_list = [max(a, b, c, d, e, f) for a, b, c, d, e, f in
                      zip(title_list, des_list, brand_list, bullet_list, mat_list, attr_list)]
        # ratio that represents the portion of query terms is found in product information
        if (len_of_query[i] - len(xbi))==0:
            ratio_query = 0
        else:
            ratio_query = float(sum(final_list)) / (len_of_query[i] - len(xbi))

        xbi_mark = 0
        xbi_ratio = -1
        terms = str(search_term[i]).split()
        #print(terms)
        len_terms = len(terms)

        if len(xbi) != 0:
            for i in xbi:
                # if xbi is not on the first index, and both item b/f and after xbi exists, mark
                if i >= 1 and i < len_terms-1:
                    if i >= 3 and terms[i-1] in positions:
                        k = i-3
                    elif i >= 2 and terms[i-1] in units:
                        k = i-2
                    else:
                        k = i-1
                    if i < len_terms-3 and terms[i+1] in positions:
                        l = 1+3
                    elif i < len_terms-2 and terms[i+1] in units:
                        l = i+2
                    else:
                        l = i+1
                    if k >= 0 and l < len(title_list) and title_list[k] == 1 and title_list[l] == 1:
                        xbi_mark += 1
                    elif k >= 0 and l < len(des_list) and des_list[k] == 1 and des_list[l] == 1:
                        xbi_mark += 1
                    elif k >= 0 and l < len(bullet_list) and bullet_list[k] == 1 and bullet_list[l] == 1:
                        xbi_mark += 1
                    elif k >= 0 and l < len(brand_list) and brand_list[k] == 1 and brand_list[l] == 1:
                        xbi_mark += 1
                    elif k >= 0 and l < len(mat_list) and mat_list[k] == 1 and mat_list[l] == 1:
                        xbi_mark += 1
            # ratio that represents the portion of "and" relationships in the query is satisfied
            xbi_ratio = float(xbi_mark) / len(xbi)

        result = result.append({'title_res': title_res,'des_res': des_res, 'brand_res': brand_res, 'mat_res': mat_res,
                                'bullet_res': bullet_res, 'attr_res': attr_res,
                                'last_in_title': last_in_title, 'last_in_des': last_in_des,
                                'last_in_bullet': last_in_bullet,
                                'ratio_query': ratio_query,'ratio_title': ratio_title, 'ratio_des': ratio_des,
                                'ratio_brand': ratio_brand, 'ratio_bullet': ratio_bullet, 'ratio_attr': ratio_attr,
                                'xbi_mark': xbi_mark, 'xbi_ratio': xbi_ratio}, ignore_index=True)
    #print(result)
    df = pd.DataFrame.merge(df, result, right_index=True, left_index=True)
    print df.shape
    df.to_csv("dataframe_"+name+".csv")


main("train")
print "train processing finished"
main("test")
print "test processing finished"