# -*- coding: utf-8 -*-

"""

Judy Note:  I used a sample yelp fusion API script from the Yelp website and added code for our purposes.  See Judy Notes integrated below.  
I added functions to:  1) parse the address, 2) save the results to JSON files and 3) save the results to the database

Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API

by using the Search API to query for businesses by a search term and location,

and the Business API to query additional information about the top result

from the search query.



Please refer to http://www.yelp.com/developers/v3/documentation for the API

documentation.



This program requires the Python requests library, which you can install via:

`pip install -r requirements.txt`.



Sample usage of the program:

`python sample.py --term="bars" --location="San Francisco, CA"`

"""

from __future__ import print_function



import argparse

import json, codecs

import pprint

import requests

import sys

import urllib

import psycopg2




# This client code can run on Python 2.x or 3.x.  Your imports can be

# simpler if you only need one of those.

try:

    # For Python 3.0 and later

    from urllib.error import HTTPError

    from urllib.parse import quote

    from urllib.parse import urlencode

except ImportError:

    # Fall back to Python 2's urllib2 and urllib

    from urllib2 import HTTPError

    from urllib import quote

    from urllib import urlencode





# Yelp Fusion no longer uses OAuth as of December 7, 2017.

# You no longer need to provide Client ID to fetch Data

# It now uses private keys to authenticate requests (API Key)

# You can find it on

# https://www.yelp.com/developers/v3/manage_app

API_KEY= None 


#Judy Note:  This is the API key I got from Yelp -- It limits to 50 records per API call, etc.  
API_KEY='SL4N0D6gQDkL5KzkfVw0OfixRtLgT-YcanzuR8TYvQRjdIuyG2Ms6vNjjfBYYXEC1iKRSfeD7_h8UxiAt6rgR6aZGH5iBOkPfRbeQaz0HiDjkNdY8laxSa1ekx61WnYx'


# API constants, you shouldn't have to change these.

API_HOST = 'https://api.yelp.com'

SEARCH_PATH = '/v3/businesses/search'

BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Judy Note:  I edited Yelp script for Washington restaurants. It gets the top 50 restaurants. My license doesn't permit me to raise the search_limit over 50. I tried.

DEFAULT_TERM = 'restaurant'

DEFAULT_LOCATION = 'Washington, DC'

SEARCH_LIMIT = 50

def request(host, path, api_key, url_params=None):

    """Given your API_KEY, send a GET request to the API.

    Args:

        host (str): The domain host of the API.

        path (str): The path of the API after the domain.

        API_KEY (str): Your API Key.

        url_params (dict): An optional set of query parameters in the request.

    Returns:

        dict: The JSON response from the request.


    Raises:

        HTTPError: An error occurs from the HTTP request.

    """

    url_params = url_params or {}

    url = '{0}{1}'.format(host, quote(path.encode('utf8')))

    headers = {

        'Authorization': 'Bearer %s' % api_key,

    }


    print(u'Querying {0} ...'.format(url))


    response = requests.request('GET', url, headers=headers, params=url_params)


    return response.json()


def search(api_key, term, location):

    """Query the Search API by a search term and location.

    Args:

        term (str): The search term passed to the API.

        location (str): The search location passed to the API.



    Returns:

        dict: The JSON response from the request.

    """

    url_params = {

        'term': term.replace(' ', '+'),

        'location': location.replace(' ', '+'),

        'limit': SEARCH_LIMIT

    }

    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):

    """Query the Business API by a business ID.

    Args:

        business_id (str): The ID of the business to query.


    Returns:

        dict: The JSON response from the request.

    """

    business_path = BUSINESS_PATH + business_id


    return request(API_HOST, business_path, api_key)


def query_api(term, location):

    """Queries the API by the input values from the user.


    Args:

        term (str): The search term to query.

        location (str): The location of the business to query.

    """

    response = search(API_KEY, term, location)

#Judy Note: Yelp returns the top 50 Washingon DC businesses in JSON format

    businesses = response.get('businesses')

    if not businesses:

        print(u'No businesses for {0} in {1} found.'.format(term, location))

        return

    pprint.pprint(response, indent=2)

#Judy Note: This connects to Judy's Postgres database that I called "blockwise" for my prototye/draft purposes; edit the string for your PG db name, user, PW    
    con = None

    con = psycopg2.connect("dbname='blockwise' user='postgres' password='purplerain'")   
    
    cur = con.cursor()

#Judy Note: I added code to this loop to print each business record returned by Yelp to the console, parse the house number and street name, and load records into PostgreSQL

    for business in businesses:

#Judy Note: In the loop thru businesses, print business name and location for each Yelp business to the console
        print(business['name'] + ', ' + str(business['rating']))
        print(business['location']['address1'])
        print(business['id'])

#Judy Note: In the loop thru businesses, save the JSON for each Yelp business to a JSON file named with the business ID
        with open(business['id'] + 'data.json', 'wb') as f:
           json.dump(response, codecs.getwriter('utf-8')(f), ensure_ascii=False)

#Judy Note: In the loop thru businesses, split the address house number from the street name and put all Yelp info to save in Postgres into variables
        split_string = business['location']['address1'].split(' ',1) 
        street_name = split_string[1]
        house_number = split_string[0]
        address = business['location']['address1']
        business = business['name']
        loc_id = business['id']
        s_rank = '0'
        s_review_count = '0'
        s_rating = '0'

#Judy Note: In the loop thru businesses, insert data into PG table; in FUTURE, add a field for "location_source" here and in PG DB, e.g., Yelp for this data; but we could have other data sources and their corresponding ID in the location _id
        SQL = "INSERT INTO blockadvisor_location(location_id, business_name, address, street_number, street_name, rank, review_count, rating)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(SQL, (loc_id, business, address, house_number, street_name, s_rank, s_review_count, s_rating))
        con.commit()

#Judy Note: Outside of the business loop, close the PG db connection after finishing the loop through businesses
    con.close()

#Judy Note: Back to original Yelp sample script code 
    business_id = businesses[0]['id']


    print(u'{0} businesses found, querying business info ' \

        'for the top result "{1}" ...'.format(

            len(businesses), business_id))

    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))

    #pprint.pprint(response, indent=2)


def main():

    parser = argparse.ArgumentParser()



    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,

                        type=str, help='Search term (default: %(default)s)')

    parser.add_argument('-l', '--location', dest='location',

                        default=DEFAULT_LOCATION, type=str,

                        help='Search location (default: %(default)s)')



    input_values = parser.parse_args()



    try:

        query_api(input_values.term, input_values.location)

    except HTTPError as error:

        sys.exit(

            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(

                error.code,

                error.url,

                error.read(),

            )

        )





if __name__ == '__main__':

    main()