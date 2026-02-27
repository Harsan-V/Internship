import pandas as pd
import numpy as np

df = pd.read_csv("Titanic-Dataset.csv.xls")

print(df.isnull().sum()) #----> Missiing Values

# So Age is 177
# Cabin is 687
# Embarked 2


'''
For Age It Depends on Two Factors : 1 -----> Fare (Less Fair , But not same value The most as Pclass)
                                    2 -----> Pclass (For 3rd Class its Missing Most)

So we can say  Age depends on Pclass.
'''
'''To Solve we can use Mean or Median
    
    Mean = Average of Values.  So From The Age Data Most 3rd Class Age are below 30 so Mean is Not Right.

    So We go Median as Mean Gives Average Of All Values.
    '''  

# Age ----> MAR
df['Age'] = df.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.median()))
print(df.groupby('Pclass')['Age'].median())
print(df['Age'])
print(df.head(10))


# Embarked -----> MCAR
''' We Can Use Mode as Its missing values are 2 and Most often For that Case S comes'''

df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])



#Cabin ------> MAR

# Create Has_Cabin feature
df['Has_Cabin'] = df['Cabin'].notnull().astype(int)

# Drop original Cabin column
df = df.drop('Cabin', axis=1)

print(df.isnull().sum())

df.to_csv("Titanic-cleaned.csv",index="False")
