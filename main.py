from amazon.api import AmazonAPI
import requests
import json
import sys

# Load Config
post_def = sys.argv[1]
key_def = sys.argv[2]

with open(key_def) as key_file:
    key_data = json.load(key_file)

# API Keys
AMAZON_ACCESS_KEY = key_data['amazon_access']
AMAZON_SECRET_KEY = key_data['amazon_secret']
AMAZON_ASSOC_TAG = "boagambea-21"

GENIUS_ACCESS_KEY = key_data['genius_access']
GENIUS_SECRET_KEY = key_data['genius_secret']

# API Setup
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region='UK')

# Load Post Definition
with open(post_def) as post_file:
    post_data = json.load(post_file)

# Set geni.us headers
headers = {'X-Api-Key': GENIUS_ACCESS_KEY,
           'X-Api-Secret': GENIUS_SECRET_KEY,
           'Content-Type': 'application/json'}

# Construct Post
intro = '<' + post_data['title_tag'] + '>' + post_data['intro_title'] + '</' + post_data['title_tag'] + '>'
intro = intro + post_data['intro_copy']
products = ''

for product in post_data['products']:
    # Generate genius link
    payload = {'Url': product['affiliate_link'], 'GroupId': '24142'}
    r = requests.post('https://api.geni.us/v2/shorturl', headers=headers, params=payload)
    link_json = json.loads(r.text)
    link = link_json['NewLink']

    # Get Amazon Image
    amazon_product = amazon.lookup(ItemId=product['asin'])
    image_link = amazon_product.large_image_url

    products = products + '<a rel="nofollow" target="_blank" href="' + link + '">'
    products = products + '<' + post_data['title_tag'] + '>' + product['title'] + '</' + post_data['title_tag'] + '>'
    products = products + '</a>'
    products = products + '<a rel="nofollow" target="_blank" href="' + link + '">'
    products = products + '<img src="' + image_link + '" alt="' + product['title'] + '" /></a>'
    products = products + product['copy']
    products = products + '<a rel="nofollow" target="_blank" href="' + link + '">' + post_data['buy_button'] + '</a>'

print (intro + products)
