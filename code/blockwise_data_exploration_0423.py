
# coding: utf-8

# This Notebook is based first on adapting the code on the following web page to explore our DC crime data:  
# 
# http://pbpython.com/simple-graphing-pandas.html
# 

# In[16]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
pd.__version__


# In[17]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[18]:


crimes=pd.read_csv("dc_crime2018423.csv",parse_dates=['START_DATE'])
crimes.head()


# In[19]:


crimes.describe()


# In[20]:


crimes['ucr-rank'].describe()


# In[21]:


crimes.dtypes


# In[22]:


crimetypes = crimes[['WARD','offensegroup','offense-text','offensekey','ucr-rank','OFFENSE','METHOD','START_DATE']]
crimetypes.head()


# In[23]:


offense_group = crimetypes.groupby('OFFENSE')
offense_group.size()


# In[25]:


ucr_avg = offense_group.mean()
ucr_avg.sort_values(by='ucr-rank').head()


# In[26]:


my_plot = ucr_avg.plot(kind='bar')


# In[27]:


my_plot = ucr_avg.sort_values(by='ucr-rank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Offense")
my_plot.set_xlabel("Offense")
my_plot.set_ylabel("UCR Rank (1-9)")


# In[28]:


crimetypes = crimes[['offensegroup','WARD','ucr-rank','START_DATE']]
crimetypes.head()


# In[29]:


ward_group=crimetypes.groupby(['offensegroup','WARD']).mean()


# In[63]:


ward_group.head(20)


# In[30]:


ward_group.unstack().head()


# In[31]:


my_plot = ward_group.unstack().plot(kind='bar',stacked=True,title="UCR by Ward")
my_plot.set_xlabel("Wards")
my_plot.set_ylabel("Average UCR Rank")


# In[32]:


my_plot = ward_group.unstack().plot(kind='bar',stacked=True,title="Average UCR Rank by Ward",figsize=(9, 7))
my_plot.set_xlabel("Wards")
my_plot.set_ylabel("Average UCR Rank")
my_plot.legend(["Average","Ward 1","Ward2","Ward 3","Ward 4","Ward 5"], loc=9,ncol=6)


# In[33]:


crime_patterns = crimes[['ucr-rank','START_DATE']]
crime_patterns.head()


# In[34]:


crime_plot = crime_patterns['ucr-rank'].hist(bins=9)
crime_plot.set_title("Crime Patterns")
crime_plot.set_xlabel("Average UCR Ranks (1-9)")
crime_plot.set_ylabel("Number of Crimes")


# In[35]:


crime_patterns = crimes[['ucr-rank','START_DATE']]
crime_patterns.head(10)


# In[81]:


crime_patterns.tail(20)


# In[36]:


#Doesn't work for some reason
crime_patterns = crime_patterns.set_index('START_DATE')
crime_patterns.tail(12)


# In[37]:


#Changing the sampling to year instead of month
crime_patterns.tail(200).resample('A',how=sum)


# In[38]:


crime_patterns.resample('Y').mean() #not working for year end
crime_patterns.tail(12)


# #try this - doesn't work
# #https://stackoverflow.com/questions/41517127/python-pandas-resample-date-range?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
# date_range = crime_patterns(start = '5/3/2005', periods =5+1, freq='1D')
# new_date_range = crime_patterns.date_range(date_range.min(), date_range.max(), freq='30 min')

# In[39]:


crime_plot = crime_patterns.resample('M',how=sum).plot(title="Average UCR Rank by Month",legend=None)
crime_plot.tail(10)


# In[172]:


#This csv file comes from a postgres View that links the blockadvisor_location and blockadvisor_crime tables (crimes for each location)
loc_crimes=pd.read_csv("location_crime_20180424.csv",parse_dates=['report_date'])
loc_crimes.head()


# In[91]:


loc_crimes.describe()


# In[92]:


loc_crimes['ucrrank'].describe()


# In[93]:


loc_crimes.dtypes


# In[173]:


businesses = loc_crimes[['business_name','offense','category01','ucrrank','report_date']]
businesses.head(200)


# In[186]:


business_group = businesses.groupby('category01')
business_group.size()


# In[187]:


business_group = businesses.groupby('business_name')
business_group.size()


# In[188]:


ucrrank_mean = business_group.mean()
ucrrank_mean.sort_values(by='ucrrank').head(9)


# In[189]:


my_plot = ucrrank_mean.plot(kind='bar')


# In[190]:


my_plot = ucrrank_mean.sort_values(by='ucrrank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Business")
my_plot.set_xlabel("Businesses")
my_plot.set_ylabel("UCR Rank (1-9)")


# In[146]:


businesses = loc_crimes[['business_name','ucrrank']]
businesses.head()


# In[166]:


ucr_group=loc_crimes.groupby(['business_name','ucrrank']).mean()
ucr_group.head()


# In[167]:


ucr_group.unstack().head()


# In[168]:


my_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Average UCR Rank by Business")
my_plot.set_xlabel("Businesses")
my_plot.set_ylabel("Average UCR Rank")


# In[154]:


#Something wrong here
my_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Average UCR by Business",figsize=(9, 7))
my_plot.set_xlabel("Businesses")
my_plot.set_ylabel("Average UCR Rank")
my_plot.legend(["Mean","1","2","3","4","5","6","7","8","9"], loc=9,ncol=4)


# In[169]:


crime_patterns = loc_crimes[['ucrrank','report_date']]
crime_patterns.head(20)


# In[170]:


crime_patterns = crime_patterns.set_index('report_date')
crime_patterns.head(10)


# In[158]:


crime_patterns.resample('M',how=sum)


# In[171]:


crime_plot = crime_patterns.resample('M',how=sum).plot(title="Average UCR Rank by Month",legend=None)

