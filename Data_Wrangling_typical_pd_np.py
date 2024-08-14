import pandas as pd
import numpy as np


df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

#check percentage of missing values in each attribute
df.isnull().sum()/len(df)*10
#see how many launches in each launch sites
launch = df['LaunchSite'].value_counts()
df_launch = pd.DataFrame(launch)
#see occurrence of each orbits
orbit = df['Orbit'].value_counts()
df_orbit = pd.DataFrame(orbit)
#analyse the outcome
landing_outcomes = df['Outcome'].value_counts() #count occurence of each landing outcomes
#give index to each outcome
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
#extract bad outcomes (why [1,3,5,6,7]? you can see by printing landing outcomes with index)
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])


#create one more column ['class'], if success landing = 1, failed = 0
#create list of outcome with 0s and 1s (landing_class)
landing_class = []
for i in df['Outcome']:
    if (i == 'True ASDS' or i == 'True RTLS' or i == 'True Ocean'):
        landing_class.append(1)
    else:
        landing_class.append(0)
len(landing_class) #check if same len as df or not
#create new column and assign list to it
df['Class']=landing_class
#see success rate by using .mean()
df["Class"].mean()
#export
df.to_csv("dataset_part_2.csv", index=False)












