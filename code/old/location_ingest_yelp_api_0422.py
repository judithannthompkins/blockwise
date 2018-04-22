# -*- coding: utf-8 -*-

"""

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

import datetime

from pyparsing import *

from decimal import Decimal



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


# Defaults for our simple example.

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


    businesses = response.get('businesses')


    if not businesses:

        print(u'No businesses for {0} in {1} found.'.format(term, location))

        return


#    pprint.pprint(response, indent=2)

#Judy Note: This connects to Judy's Postgres database that I called "blockwise" for now; edit for your database name
    con = None

    con = psycopg2.connect("dbname='blockwise' user='postgres' password='purplerain'")

    cur = con.cursor()

#Judy Note: I added this loop to print each business record returned by Yelp to the console, parse the house number and street name, and load records into PostgreSQL
    now = datetime.datetime.now()
    jsonfile = str(now.year) + str(now.month) + str(now.day)

    #Judy Note: Save the JSON for each Yelp business to a JSON file named with the business ID
    with open(jsonfile + 'yelp50.json', 'wb') as f:


        for business in businesses:

            #Judy Note: Print business name and location for each Yelp business to the console
     #       print(business['id'])
            print(business['name'] + ', ' + str(business['rating']))
     #       print(business['location']['address1'])

            json.dump(response, codecs.getwriter('utf-8')(f), ensure_ascii=False)

            #Judy Note:
            split_string = business['location']['address1'].split(' ',1)
            #street_name = normalizeStreetSuffixes(split_string[1]).lower()   #Judy added street suffix normalization, e.g., "Street" to "St" on 0418
            street_name = split_string[1].lower()   #Judy added street suffix normalization, e.g., "Street" to "St" on 0418
            house_number = split_string[0]
            #Code to eliminate numbers from house numbers so can match to block street number ranges
            house_number_no_char = ''.join([i for i in house_number if i.isdigit()])     

            address = business['location']['address1']
            business_name = business['name']

            #loc_id = '500000'  #need to change this to the business ID; program didn't with business['id'] here for some reason to figure out later
            loc_id = business['id']  #need to change this to the business ID; program didn't with business['id'] here for some reason to figure out later
            review_count = business['review_count']
            #s_rating = '0'
            rating = Decimal(business['rating'])
            #Judy need to insert into location categories table
            categories = ""
            for x in business['categories']:
                print(x['title'])
                s_category = x['title']
                categories = categories + ' * ' + x['title']

            lati = float(business['coordinates']['latitude'])
            longi = float(business['coordinates']['longitude'])
            s_lati = str(business['coordinates']['latitude'])
            s_longi = str(business['coordinates']['longitude'])
            coord = s_lati + "," + s_longi

            phone = business['display_phone']
            #print(phone)
            image_url = business['image_url']
            #print(image_url)
            url = business['url']
            #print(url)
            zip = business['location']['zip_code']
            #print(zip)
            city = business['location']['city']
            #print(city)
            state = business['location']['state']
            #print(state)
            country = business['location']['country']
            #print(country)

            #Judy Note:  May need to add test for the keys. For example, price did not appear in all businesses and caused an error for a business (Napoli_ without it

            SQL = "INSERT INTO blockadvisor_location(location_id, business_name, address, street_number, street_name, review_count, rating, categories, latitude, longitude, coordinates, phone, image_url, url, zip_code, city, state, country)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            cur.execute(SQL, (loc_id, business_name, address, house_number_no_char, street_name, review_count, rating, categories, lati, longi, coord, phone, image_url, url, zip, city, state, country))
            con.commit()

            inserted_id = cur.fetchone()[0]
            print('inserted: ' + str(inserted_id))

            for x in business['categories']:
                s_category = x['title']
                SQL = "INSERT INTO blockadvisor_location_categories(blockadvisor_location_id, category)  VALUES (%s, %s);"
                cur.execute(SQL, (inserted_id, s_category))
                con.commit()

    con.close()

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \

        'for the top result "{1}" ...'.format(

            len(businesses), business_id))

    response = get_business(API_KEY, business_id)

    con.close()

    print(u'Result for business "{0}" found:'.format(business_id))

    #pprint.pprint(response, indent=2)

def normalizeStreetSuffixes(inputValue,case='l'):
        '''
        if case=='l', returns lowercase
        if case=='u', returns uppercase
        else returns proper case
        '''
        case = case[0].lower()
        abbv = suffixDict()
        words = inputValue.split()
        for i,word in enumerate(words):
            w = word.lower()
            rep = abbv[w] if w in abbv.keys() else words[i]
            words[i] = rep.upper() if case == 'u' else rep.lower() if case == 'l' else (rep[0].upper() + rep[1:])
        return ' '.join(words)

def suffixDict():
    """
    Use common abbreviations -> USPS standardized abbreviation to replace common street suffixes

    Obtains list from https://www.usps.com/send/official-abbreviations.htm
    """
    return {'trpk': 'tpke', 'forges': 'frgs', 'bypas': 'byp', 'mnr': 'mnr', 'viaduct': 'via', 'mnt': 'mt',
            'lndng': 'lndg', 'vill': 'vlg', 'aly': 'aly', 'mill': 'ml', 'pts': 'pts', 'centers': 'ctrs', 'row': 'row', 'cnter': 'ctr',
            'hrbor': 'hbr', 'tr': 'trl', 'lndg': 'lndg', 'passage': 'psge', 'walks': 'walk', 'frks': 'frks', 'crest': 'crst', 'meadows': 'mdws',
            'freewy': 'fwy', 'garden': 'gdn', 'bluffs': 'blfs', 'vlg': 'vlg', 'vly': 'vly', 'fall': 'fall', 'trk': 'trak', 'squares': 'sqs',
            'trl': 'trl', 'harbor': 'hbr', 'frry': 'fry', 'div': 'dv', 'straven': 'stra', 'cmp': 'cp', 'grdns': 'gdns', 'villg': 'vlg',
            'meadow': 'mdw', 'trails': 'trl', 'streets': 'sts', 'prairie': 'pr', 'hts': 'hts', 'crescent': 'cres', 'pass': 'pass',
            'ter': 'ter', 'port': 'prt', 'bluf': 'blf', 'avnue': 'ave', 'lights': 'lgts', 'rpds': 'rpds', 'harbors': 'hbrs',
            'mews': 'mews', 'lodg': 'ldg', 'plz': 'plz', 'tracks': 'trak', 'path': 'path', 'pkway': 'pkwy', 'gln': 'gln',
            'bot': 'btm', 'drv': 'dr', 'rdg': 'rdg', 'fwy': 'fwy', 'hbr': 'hbr', 'via': 'via', 'divide': 'dv', 'inlt': 'inlt',
            'fords': 'frds', 'avenu': 'ave', 'vis': 'vis', 'brk': 'brk', 'rivr': 'riv', 'oval': 'oval', 'gateway': 'gtwy',
            'stream': 'strm', 'bayoo': 'byu', 'msn': 'msn', 'knoll': 'knl', 'expressway': 'expy', 'sprng': 'spg',
            'flat': 'flt', 'holw': 'holw', 'grden': 'gdn', 'trail': 'trl', 'jctns': 'jcts', 'rdgs': 'rdgs',
            'tunnel': 'tunl', 'ml': 'ml', 'fls': 'fls', 'flt': 'flt', 'lks': 'lks', 'mt': 'mt', 'groves': 'grvs',
            'vally': 'vly', 'ferry': 'fry', 'parkway': 'pkwy', 'radiel': 'radl', 'strvnue': 'stra', 'fld': 'fld',
            'overpass': 'opas', 'plaza': 'plz', 'estate': 'est', 'mntn': 'mtn', 'lock': 'lck', 'orchrd': 'orch',
            'strvn': 'stra', 'locks': 'lcks', 'bend': 'bnd', 'kys': 'kys', 'junctions': 'jcts', 'mountin': 'mtn',
            'burgs': 'bgs', 'pine': 'pne', 'ldge': 'ldg', 'causway': 'cswy', 'spg': 'spg', 'beach': 'bch', 'ft': 'ft',
            'crse': 'crse', 'motorway': 'mtwy', 'bluff': 'blf', 'court': 'ct', 'grov': 'grv', 'sprngs': 'spgs',
            'ovl': 'oval', 'villag': 'vlg', 'vdct': 'via', 'neck': 'nck', 'orchard': 'orch', 'light': 'lgt',
            'sq': 'sq', 'pkwy': 'pkwy', 'shore': 'shr', 'green': 'grn', 'strm': 'strm', 'islnd': 'is',
            'turnpike': 'tpke', 'stra': 'stra', 'mission': 'msn', 'spngs': 'spgs', 'course': 'crse',
            'trafficway': 'trfy', 'terrace': 'ter', 'hway': 'hwy', 'avenue': 'ave', 'glen': 'gln',
            'boul': 'blvd', 'inlet': 'inlt', 'la': 'ln', 'ln': 'ln', 'frst': 'frst', 'clf': 'clf',
            'cres': 'cres', 'brook': 'brk', 'lk': 'lk', 'byp': 'byp', 'shoar': 'shr', 'bypass': 'byp',
            'mtin': 'mtn', 'ally': 'aly', 'forest': 'frst', 'junction': 'jct', 'views': 'vws', 'wells': 'wls', 'cen': 'ctr',
            'exts': 'exts', 'crt': 'ct', 'corners': 'cors', 'trak': 'trak', 'frway': 'fwy', 'prarie': 'pr', 'crossing': 'xing',
            'extn': 'ext', 'cliffs': 'clfs', 'manors': 'mnrs', 'ports': 'prts', 'gatewy': 'gtwy', 'square': 'sq', 'hls': 'hls',
            'harb': 'hbr', 'loops': 'loop', 'mdw': 'mdw', 'smt': 'smt', 'rd': 'rd', 'hill': 'hl', 'blf': 'blf',
            'highway': 'hwy', 'walk': 'walk', 'clfs': 'clfs', 'brooks': 'brks', 'brnch': 'br', 'aven': 'ave',
            'shores': 'shrs', 'iss': 'iss', 'route': 'rte', 'wls': 'wls', 'place': 'pl', 'sumit': 'smt', 'pines': 'pnes',
            'trks': 'trak', 'shoal': 'shl', 'strt': 'st', 'frwy': 'fwy', 'heights': 'hts', 'ranches': 'rnch',
            'boulevard': 'blvd', 'extnsn': 'ext', 'mdws': 'mdws', 'hollows': 'holw', 'vsta': 'vis', 'plains': 'plns',
            'station': 'sta', 'circl': 'cir', 'mntns': 'mtns', 'prts': 'prts', 'shls': 'shls', 'villages': 'vlgs',
            'park': 'park', 'nck': 'nck', 'rst': 'rst', 'haven': 'hvn', 'turnpk': 'tpke', 'expy': 'expy', 'sta': 'sta',
            'expr': 'expy', 'stn': 'sta', 'expw': 'expy', 'street': 'st', 'str': 'st', 'spurs': 'spur', 'crecent': 'cres',
            'rad': 'radl', 'ranch': 'rnch', 'well': 'wl', 'shoals': 'shls', 'alley': 'aly', 'plza': 'plz', 'medows': 'mdws',
            'allee': 'aly', 'knls': 'knls', 'ests': 'ests', 'st': 'st', 'anx': 'anx', 'havn': 'hvn', 'paths': 'path', 'bypa': 'byp',
            'spgs': 'spgs', 'mills': 'mls', 'parks': 'park', 'byps': 'byp', 'flts': 'flts', 'tunnels': 'tunl', 'club': 'clb', 'sqrs': 'sqs',
            'hllw': 'holw', 'manor': 'mnr', 'centre': 'ctr', 'track': 'trak', 'hgts': 'hts', 'rnch': 'rnch', 'crcle': 'cir', 'falls': 'fls',
            'landing': 'lndg', 'plaines': 'plns', 'viadct': 'via', 'gdns': 'gdns', 'gtwy': 'gtwy', 'grove': 'grv', 'camp': 'cp', 'tpk': 'tpke',
            'drive': 'dr', 'freeway': 'fwy', 'ext': 'ext', 'points': 'pts', 'exp': 'expy', 'ky': 'ky', 'courts': 'cts', 'pky': 'pkwy', 'corner': 'cor',
            'crssing': 'xing', 'mnrs': 'mnrs', 'unions': 'uns', 'cyn': 'cyn', 'lodge': 'ldg', 'trfy': 'trfy', 'circle': 'cir', 'bridge': 'brg',
            'dl': 'dl', 'dm': 'dm', 'express': 'expy', 'tunls': 'tunl', 'dv': 'dv', 'dr': 'dr', 'shr': 'shr', 'knolls': 'knls', 'greens': 'grns',
            'tunel': 'tunl', 'fields': 'flds', 'common': 'cmn', 'orch': 'orch', 'crk': 'crk', 'river': 'riv', 'shl': 'shl', 'view': 'vw',
            'crsent': 'cres', 'rnchs': 'rnch', 'crscnt': 'cres', 'arc': 'arc', 'btm': 'btm', 'blvd': 'blvd', 'ways': 'ways', 'radl': 'radl',
            'rdge': 'rdg', 'causeway': 'cswy', 'parkwy': 'pkwy', 'juncton': 'jct', 'statn': 'sta', 'gardn': 'gdn', 'mntain': 'mtn',
            'crssng': 'xing', 'rapid': 'rpd', 'key': 'ky', 'plns': 'plns', 'wy': 'way', 'cor': 'cor', 'ramp': 'ramp', 'throughway': 'trwy',
            'estates': 'ests', 'ck': 'crk', 'loaf': 'lf', 'hvn': 'hvn', 'wall': 'wall', 'hollow': 'holw', 'canyon': 'cyn', 'clb': 'clb',
            'cswy': 'cswy', 'village': 'vlg', 'cr': 'crk', 'trce': 'trce', 'cp': 'cp', 'cv': 'cv', 'ct': 'cts', 'pr': 'pr', 'frg': 'frg',
            'jction': 'jct', 'pt': 'pt', 'mssn': 'msn', 'frk': 'frk', 'brdge': 'brg', 'cent': 'ctr', 'spur': 'spur', 'frt': 'ft', 'pk': 'park',
            'fry': 'fry', 'pl': 'pl', 'lanes': 'ln', 'gtway': 'gtwy', 'prk': 'park', 'vws': 'vws', 'stravenue': 'stra', 'lgt': 'lgt',
            'hiway': 'hwy', 'ctr': 'ctr', 'prt': 'prt', 'ville': 'vl', 'plain': 'pln', 'mount': 'mt', 'mls': 'mls', 'loop': 'loop',
            'riv': 'riv', 'centr': 'ctr', 'is': 'is', 'prr': 'pr', 'vl': 'vl', 'avn': 'ave', 'vw': 'vw', 'ave': 'ave', 'spng': 'spg',
            'hiwy': 'hwy', 'dam': 'dm', 'isle': 'isle', 'crcl': 'cir', 'sqre': 'sq', 'jct': 'jct', 'jctn': 'jct', 'mountain': 'mtn',
            'keys': 'kys', 'parkways': 'pkwy', 'drives': 'drs', 'tunl': 'tunl', 'jcts': 'jcts', 'knl': 'knl', 'center': 'ctr',
            'driv': 'dr', 'tpke': 'tpke', 'sumitt': 'smt', 'canyn': 'cyn', 'ldg': 'ldg', 'harbr': 'hbr', 'rest': 'rst', 'shoars': 'shrs',
            'vist': 'vis', 'gdn': 'gdn', 'islnds': 'iss', 'hills': 'hls', 'cresent': 'cres', 'point': 'pt', 'lake': 'lk', 'vlly': 'vly',
            'strav': 'stra', 'crossroad': 'xrd', 'bnd': 'bnd', 'strave': 'stra', 'stravn': 'stra', 'knol': 'knl', 'vlgs': 'vlgs',
            'forge': 'frg', 'cntr': 'ctr', 'cape': 'cpe', 'height': 'hts', 'lck': 'lck', 'highwy': 'hwy', 'trnpk': 'tpke', 'rpd': 'rpd',
            'boulv': 'blvd', 'circles': 'cirs', 'valleys': 'vlys', 'vst': 'vis', 'creek': 'crk', 'mall': 'mall', 'spring': 'spg',
            'brg': 'brg', 'holws': 'holw', 'lf': 'lf', 'est': 'est', 'xing': 'xing', 'trace': 'trce', 'bottom': 'btm',
            'streme': 'strm', 'isles': 'isle', 'circ': 'cir', 'forks': 'frks', 'burg': 'bg', 'run': 'run', 'trls': 'trl',
            'radial': 'radl', 'lakes': 'lks', 'rue': 'rue', 'vlys': 'vlys', 'br': 'br', 'cors': 'cors', 'pln': 'pln',
            'pike': 'pike', 'extension': 'ext', 'island': 'is', 'frd': 'frd', 'lcks': 'lcks', 'terr': 'ter',
            'union': 'un', 'extensions': 'exts', 'pkwys': 'pkwy', 'islands': 'iss', 'road': 'rd', 'shrs': 'shrs',
            'roads': 'rds', 'glens': 'glns', 'springs': 'spgs', 'missn': 'msn', 'ridge': 'rdg', 'arcade': 'arc',
            'bayou': 'byu', 'crsnt': 'cres', 'junctn': 'jct', 'way': 'way', 'valley': 'vly', 'fork': 'frk',
            'mountains': 'mtns', 'bottm': 'btm', 'forg': 'frg', 'ht': 'hts', 'ford': 'frd', 'hl': 'hl',
            'grdn': 'gdn', 'fort': 'ft', 'traces': 'trce', 'cnyn': 'cyn', 'cir': 'cir', 'un': 'un', 'mtn': 'mtn',
            'flats': 'flts', 'anex': 'anx', 'gatway': 'gtwy', 'rapids': 'rpds', 'villiage': 'vlg', 'flds': 'flds',
            'coves': 'cvs', 'rvr': 'riv', 'av': 'ave', 'pikes': 'pike', 'grv': 'grv', 'vista': 'vis', 'pnes': 'pnes',
            'forests': 'frst', 'field': 'fld', 'branch': 'br', 'grn': 'grn', 'dale': 'dl', 'rds': 'rds', 'annex': 'anx',
            'sqr': 'sq', 'cove': 'cv', 'squ': 'sq', 'skyway': 'skwy', 'ridges': 'rdgs', 'hwy': 'hwy', 'tunnl': 'tunl',
            'underpass': 'upas', 'cliff': 'clf', 'lane': 'ln', 'land': 'land', 'bch': 'bch', 'dvd': 'dv', 'curve': 'curv',
            'cpe': 'cpe', 'summit': 'smt', 'gardens': 'gdns'}

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
