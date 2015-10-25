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

#import numpy as np
year_count = frame[["year", "count"]].groupby('year')['count'].sum()
#name_count.sort(["count"], ascending = [False])
print type(year_count)
print year_count.index, year_count.values


year_count.describe
#import matplotlib.pyplot as plt
plt.plot(year_count.index, year_count.values)
plt.show()
