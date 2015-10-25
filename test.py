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
frame.describe


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

print name1945_o[name1945_o["diff"] < 0.8].sort(["total"],ascending=[False]).head()
print name2013_o[name2013_o["diff"] < 0.8].sort(["total"],ascending=[False]).head()


# 4. Percentage Increase

# total number of names per year
yearTotalDF = frame[["year", "count"]].groupby(["year"]).sum().reset_index()
# total number of counts per name per year
nameFrameDF = frame[["name", "year", "count"]].groupby(["year", "name"]).sum().reset_index()
# Get the percentages for each name per year
nameFrameDF = pd.merge(nameFrameDF, yearTotalDF, left_on = "year", right_on = "year", how = "inner")
nameFrameDF["pctFreq"] = nameFrameDF["count_x"]/nameFrameDF["count_y"]*100

