#!/usr/bin/env python
# coding: utf-8

# In[16]:


# Dependencies and Setup
import scipy.stats as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
get_ipython().run_line_magic('matplotlib', 'inline')

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(r'C:\Users\gonza\Desktop\du-den-data-pt-08-2020-u-c\05-Matplotlib\Homework\Instructions\Pymaceuticals\data\Mouse_metadata.csv', low_memory = False,)
study_results = pd.read_csv(r'C:\Users\gonza\Desktop\du-den-data-pt-08-2020-u-c\05-Matplotlib\Homework\Instructions\Pymaceuticals\data\Study_results.csv')
#mouse_metadata.head(10)
#study_results.head(10)
#turn data into dataframe
mouse_df = pd.DataFrame(mouse_metadata)
study_df = pd.DataFrame(study_results)
# Combine the data into a single dataset
ds = pd.merge(mouse_df, study_df, on = 'Mouse ID', how = 'outer')
# Display the data table for preview
ds.head(10)


# In[18]:


#Use groupby to get t vol by regimen
mean = ds.groupby('Drug Regimen')['Tumor Volume (mm3)'].mean()
median = ds.groupby('Drug Regimen')['Tumor Volume (mm3)'].median()
variance = ds.groupby('Drug Regimen')['Tumor Volume (mm3)'].var()
std = ds.groupby('Drug Regimen')['Tumor Volume (mm3)'].std()
sem = ds.groupby('Drug Regimen')['Tumor Volume (mm3)'].sem()
summary_df = pd.DataFrame({"Mean": mean, "Median": median, "Variance": variance, "Standard Deviation": std, "SEM": sem})
summary_df.head(10)
#Combined all variables made into one dataframe\ table 


# In[23]:


#Bar plot using pandas, total number of mice
grouped_df = pd.DataFrame(ds.groupby(["Drug Regimen"]).count()).reset_index()
c = grouped_df[["Drug Regimen","Mouse ID"]]
c.plot(kind="bar", figsize=(10,3))
plt.title("Count per Drug Regimen")
plt.xlabel('Drug Regimen')
plt.ylabel('Count of Mice')
plt.show()
plt.tight_layout()
#


# In[25]:


#Using matplot... first we get our axis 
regimen_count = (ds.groupby(["Drug Regimen"])["Age_months"].count()).tolist()
x_axis = np.arange(len(regimen_count))
plt.bar(x_axis, regimen_count, color='red', alpha=0.5, align="center")
plt.title("Count for each Treatment")
plt.xlabel("Drug Regimen")
plt.ylabel("Count of Mice")


# In[27]:


#Pie plots for sex, first we filter data, get count of mice, then create new df 
gender_df = pd.DataFrame(ds.groupby(["Sex"]).count()).reset_index()
#gender_df.head()
gender_df = gender_df[["Sex","Mouse ID"]]
gender_df = gender_df.rename(columns={"Mouse ID": "Count"})
gender_df.head()


# In[38]:


#We now plot df, first using pandas
plt.figure(figsize=(10,5))
ax1 = plt.subplot(121, aspect='equal')
gender_df.plot(kind='pie', y = "Count", ax=ax1, autopct='%1.1f%%', startangle=90, shadow=False,labels=gender_df['Sex'], legend = True, fontsize=16)


# In[54]:


#using matplot, use pie. wasnt able to use count variable so just used numbers from last column.. as numbers should be same
#count variable was used to change data into usable for pie chart, but didnt work 
#count = (ds.groupby(["Sex"])["Age_months"].count()).tolist()
labels = ['females', 'Males']
sizes = ['49.4', '50.6']
color = ['Blue', 'Red']
type(count)
plt.pie(sizes, explode = (.1,0), colors= color , labels = labels,  autopct="%1.1f%%", shadow=True, startangle=140)


# In[58]:


#Calculate the final tumor volume of each mouse across four of the most promising treatment regimens
#The four treatments are given, so we make df with those
Cap_df = ds.loc[ds["Drug Regimen"] == "Capomulin",:]
Ram_df = ds.loc[ds["Drug Regimen"] == "Ramicane", :]
Inf_df = ds.loc[ds["Drug Regimen"] == "Infubinol", :]
Cef_df = ds.loc[ds["Drug Regimen"] == "Ceftamin", :]
#Calculate the quartiles and IQR
#we need to do one treatment at a time.. Capomulin first
Cap = Cap_df.groupby('Mouse ID').max()['Timepoint']
Capomulin_vol = pd.DataFrame(Cap)
Capomulin_merge = pd.merge(Capomulin_vol, ds, on=("Mouse ID","Timepoint"),how="left")
Capomulin_merge.head()


# In[59]:


#Ramicane treatment
Ram = Ram_df.groupby('Mouse ID').max()['Timepoint']
Ramicane_vol = pd.DataFrame(Ram)
Ramicane_merge = pd.merge(Ramicane_vol, ds, on=("Mouse ID","Timepoint"),how="left")
Ramicane_merge.head()


# In[60]:


#Infubinol treatment data
Inf = Inf_df.groupby('Mouse ID').max()['Timepoint']
Infubinol_vol = pd.DataFrame(Inf)
Infubinol_merge = pd.merge(Infubinol_vol, ds, on=("Mouse ID","Timepoint"),how="left")
Infubinol_merge.head()


# In[61]:


# Ceftamin
Cef = Cef_df.groupby('Mouse ID').max()['Timepoint']
Ceftamin_vol = pd.DataFrame(Cef)
Ceftamin_merge = pd.merge(Ceftamin_vol, ds, on=("Mouse ID","Timepoint"),how="left")
Ceftamin_merge.head()


# In[62]:


#Now that we have the datasets... we can start to find IQR and etc.
# Cap first. Get the tumor Series data 
Cap_tumors = Capomulin_merge["Tumor Volume (mm3)"]
quartiles =Cap_tumors.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq
print(f"The lower quartile of Capomulin tumors: {lowerq}")
print(f"The upper quartile of Capomulin tumors: {upperq}")
print(f"The interquartile range of Capomulin tumors: {iqr}")
print(f"The median of Capomulin tumors: {quartiles[0.5]} ")
lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[63]:


#ramiucane, get series column, find IQR
Ram_tumors = Ramicane_merge["Tumor Volume (mm3)"]
quartiles =Ram_tumors.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq
print(f"The lower quartile of Ramicane tumors is: {lowerq}")
print(f"The upper quartile of Ramicane tumors is: {upperq}")
print(f"The interquartile range of Ramicane tumors is: {iqr}")
print(f"The median of Ramicane tumors is: {quartiles[0.5]} ")
lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[64]:


#Infubinol
Inf_tumors = Infubinol_merge["Tumor Volume (mm3)"]
quartiles =Inf_tumors.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq
print(f"The lower quartile of Infubinol tumors is: {lowerq}")
print(f"The upper quartile of Infubinol tumors is: {upperq}")
print(f"The interquartile range of Infubinol tumors is: {iqr}")
print(f"The median of Infubinol tumors is: {quartiles[0.5]} ")
lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[65]:


#Ceftamin
Cef_tumors = Ceftamin_merge["Tumor Volume (mm3)"]
quartiles = Cef_tumors.quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq
print(f"The lower quartile of treatment is: {lowerq}")
print(f"The upper quartile of temperatures is: {upperq}")
print(f"The interquartile range of temperatures is: {iqr}")
print(f"The the median of temperatures is: {quartiles[0.5]} ")
lower_bound = lowerq - (1.5*iqr)
upper_bound = upperq + (1.5*iqr)
print(f"Values below {lower_bound} could be outliers.")
print(f"Values above {upper_bound} could be outliers.")


# In[68]:


#Now we graph the above 4 IQR data
data2 = [Cap_tumors, Ram_tumors, Inf_tumors, Cef_tumors]
names= ['Capomulin', 'Ramicane', 'Infubinol','Ceftamin']
fig1, ax1 = plt.subplots(figsize=(15, 10))
ax1.set_title('Tumor Volume at Selected Mouse',fontsize =20)
ax1.set_ylabel('Final Tumor Volume (mm3)',fontsize = 10)
ax1.set_xlabel('Drug Regimen Used',fontsize = 10)
ax1.boxplot(data2, labels = names, widths = 0.5, patch_artist=True,vert=True)
plt.show()


# In[ ]:


#Nnext we use the data for scatter plot

