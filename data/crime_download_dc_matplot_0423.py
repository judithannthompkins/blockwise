# Standard import for pandas, numpy and matplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read in the csv file and display some of the basic info
crimes=pd.read_csv("dc_crime2018423.csv",parse_dates=['START_DATE'])
print( "Data types in the file:")
print(crimes.dtypes)
print("Summary of the input file:")
print(crimes.describe())

print("Basic UCR Rank stats:")
print(crimes['ucr-rank'].describe())

#from http://pbpython.com/simple-graphing-panddc_crime2018423.csvas.html

# Filter the columns down to the ones we need to look at for ward crimes
#customers = sales[['name','ext price','date']]
#customer_group = customers.groupby('name')
#sales_totals = customer_group.sum()

crimetypes = crimes[['WARD','ucr-rank','START_DATE']]
print("Crime Types")
print(crimetypes.head())


offense_group = crimetypes.groupby('WARD')
ucrrank_mean = offense_group.mean()
print(ucrrank_mean)



# Create a basic bar chart for the sales data and show it
bar_plot = ucrrank_mean.sort_values(by='ucr-rank',ascending=False).plot(kind='bar',legend=None,title="UCR Rank by Ward")
bar_plot.set_xlabel("Wards")
bar_plot.set_ylabel("UCR (1-9))")
plt.show()


# Do a similar chart but break down by category in stacked bars
# Select the appropriate columns and group by name and category
#customers = sales[['name','category','ext price','date']]
# Do a similar chart but break down by category in stacked bars
# Select the appropriate columns and group by name and category

#customers = sales[['name','category','ext price','date']]
#category_group = customers.groupby(['name','category']).sum()

#This is weird; need to fix

crimetypes = crimes[['WARD','OFFENSE','ucr-rank','START_DATE']]
offense_group = crimes.groupby(['WARD','ucr-rank']).mean()
stack_bar_plot = offense_group.unstack().plot(kind='bar',stacked=True,title="Average UCR Rank by Ward",figsize=(9, 7))
stack_bar_plot.set_xlabel("Wards")
stack_bar_plot.set_ylabel("UCR Ranks")
stack_bar_plot.legend(["Total","Ward 1","Ward 2","Ward 3","Ward 4","Ward 5"], loc=9,ncol=4)
plt.show()



# Create a simple histogram of purchase volumes
crime_patterns = crimes[['ucr-rank','START_DATE']]
crime_plot = crime_patterns['ucr-rank'].hist(bins=20)
crime_plot.set_title("Crime Patterns")
crime_plot.set_xlabel("ucr-rank")
crime_plot.set_ylabel("Number of crimes")
fig = crime_plot.get_figure()
plt.show()
fig.savefig("total-crimes.png")



# Create a line chart showing purchases by month
# Resampling commands deprecated; see new way to do this
crime_patterns = crime_patterns.set_index('START_DATE')
month_plot = crime_patterns.resample('M',how=sum).plot(title="Total Crimes by Month",legend=None)
fig = month_plot.get_figure()
#Show the image, then save it
plt.show()
fig.savefig("total-crimes-month.png")

year_plot = crime_patterns.resample('A',how=sum).plot(title="Total Crimes by Year",legend=None)
fig = year_plot.get_figure()
#Show the image, then save it
plt.show()
fig.savefig("total-crimes-annual.png")
