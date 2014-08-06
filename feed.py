import oauth2 as oauth
import json
import re
import os.path

import config

consumer = oauth.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)
access_token = oauth.Token(key=config.ACCESS_KEY, secret=config.ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

timeline_endpoint = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

url_pattern = ''

response, data = client.request(timeline_endpoint)

tweets = json.loads(data)

url_candidates = []

def store_contract_info(data_dir, pub1, pub2, fact_id, curr):
    # for now we're only interested in pub2, which is the charity    
    # in theory we might want to write this to a file for pub1 as well in case the user loses their local storage list.
    contract = pub1 + '-' + pub2 + '-' + fact_id + '-' + curr
    #print "storing contract %s" % (contract)
    fname = data_dir + '/' + pub2 + '.txt'
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            for line in f:
                #print "chek "+line
                if line.rstrip("\n") == contract:
                    return True
                #print "line :%s: not match :%s:" % (line, contract)
    with open(fname, 'a') as fa:
        fa.write(contract + "\n")

    return True

for tweet in tweets:
    url_candidate = None
    if 'entities' not in tweet:
        continue
    if 'urls' not in tweet['entities']:
        continue
    for url in tweet['entities']['urls']:
        if 'expanded_url' in url:
            url_candidate = url['expanded_url']
        elif 'url' in url:
            url_candidate = url['url']
        else:
            continue
    url_candidates.append(url_candidate)

for uc in url_candidates:
    m = re.match('^.*?\#([a-f0-9]{66})\-([a-f0-9]{66})\-(\d+)\-(t?btc)$', uc)
    if m is None:
        continue
    pub1 = m.group(1)
    pub2 = m.group(2)
    fact_id = m.group(3)
    curr = m.group(4)
    store_contract_info(config.DATA_DIR, pub1, pub2, fact_id, curr);

