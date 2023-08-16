#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.cluster import DBSCAN
from math import radians
import json


# In[18]:


# Load the JSON data
with open('livedata.json') as f:
    data = json.load(f)


# In[19]:



# Convert the latitude and longitude strings to floats
for entry in data:
    entry['latitude'] = float(entry['latitude'])
    entry['longitude'] = float(entry['longitude'])

df = pd.DataFrame(data)


# In[20]:


plt.figure(figsize=(8,6))
sns.scatterplot(x='latitude', y='longitude', data=df, hue='id')
plt.legend(bbox_to_anchor=[1, 0.8])
plt.show()


# In[29]:


def get_infected_names(input_name):
    epsilon = 0.0018288
    model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
    df['cluster'] = model.labels_.tolist()

    input_name_clusters = []
    for i in range(len(df)):
        if df['id'][i] == input_name:
            if df['cluster'][i] in input_name_clusters:
                pass
            else:
                input_name_clusters.append(df['cluster'][i])
    
    infected_names = []
    for cluster in input_name_clusters:
        if cluster != -1:
            ids_in_cluster = df.loc[df['cluster'] == cluster, 'id']
            for i in range(len(ids_in_cluster)):
                member_id = ids_in_cluster.iloc[i]
                if (member_id not in infected_names) and (member_id != input_name):
                    infected_names.append(member_id)
                else:
                    pass
    return infected_names

epsilon = 0.0018288  # Define epsilon here
model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['latitude', 'longitude']])
df['cluster'] = model.labels_.tolist()


# In[30]:


labels = df['cluster']
fig = plt.figure(figsize=(12,10))
sns.scatterplot(df['latitude'], df['longitude'], hue=['cluster-{}'.format(x) for x in labels])
plt.legend(bbox_to_anchor=[1, 1])
plt.show()


# In[31]:


unique_names = set()

# Iterate through the data and add names to the set
for entry in data:
    unique_names.add(entry['id'])

# Print the unique names
for name in unique_names:
    print(name)


# In[39]:


print(get_infected_names("Bob"))


# In[ ]:




