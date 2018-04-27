import geopy.distance
import csv

from geopy.distance import geodesic
from geopy.distance import great_circle

'''
#Start with simple test
#Geopy can calculate geodesic distance between two points using the geodesic distance or the great-circle distance,
restaurant = (38.90721, -77.06356)
crime1 = (38.90721387, -77.06325007)
print(str(geodesic(restaurant, crime1).feet) + ' feet from crime')
crime2 = (38.89359008, -77.02295057)
print(str(geodesic(restaurant, crime2).feet) + ' feet from crime')

#print(great_circle(restaurant, crime1).feet)
'''

#Now iterate through .csv file
count = 0
with open('C:\\Users\\Judith\projects\\blockwise\data\\location_crime_geo.csv') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row.
    for row in reader:
        count = count + 1
        if count < 100:
            print('COUNT: ' + str(count))
            loc=row[0]
            loc_addr=row[1] 
            loc_lat=row[2] 
            loc_long=row[3] 
            crime=row[9]
            crime_block=row[6]
            crime_date=row[14] 
            crime_lat=row[7] 
            crime_long=row[8]

            print(loc.upper())
            print(loc_addr)
            print(loc_lat) 
            print(loc_long) 
            print(crime.upper())
            print(crime_block) 
            print(crime_date) 
            print(crime_lat) 
            print(crime_long)
            restaurant_geo=(loc_lat + ', ' + loc_long)
            crime_geo=(crime_lat + ', ' + crime_long)
            print(str(geodesic(restaurant_geo, crime_geo).feet) + ' FEET FROM CRIME')

