import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint

%matplotlib inline

crimes=pd.read_csv("dc_crime2018423.csv",parse_dates=['START_DATE'])
crimes.head()

crimes.describe()

crimes['ucr-rank'].describe()

crimes.dtypes

crimetypes = crimes[['WARD','offensegroup','offense-text','offensekey','ucr-rank','OFFENSE','METHOD','START_DATE']]
crimetypes.head()

offense_group = crimetypes.groupby('OFFENSE')
offense_group.size()

ucr_avg = offense_group.mean()
ucr_avg.sort_values(by='ucr-rank').head()

my_plot = ucr_avg.plot(kind='bar')

my_plot = ucr_avg.sort_values(by='ucr-rank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Offense")
my_plot.set_xlabel("Offense")
my_plot.set_ylabel("UCR Rank (1-9)")

crimetypes = crimes[['offensegroup','WARD','ucr-rank','START_DATE']]
crimetypes.head()

ward_group=crimetypes.groupby(['offensegroup','WARD']).mean()

ward_group.head(20)

ward_group.unstack().head()

my_plot = ward_group.unstack().plot(kind='bar',stacked=True,title="UCR by Ward")
my_plot.set_xlabel("Wards")
my_plot.set_ylabel("Average UCR Rank")

my_plot = ward_group.unstack().plot(kind='bar',stacked=True,title="Average UCR Rank by Ward",figsize=(9, 7))
my_plot.set_xlabel("Wards")
my_plot.set_ylabel("Average UCR Rank")
my_plot.legend(["Average","Ward 1","Ward2","Ward 3","Ward 4","Ward 5"], loc=9,ncol=6)

crime_patterns = crimes[['ucr-rank','START_DATE']]
crime_patterns.head()

crime_plot = crime_patterns['ucr-rank'].hist(bins=9)
crime_plot.set_title("Crime Patterns")
crime_plot.set_xlabel("Average UCR Ranks (1-9)")
crime_plot.set_ylabel("Number of Crimes")

crime_patterns = crimes[['ucr-rank','START_DATE']]
crime_patterns.head(10)

crime_patterns.tail(20)

#Doesn't work for some reason
crime_patterns = crime_patterns.set_index('START_DATE')
crime_patterns.tail(12)

crime_patterns.tail(200).resample('A',how=sum)

crime_patterns.resample('Y').mean() #not working for year end
crime_patterns.tail(12)

crime_plot = crime_patterns.resample('M',how=sum).plot(title="Average UCR Rank by Month",legend=None)
crime_plot.tail(10)


