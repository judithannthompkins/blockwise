import psycopg2

import csv

def read_csv():

#Judy Note: This connects to Judy's Postgres database that I called "blockwise" for now; edit for your database name    
    con = None

    con = psycopg2.connect("dbname='blockwise' user='postgres' password='purplerain'")   
    
    cur = con.cursor()

#Judy Note: Loop through the crime data in the csv file, parse the block column, and load each record in Postgres

    with open('C:\\Users\\Judith\projects\\blockwise\data\\dc_crime2018423.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row.
        for row in reader:
            cluster=row[0]
            census=row[1] 
            og=row[2]
            longi=row[3] 
            endt=row[4]
            ot=row[5] 
            sh=row[6] 
            yb=row[7] 
            dist=row[8] 
            wd=row[9] 
            yr=row[10]
            ok=row[11]
            bd=row[12]
            sect=row[13]

            ps=row[14]
            ucr=row[15]
            bg=row[16]
            vp=row[17]
            xb=row[18]
            bl=row[19]
            sdt=row[20]
            cn=row[21]
            offe=row[22]
            ac=row[23]
            rdt=row[24] 
            meth=row[25] 
            loc=row[26] 
            lat=row[27] 

#Judy Note:  Use the block column to create three additional columns:  begining street number, end street number and street name so that the block-level crime data can be matched to the location street address
            #print(bl)
            bl_no_block = (bl.replace("block of ", ""))
            #print(bl_no_block)
            split_block = bl_no_block.split('-',1) 
            no1 = split_block[0]
            #print(no1)
            rest1 = split_block[-1].lstrip()
            #print(rest1)
            split_block2 = rest1.split(' ',1)
            no2 = split_block2[0]
            #print(no2)

#Judy Note: This changes Street to St in order to be consistent with street type abbreviations used in the Yelp street names so we can match the location and crime data
            street = normalizeStreetSuffixes(split_block2[-1])
            #print(street)

            SQL = "INSERT INTO blockadvisor_crime(neighborhood_cluster, census_tract, offense_group, longitude, end_date, offense_text, shift, yblock, district, ward, year, offense_key, bid, sector, psa, ucrrank, block_group, voting_precinct, xblock, block, block_street_name, block_street_number_begin, block_street_number_end, start_date, cnn, offense, anc, report_date, method, location, latitude)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

            cur.execute(SQL, (cluster, census, og, longi, endt, ot, sh, yb, dist, wd, yr, ok, bd, sect, ps, ucr, bg, vp, xb, bl, street, no1, no2, sdt, cn, offe, ac, rdt, meth, loc, lat))
            con.commit()


def normalizeStreetSuffixes(inputValue,case='l'):
    
#Judy Note:  I found this function line to turn street to st and similar postal abbreviations.
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


        read_csv()


if __name__ == '__main__':

    main()
