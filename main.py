from amazon.api import AmazonAPI
import requests
import json
import sys

# API Keys
AMAZON_ACCESS_KEY = ""
AMAZON_SECRET_KEY = ""
AMAZON_ASSOC_TAG = ""

GENIUS_ACCESS_KEY = ""
GENIUS_SECRET_KEY = ""

# API Setup
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

# Load Post Definition
post_def = sys.argv[1]

with open(post_def) as post_file:
    post_data = json.load(post_file)

# Set geni.us headers
headers = {'X-Api-Key': GENIUS_ACCESS_KEY,
           'X-Api-Secret': GENIUS_SECRET_KEY}

# Construct Post
intro = '<' + post_data['title_tag'] + '>' + post_data['intro_title'] + '</' + post_data['title_tag'] + '>'
products = ''

for product in post_data['products']:
    payload = {'Url': product['affiliate_link'], 'GroupId': '24142'}
    r = requests.post('https://api.geni.us/v2/shorturl', headers=headers)
    link_json = json.load(r.text)
    link = link_json['NewLink']

    products = products + '<a rel="nofollow" target="_blank" href="' + link + '">'
    products = products + '<' + post_data['title_tag'] + '>' + product['title'] + '</' + post_data['title_tag'] + '>'
    products = products + '</a>'