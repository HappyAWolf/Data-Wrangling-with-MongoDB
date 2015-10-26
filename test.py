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



# Part B. Find other insights
# Merge with census data and see what we can find
# For the in house data we only focus on 2010+ to save time
frame_ge2010 = frame[(frame["year"]>=2010) & (frame["year"]<=2014)]
print frame_ge2010.describe()
print frame_ge2010.columns

# Some functions to clean the data
def get_region(state):
    if state in ['DE', 'DC', 'MD', 'FL', 'GA', 'NC', 'SC', 'VA', 'WV', 'AL', 'KT', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX']:
        return 3
    elif state in ['CT', 'ME', 'MA', 'RI', 'VT', 'NH', 'PA', 'NJ', 'NY']:
        return 1
    elif state in ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD']:
        return 2
    elif state in ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']:
        return 4

def get_gender_code(gender):
    if gender in ['F', 'Female']:
        return 2
    else:
        return 1

def get_state_code(state):
    if state == 'Alabama':
        return 'AL'
    if state == 'Alaska':
        return 'AK'
    if state == 'Arizona':
        return 'AZ'
    if state == 'Arkansas':
        return 'AR'
    if state == 'California':
        return 'CA'
    if state == 'Colorado':
        return 'CO'
    if state == 'Connecticut':
        return 'CT'
    if state == "Delaware":
        return "DE"
    if state == "Florida":
        return "FL"
    if state == 'Georgia':
        return "GA"
    if state == 'Hawaii':
        return "HI"
    if state == 'Idaho':
        return "ID"
    if state == 'Illinois':
        return "IL"
    if state == 'Indiana':
        return "IN"
    if state == 'Iowa':
        return "IA"
    if state == 'Kansas':
        return "KS"
    if state == 'Kentucky':
        return "KY"
    if state == 'Louisiana':
        return "LA"
    if state == 'Maine':
        return "ME"
    if state == 'Maryland':
        return "MD"
    if state == 'Massachusetts':
        return "MA"
    if state == 'Michigan':
        return "MI"
    if state == 'Minnesota':
        return "MN"
    if state == 'Mississippi':
        return "MS"
    if state == 'Missouri':
        return "MO"
    if state == 'Montana':
        return "MT"
    if state == 'Nebraska':
        return "NE"
    if state == 'Nevada':
        return "NV"
    if state == 'New Hampshire':
        return "NH"
    if state == 'New Jersey':
        return "NJ"
    if state == 'New Mexico':
        return "NM"
    if state == 'New York':
        return "NY"
    if state == 'North Carolina':
        return "NC"
    if state == 'North Dakota':
        return "ND"
    if state == 'Ohio':
        return "OH"
    if state == 'Oklahoma':
        return "OK"
    if state == 'Oregon':
        return "OR"
    if state == 'Pennsylvania':
        return "PA"
    if state == 'Rhode Island':
        return "RI"
    if state == 'South Carolina':
        return "SC"
    if state == 'South Dakota':
        return "SD"
    if state == 'Tennessee':
        return "TN"
    if state == 'Texas':
        return "TX"
    if state == 'Utah':
        return "UT"
    if state == 'Vermont':
        return "VT"
    if state == 'Virginia':
        return "VA"
    if state == 'Washington':
        return "WA"
    if state == 'West Virginia':
        return "WV"
    if state == 'Wisconsin':
        return "WI"
    if state == 'Wyoming':
        return "WY"

# To make things easy, the top names in 2010+ are directly copied from the SSA webpage. 
def top_names(name):
    return name in ["Emma", "Olivia", "Sophia", "Isabella", "Ava", "Noah", "Liam", "Mason", "Jacob", "William", "Jayden", "Michael"]
        
# Continue clean the data
frame_ge2010["gender_code"] = frame_ge2010.apply(lambda row: get_gender_code(row["gender"]), axis = 1)
frame_ge2010.columns = ["state", "sex", "year", "name", "count", "gender"]

# Here we create a label to flag the most popular names. It is impractical to predict the actual names, but predicting popular names is totally doable. 
frame_ge2010["top_name"] = frame_ge2010.apply(lambda row: top_names(row["name"]), axis = 1)

print frame_ge2010.describe()
print frame_ge2010.columns


# Read in the downloaded Census data
filename = 'PEP_2014_PEPSR5H.csv'
newfile = directory + '/' + filename
print newfile

census_df = pd.read_csv(newfile, index_col = None, header = 0)
print census_df.describe()
census_df2 = census_df[["Year.display-label", "Sex.display-label", "Hisp.display-label", "GEO.display-label", "wac", "bac", "iac", "aac", "nac"]]
census_df2 = census_df2[(census_df2["Sex.display-label"]!='Both Sexes') & (census_df2["Hisp.display-label"]=='Total') & (census_df2["GEO.display-label"]!='United States') & (census_df2['Year.display-label'] != 'April 1, 2010 Estimates Base') & (census_df2['Year.display-label'] != 'April 1, 2010 Census')]
print census_df2.describe()

census_df2["year"] = census_df2.apply(lambda row: int(row["Year.display-label"][-2:])+2000, axis = 1)
census_df2["gender"] = census_df2.apply(lambda row: get_gender_code(row["Sex.display-label"]), axis = 1) 
census_df2["state"] = census_df2.apply(lambda row: get_state_code(row["GEO.display-label"]), axis = 1)
census_df2["total"] = census_df2["wac"]+census_df["bac"]+census_df["iac"]+census_df["aac"]+census_df["nac"]
census_df2.describe()

census_df3 = census_df2[["year", "state", "gender", "wac", "bac", "iac", "aac", "nac", "total"]]

# Now combining the two data together
new_frame = pd.merge(frame_ge2010, census_df3, left_on = ["state", "year", "gender"], right_on = ["state", "year", "gender"], how = "inner")


# In order to find the relations between fields, all fields must be numeric or at least coded numeric

from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)

# we need to implement handler function to check for numerical values
# for now just the list of categorical fields
frame_nocat = MultiColumnLabelEncoder(columns = ['state', 'name']).fit_transform(new_frame)
frame_nocat.columns


# Find the Spearman correlation among different variables
from scipy.stats import spearmanr, kendalltau, pearsonr

print spearmanr(frame_nocat["state"], frame_nocat["name"])
print spearmanr(frame_nocat["top_name"], frame_nocat["gender"])
print spearmanr(frame_nocat["top_name"], frame_nocat["wac"])
print spearmanr(frame_nocat["top_name"], frame_nocat["bac"])
print spearmanr(frame_nocat["top_name"], frame_nocat["aac"])
print spearmanr(frame_nocat["top_name"], frame_nocat["nac"])
print spearmanr(frame_nocat["top_name"], frame_nocat["state"])

# We are going to train a model to predict top popular names. So the entire data are split into training and test sets. 
msk = np.random.rand(len(frame_nocat)) < 0.6

train = frame_nocat[msk]
test = frame_nocat[~msk]

#print train.describe()
#print test.describe()

y_train = train['top_name']
x_train = train
x_train.drop(['top_name', 'sex'], axis=1, inplace=True)
x_train.head()


# MODELING ###
# Multiple methods with cross validtaion to find the most suitable one 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.cross_validation import cross_val_score
#from sklearn.naive_bayes import GaussianNB
#from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

names, accs = [],[]
for algorithm in (LogisticRegression, 
                  KNeighborsClassifier,
                  #GaussianNB,
                  #SVC,
                  DecisionTreeClassifier,
                  RandomForestClassifier):

    accuracy = np.mean(cross_val_score(algorithm(), x_train, y_train, cv=10, scoring='accuracy')) #10-fold cross validation with 'accuracy/precision/recall/f1' as scores to output
    print '%-30s %.4f' % (algorithm.__name__, accuracy)
    names.append(algorithm.__name__)
    accs.append(accuracy)


# It is easy to see that Logistic Requesstion wins. So we train a LR to make the prediction. 

model = LogisticRegression()
model = model.fit(x_train, y_train)
model.score(x_train, y_train)

y_train.mean()

# Examine the coefficients
pd.DataFrame(zip(x_train.columns, np.transpose(model.coef_)))



y_test = test['top_name']
x_test = test
x_test.drop(["top_name", 'sex'], axis=1, inplace=True)

predicted = model.predict(x_test)
print predicted

probs = model.predict_proba(x_test)
print probs


# Model check
from sklearn import metrics
print metrics.accuracy_score(y_test, predicted)
print metrics.roc_auc_score(y_test, probs[:, 1])

print metrics.confusion_matrix(y_test, predicted)
print metrics.classification_report(y_test, predicted)





