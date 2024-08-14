# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

from js import fetch
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp = await fetch(URL)
dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df=pd.read_csv(dataset_part_2_csv)
df.head(5)

#categorical plot (looks like scatter plot)
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5) #aspect ratio -> width / height ratio
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()


#bar 
df_bar = df.groupby('Orbit')['Class'].mean()
df_bar.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Orbit')
plt.ylabel('Success Rate')
plt.title('Success Rate according to Orbit')
plt.show()


# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        #split("-") => split string into multiple substring if there is "-" in the string
        #[0] => take the first element of substring that are separated, which is the year
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()
    


#line
df_line = df.groupby('Date')['Class'].mean().reset_index()
#Plot the line chart
plt.figure(figsize=(10, 6))
plt.plot(df_line['Date'], df_line['Class'], marker='o')
#labeling
plt.xlabel('Year', fontsize=14)
plt.ylabel('Success Rate', fontsize=14)
plt.title('Success Rate vs Year', fontsize=16)
plt.show()


#dummy variables (convert from categorical data to 1,0; thus easy to parse and do machine learning)
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
# Applying get_dummies to create one-hot encoded variables for the specified columns
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
# Displaying the first few rows of the resulting DataFrame
features_one_hot.head()

#change to float data type
features_one_hot = features_one_hot.astype('float64')
features_one_hot.head()
features_one_hot.dtypes
features_one_hot.info() 


#export to csv file
features_one_hot.to_csv('dataset_part_3.csv', index=False)






