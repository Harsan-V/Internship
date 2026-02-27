import pandas as pd
import numpy as np

df = pd.read_csv("adult.csv")

df = df.replace("?", np.nan)

print(df.head(10))

print(df.isnull().sum())


#   workclass - 2799 missing
#   occupation - 2809 missingp
#   native-country - 857 missing

#   workclass.  ---> MAR
df['workclass'] = df['workclass'].fillna(df['workclass'].mode()[0])

#   Occupation -----> MAR
df['occupation'] = df['occupation'].fillna(df['occupation'].mode()[0])

#native-country.  -------> MAR
df['native-country']=df['native-country'].fillna(df['native-country'].mode()[0])

print(df.isnull().sum())

print(df['occupation'].head(10))

df.to_csv("adult_cleaned.csv", index=False)