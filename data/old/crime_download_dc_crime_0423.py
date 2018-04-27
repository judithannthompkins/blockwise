import wget
import datetime

now = datetime.datetime.now()
csvfile = "dc_crime" + str(now.year) + str(now.month) + str(now.day)

url = 'https://datagate.dc.gov/search/open/crimes?daterange=2years&details=true&format=csv'  
wget.download(url, csvfile + '.csv') 

