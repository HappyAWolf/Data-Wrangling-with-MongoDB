import os
import glob
import pandas as pd
import numpy as np
import zipfile

# data directory
directory = '/Users/lullaberry/Downloads/namesbystate'

z = zipfile.ZipFile(directory + '.zip', "r")
print z.namelist()

# load the data files
frame = pd.DataFrame()
list_ = []
for file_ in sorted(z.namelist()):
    if file_ == 'StateReadMe.pdf':
      continue
    df = pd.read_csv(directory + '/' + file_, index_col = None, header = None)
    print file_, df.shape
    list_.append(df)
frame = pd.concat(list_)
print frame.shape

frame.columns = ['state', 'gender', 'year', 'name', 'count']

print frame.describe()
print pd.isnull(frame).any()

# Part A) Descriptive Analysis

#1. Something about the data

year_count = frame[["year", "count"]].groupby('year')['count'].sum()

year_count.describe()
import matplotlib.pyplot as plt
plt.plot(year_count.index, year_count.values)
plt.show()


#2. Most popular name of all time, of either gender

nameFrame = frame[["name","gender","count"]]

nf1 = nameFrame.groupby(["gender", "name"])["count"].sum()

print nf1["F"].argmax(), nf1["F"][nf1["F"].argmax()]
print nf1["M"].argmax(), nf1["M"][nf1["M"].argmax()]
print nf1.argmax(), nf1[nf1.argmax()]



#3. Most gender ambiguous name in 2013, 1945
name1945 = frame[frame.year==1945][["gender", "name", "count"]].groupby(["gender", "name"]).sum().reset_index()
name2013 = frame[frame.year==2013][["gender", "name", "count"]].groupby(["gender", "name"]).sum().reset_index()
#print name1945.shape
#print name1945.describe()
#print name2013.shape
#print name2013.describe()

def get_overlap(df):
    df_f = df[df.gender == 'F'][["name", "count"]]
    df_m = df[df.gender == 'M'][["name", "count"]]
    df_o = pd.merge(df_f, df_m, left_on = "name", right_on = "name", how = "inner")
    df_o["total"] = df_o["count_x"] + df_o["count_y"]
    df_o["diff"] = abs(df_o["count_x"] - df_o["count_y"]) / (df_o["count_x"] + df_o["count_y"])
    return df_o
name2013_o = get_overlap(name2013)
name1945_o = get_overlap(name1945)

import matplotlib.pyplot as plt
name2013_o.plot(kind='scatter', x='diff', y='total')
plt.show()

print name1945_o[name1945_o["diff"] < 0.25].sort(["total"],ascending=[False]).head()
print name2013_o[name2013_o["diff"] < 0.25].sort(["total"],ascending=[False]).head()


# 4. Percentage Increase

# total number of names per year
yearTotalDF = frame[["year", "count"]].groupby(["year"]).sum().reset_index()
# total number of counts per name per year
nameFrameDF = frame[["name", "year", "count"]].groupby(["year", "name"]).sum().reset_index()
# Get the percentages for each name per year
nameFrameDF = pd.merge(nameFrameDF, yearTotalDF, left_on = "year", right_on = "year", how = "inner")
nameFrameDF["pctFreq"] = nameFrameDF["count_x"]/nameFrameDF["count_y"]*100

def get_pctIncrease(df, start_year, end_year):
    df1 = df[df["year"]==start_year][["name", "pctFreq"]]
    df2 = df[df["year"]==end_year][["name", "pctFreq"]]
    df3 = pd.merge(df1, df2, left_on = "name", right_on = "name", how = "inner").fillna(value = 0)
    df3["increase"] = (df3["pctFreq_y"] / df3["pctFreq_x"] - 1) * 100
    return df3

diff = get_pctIncrease(nameFrameDF, 1980, 2014)

print diff.sort(["increase"],ascending=[False]).head(1)
print diff.sort(["increase"],ascending=[True]).head(1)


# 5. Even larger increase/decrease?

def find_max_min(df, start_year, end_year):
    increase = []
    decrease = []
    for j in range(start_year+1, end_year + 1):
        diff = get_pctIncrease(df, start_year, j)
        inc = diff.sort(["increase"],ascending=[False]).head(1).values
        dec = diff.sort(["increase"],ascending=[True]).head(1).values
        increase.append((j, inc[0, 0], inc[0, 1], inc[0, 2], inc[0, 3]))
        decrease.append((j, dec[0, 0], dec[0, 1], dec[0, 2], dec[0, 3]))
    max_inc = 0
    max_ind = 0
    min_inc = 0
    min_ind = 0
    for l in range(len(decrease)):
        if min_inc >= decrease[l][4]:
            min_inc = decrease[l][4]
            min_ind = l
        if max_inc <= increase[l][4]:
            max_inc = increase[l][4]
            max_ind = l
    return (increase[max_ind], decrease[min_ind])

find_max_min(nameFrameDF, 1980, 2014)


def find_global_max_min(df, start_year, end_year):
    max_list = []
    min_list = []
    max_inc = 0
    min_inc = 0
    max_ind = 0
    min_ind = 0
    for j in range(start_year, end_year):
        find = find_max_min(df, j, end_year)
        max_list.append((j, find[0]))
        min_list.append((j, find[1]))
    for l in range(len(max_list)):
        if max_inc <= max_list[l][1][4]:
            max_inc = max_list[l][1][4]
            max_ind = l
        if min_inc >= min_list[l][1][4]:
            min_inc = min_list[l][1][4]
            min_ind = l
    return (max_list[max_ind], min_list[min_ind])

find_global_max_min(nameFrameDF, 1910, 2014)


# Part B) Insights





