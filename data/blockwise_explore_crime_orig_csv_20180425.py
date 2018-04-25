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

# Filter the columns down to the ones we need to look at for customer sales
crimetypes = crimes[['WARD','offensegroup','ucr-rank','OFFENSE','START_DATE']]
print(crimetypes.head())

#Group the customers by name and sum their sales
#customer_group = customers.groupby('name')
#sales_totals = customer_group.sum()

offense_group = crimetypes.groupby('OFFENSE')
print(offense_group.size())

ucr_avg = offense_group.mean()
ucr_avg.sort_values(by='ucr-rank').head()


# Create a basic bar chart for the sales data and show it
bar_plot = ucr_avg.sort_values(by='ucr-rank',ascending=False).plot(kind='bar',legend=None,title="Average UCR Rank by Ward")
bar_plot.set_xlabel("Ward")
bar_plot.set_ylabel("UCR Rank (1-9)")
plt.show()

# Do a similar chart but break down by category in stacked bars
# Select the appropriate columns and group by name and category
crimetypes = crimes[['offensegroup','WARD','ucr-rank','START_DATE']]
print(crimetypes.head())
ward_group=crimetypes.groupby(['offensegroup','WARD']).sum()
print(ward_group.head(20))


# Plot and show the stacked bar chart
stack_bar_plot = ward_group.unstack().plot(kind='bar',stacked=True,title="Crimes by Offense Group by Ward",figsize=(9, 6))
stack_bar_plot.set_xlabel("Ward")
stack_bar_plot.set_ylabel("Average UCR Rank")
stack_bar_plot.legend(["Ward 1","Ward 2","Ward 3","Ward 4","Ward 5","Ward 6","Ward 7","Ward 8"], loc=9,ncol=4)
plt.show()


# Create a simple histogram
crime_patterns = crimetypes[['ucr-rank','START_DATE']]
crime_plot = crime_patterns['ucr-rank'].hist(bins=20)
crime_plot.set_title("Crime Patterns")
crime_plot.set_xlabel("UCR Rank (1-9)")
crime_plot.set_ylabel("Number of Crime")
plt.show()


# Create a line chart showing purchases by month
crime_patterns = crime_patterns.set_index('START_DATE')
month_plot = crime_patterns.resample('M',how=sum).plot(title="Total Crimes by Month",legend=None)
fig = month_plot.get_figure()

#Show the image, then save it
plt.show()
fig.savefig("crime_over_time.png")
