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

