# Standard import for pandas, numpy and matplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['toolbar'] = 'None'
SMALL_SIZE = 9
plt.rc('font', size=SMALL_SIZE)
#plt.rc('axes', titlesize=SMALL_SIZE)

# Read in the csv file and display some of the basic info
loc_crimes=pd.read_csv("location_crime_20180424.csv",parse_dates=['report_date'])
print(loc_crimes.head())

print( "Data types in the file:")
print(loc_crimes.dtypes)
print("Summary of the input file:")
print(loc_crimes.describe())

print("Basic UCR Rank stats:")
print(loc_crimes['ucrrank'].describe())

businesses = loc_crimes[['business_name','offense','category01','ucrrank','report_date']]
print(businesses.head(200))

print("GROUP CRIMES BY BUSINESS CATEGORY")
business_group = businesses.groupby('category01')
print(business_group.size())

print("GROUP CRIMES BY BUSINESS NAME")
business_group = businesses.groupby('business_name')
print(business_group.size())

ucrrank_mean = business_group.mean()
print(ucrrank_mean.sort_values(by='ucrrank').head(9))

my_plot = ucrrank_mean.sort_values(by='ucrrank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Business in Rank Order",figsize=(9,6))
my_plot.set_xlabel("Businesses")
my_plot.set_ylabel("UCR Rank (1-9)")
plt.tight_layout()
plt.subplots_adjust(left=0.1, bottom=0.3)
fig = my_plot.get_figure()
plt.show()
fig.savefig("business_by_ucr_avg1.png")

businesses = loc_crimes[['business_name','ucrrank']]
print(businesses.head())

ucr_group=loc_crimes.groupby(['business_name','ucrrank']).mean()
print(ucr_group)
#print(ucr_group.head(20))

stack_bar_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Businesses Block Crimes by Average UCR",figsize=(9,6))
#stack_bar_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Businesses Block Crimes by Average UCR BY YEAR",figsize=(9, 6))
stack_bar_plot.set_xlabel("Business")
stack_bar_plot.set_ylabel("Average UCR Rank")
stack_bar_plot.legend(["UCR 1","UCR 2","UCR 3","UCR 4","UCR 5","UCR 6","UCR 7","UCR 8","UCR 9"], loc=9,ncol=4)
plt.tight_layout()
plt.subplots_adjust(left=0.1, bottom=0.3)
#plt.subplots_adjust(left=0.1, bottom=0.1)
fig = stack_bar_plot.get_figure()
plt.show()
fig.savefig("business_by_ucr_avg2.png")


crime_patterns = loc_crimes[['ucrrank','report_date']]
crime_patterns = crime_patterns.set_index('report_date')
print(crime_patterns.head(10))

crime_plot = crime_patterns['ucrrank'].hist(bins=10)
crime_plot.set_title("UCR Crime Patterns")
crime_plot.set_xlabel("UCR Rank(1-9)")
crime_plot.set_ylabel("Number of Crimes")
fig = crime_plot.get_figure()
plt.show()
fig.savefig("crime_patterns.png")

# Create a line chart showing purchases by month
crime_patterns = loc_crimes[['ucrrank','report_date']]
crime_patterns = crime_patterns.set_index('report_date')
month_plot = crime_patterns.resample('M',how=sum).plot(title="Total Crime by Month",legend=None)
fig = month_plot.get_figure()

#Show the image, then save it
plt.show()
fig.savefig("crime_by_month.png")

