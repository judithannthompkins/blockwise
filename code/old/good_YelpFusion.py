from yelpapi import YelpAPI

import argparse

from pprint import pprint



argparser = argparse.ArgumentParser(description='Example Yelp queries using yelpapi. '

                                                'Visit https://www.yelp.com/developers/v3/manage_app to get the '

                                                'necessary API keys.')

argparser.add_argument('api_key', type=str, help='Yelp Fusion API Key')

args = argparser.parse_args()



yelp_api = YelpAPI(args.api_key)



"""

    Example search by location text and term. 

    

    Search API: https://www.yelp.com/developers/documentation/v3/business_search

"""

print('***** 5 best rated restaurants in Washington, DC *****\n{}\n'.format("yelp_api.search_query(term='restaurants', "

                                                                             "location='washington, dc', sort_by='rating', "

                                                                             "limit=5)"))

response = yelp_api.search_query(term='restaurants', location='washington, dc', sort_by='rating', limit=5)

pprint(response)

print('\n-------------------------------------------------------------------------\n')

