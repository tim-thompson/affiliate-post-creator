from amazon.api import AmazonAPI
import requests, json, sys

# Load Config
post_def = sys.argv[1]
key_def = sys.argv[2]

with open(key_def) as key_file:
    key_data = json.load(key_file)

# API Keys
AMAZON_ACCESS_KEY = key_data['amazon_access']
AMAZON_SECRET_KEY = key_data['amazon_secret']
AMAZON_ASSOC_TAG = key_data['amazon_assoc']

GENIUS_ACCESS_KEY = key_data['genius_access']
GENIUS_SECRET_KEY = key_data['genius_secret']

# API Setup
print ('Connecting to Amazon API...')
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region='UK')
print ('Connected to Amazon API')

# Load Post Definition
with open(post_def) as post_file:
    post_data = json.load(post_file)

# Set geni.us headers
headers = {'X-Api-Key': GENIUS_ACCESS_KEY,
           'X-Api-Secret': GENIUS_SECRET_KEY,
           'Content-Type': 'application/json'}

# Construct Post
intro = '<' + post_data['title_tag'] + '>' + post_data['intro_title'] + '</' + post_data['title_tag'] + '>'
intro = intro + '<p>' + post_data['intro_copy'] + '</p>'
products = ''

print ('Looping through products...')
for product in post_data['products']:
    # Generate genius link
    print ('Creating geni.us link...')
    payload = {'Url': product['affiliate_link'], 'GroupId': '24142'}
    r = requests.post('https://api.geni.us/v2/shorturl', headers=headers, params=payload)
    link_json = json.loads(r.text)
    link = link_json['NewLink']
    print ('Created geni.us link')

    # Get Amazon Image
    print ('Getting Amazon image link...')
    amazon_product = amazon.lookup(ItemId=product['asin'])
    image_link = amazon_product.large_image_url
    print ('Amazon image link retrieved')

    products = products + '<' + post_data['title_tag'] + '>'
    products = products + '<a rel="nofollow" target="_blank" href="' + link + '">'
    products = products + product['title'] + '</a></' + post_data['title_tag'] + '>'
    products = products + '<p><a rel="nofollow" target="_blank" href="' + link + '">'
    products = products + '<img class="aligncenter" src="' + image_link + '" alt="' + product['title'] + '" /></a></p>'
    products = products + '<p>' + product['copy'] + '</p>'
    products = products + '<p style="text-align: center;"><a rel="nofollow" target="_blank" href="' + link + '">' + post_data['buy_button'] + '</a></p>'

conclusion = '<' + post_data['title_tag'] + '>' + post_data['conclusion_title'] + '</' + post_data['title_tag'] + '>'
conclusion = conclusion + '<p>' + post_data['conclusion_copy'] + '</p>'

# Write HTML to file
filename = post_def.split('.')[0]
html = open(filename + '.html', 'w')
html.write(intro + products + conclusion)
html.close()

print (intro + products + conclusion)
