# Standard import for pandas, numpy and matplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

#my_plot = ucrrank_mean.plot(kind='bar')
#plt.show()


my_plot = ucrrank_mean.sort_values(by='ucrrank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Business in Rank Order")
my_plot.set_xlabel("Businesses")
my_plot.set_ylabel("UCR Rank (1-9)")
plt.show()

businesses = loc_crimes[['business_name','ucrrank']]
print(businesses.head())

ucr_group=loc_crimes.groupby(['business_name','ucrrank']).mean()
print(ucr_group)
#print(ucr_group.head(20))

stack_bar_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Businesses Block Crimes by Average UCR BY YEAR",figsize=(7, 5))
#stack_bar_plot = ucr_group.unstack().plot(kind='bar',stacked=True,title="Businesses Block Crimes by Average UCR BY YEAR",figsize=(9, 6))
stack_bar_plot.set_xlabel("Business")
stack_bar_plot.set_ylabel("Average UCR Rank")
stack_bar_plot.legend(["UCR 1","UCR 2","UCR 3","UCR 4","UCR 5","UCR 6","UCR 7","UCR 8","UCR 9"], loc=9,ncol=4)
plt.show()


crime_patterns = loc_crimes[['ucrrank','report_date']]
crime_patterns = crime_patterns.set_index('report_date')
print(crime_patterns.head(10))


crime_plot = crime_patterns['ucrrank'].hist(bins=10)
crime_plot.set_title("UCR Crime Patterns")
crime_plot.set_xlabel("UCR Rank(1-9)")
crime_plot.set_ylabel("Number of Crimes")
plt.show()

# Create a line chart showing purchases by month
crime_patterns = loc_crimes[['ucrrank','report_date']]
crime_patterns = crime_patterns.set_index('report_date')
month_plot = crime_patterns.resample('M',how=sum).plot(title="Total Crime by Month",legend=None)
fig = month_plot.get_figure()

#Show the image, then save it
plt.show()
fig.savefig("total-crimes.png")

