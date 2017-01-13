from amazon.api import AmazonAPI
import requests
import json
import sys

# API Keys
AMAZON_ACCESS_KEY = "AKIAJC5VACJC5G4VQ5HA"
AMAZON_SECRET_KEY = "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"
AMAZON_ASSOC_TAG = "boagambea-21"

GENIUS_ACCESS_KEY = "37175a09a1eb4234b2b23e324dc3e0b5"
GENIUS_SECRET_KEY = "25635ed127034b3f9f5422f6c299fee2"

# API Setup
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

# Load Post Definition
post_def = sys.argv[1]

with open(post_def) as post_file:
    post_data = json.load(post_file)

# Set geni.us headers
headers = {'X-Api-Key': GENIUS_ACCESS_KEY,
           'X-Api-Secret': GENIUS_SECRET_KEY,
           'Content-Type': 'application/json'}

# Construct Post
intro = '<' + post_data['title_tag'] + '>' + post_data['intro_title'] + '</' + post_data['title_tag'] + '>'
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
    products = products + '<img src="' + image_link + '" alt="' + product['title'] + '" />'

    print (products)
