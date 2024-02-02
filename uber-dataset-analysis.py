#!/usr/bin/env python
# coding: utf-8

# In[49]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df = pd.read_csv("uber_data.csv")
df


# In[4]:


df.info()


# In[5]:


df['tpep_pickup_datetime']= pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime']= pd.to_datetime(df['tpep_dropoff_datetime'])


# In[6]:


df.info()


# In[9]:


datetime_dim = df[['tpep_pickup_datetime', 'tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
datetime_dim


# In[12]:


datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday
datetime_dim


# In[17]:


datetime_dim['datetime_id']= datetime_dim.index


# In[19]:


datetime_dim[['datetime_id','tpep_pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday',
'tpep_dropoff_datetime', 'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]


# In[21]:


passenger_count_dim = df[['passenger_count']].drop_duplicates().reset_index(drop=True)
passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
passenger_count_dim = passenger_count_dim[['passenger_count_id', 'passenger_count']]

trip_distance_dim = df[['trip_distance']].drop_duplicates().reset_index(drop=True)
trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
trip_distance_dim = trip_distance_dim[['trip_distance_id', 'trip_distance']]


# In[22]:


rate_code_type = {
    1: "Starndard rate",
    2: "JFK",
    3: "Newark",
    4: "Nassau or Westchester",
    5: "Negotiated Fare",
    6: "Group ride"
}

rate_code_dim = df[['RatecodeID']].drop_duplicates().reset_index(drop=True)
rate_code_dim['rate_code_id'] = rate_code_dim.index
rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
rate_code_dim = rate_code_dim[['rate_code_id', 'RatecodeID', 'rate_code_name']]

rate_code_dim.head()


# In[26]:


pickup_loc_dim = df[['pickup_latitude', 'pickup_longitude']].drop_duplicates().reset_index(drop=True)
pickup_loc_dim['pickup_loc_id'] = pickup_loc_dim.index
pickup_loc_dim = pickup_loc_dim[['pickup_loc_id', 'pickup_latitude', 'pickup_longitude']]

drop_loc_dim = df[['dropoff_latitude', 'dropoff_longitude']].drop_duplicates().reset_index(drop=True)
drop_loc_dim['drop_loc_id'] = drop_loc_dim.index
drop_loc_dim = drop_loc_dim[['drop_loc_id', 'dropoff_latitude', 'dropoff_longitude']]


# In[27]:


payment_type_name = {
    1: "Credit Card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip"
}

payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)
payment_type_dim['payment_type_id'] = payment_type_dim.index
payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
payment_type_dim = payment_type_dim[['payment_type_id', 'payment_type', 'payment_type_name']]

payment_type_dim.head()


# In[28]:


fact_table = df.merge(passenger_count_dim, on='passenger_count')            .merge(trip_distance_dim, on='trip_distance')            .merge(rate_code_dim, on='RatecodeID')            .merge(pickup_loc_dim, on=['pickup_latitude', 'pickup_longitude'])            .merge(drop_loc_dim, on=['dropoff_latitude', 'dropoff_longitude'])            .merge(datetime_dim, on=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])            .merge(payment_type_dim, on='payment_type')            [['VendorID', 'datetime_id', 'passenger_count_id', 'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag',
             'pickup_loc_id', 'drop_loc_id', 'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
             'improvement_surcharge', 'total_amount']]

fact_table.head()
            


# # Find the busiest hours

# In[36]:


ride_frequency = datetime_dim['pick_hour'].value_counts().sort_values(ascending=False)
ride_frequency


# In[44]:


hourly_ride_counts = datetime_dim['pick_hour'].value_counts().sort_index()
hourly_ride_counts


# In[47]:


plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.plot(hourly_ride_counts.index, hourly_ride_counts.values, marker='o')
plt.title('Hourly Ride Counts')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Rides')
plt.grid(True)

plt.grid(axis='y')

plt.tight_layout()
plt.show()


# # Geographical Analysis

# In[52]:


plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.scatterplot(x='pickup_longitude', y='pickup_latitude', data=df, alpha=0.5)
plt.title('Popular Pickup Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)


plt.subplot(1, 2, 2)
sns.scatterplot(x='dropoff_longitude', y='dropoff_latitude', data=df, alpha=0.5)
plt.title('Popular Drop-off Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

plt.tight_layout()
plt.show()


# In[ ]:




