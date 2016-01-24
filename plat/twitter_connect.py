from apikeys import twitter_keys as keys
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from PIL import Image
from StringIO import StringIO
import json

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_BASE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'

TEST_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json'

def get_api_keys():
    print 'Go to Twitter Application Management and add your API keys'
    print 'https://apps.twitter.com/'
    print 'Add the following to plat/apikeys/twitter_keys.py:'
    print "CONSUMER_KEY = '(Consumer Key from Twitter)'"
    print "CONSUMER_SECRET = '(Consumer Secret from Twitter)'"
    exit()

def get_access_keys():
    
    #Request Token
    app_oauth = OAuth1(keys.CONSUMER_KEY, client_secret = keys.CONSUMER_SECRET)
    authorize_data = requests.post(url = REQUEST_TOKEN_URL, auth = app_oauth)
    authorize_credentials = parse_qs(authorize_data.content);
    authorize_key = authorize_credentials.get('oauth_token')[0]
    authorize_secret = authorize_credentials.get('oauth_token_secret')[0]

    #Authorize Token
    authorization_url = AUTHORIZE_BASE_URL + authorize_key
    print 'Authorize this application at: ' + authorization_url
    verify_pin = raw_input('Enter your verification pin: ')

    #Obtain Access Token
    access_token = OAuth1(keys.CONSUMER_KEY,
                          client_secret = keys.CONSUMER_SECRET,
                          resource_owner_key = authorize_key,
                          resource_owner_secret = authorize_secret,
                          verifier = verify_pin)
    access_data = requests.post(url = ACCESS_TOKEN_URL, auth = access_token)
    print access_data
    #Need to add error code handling
    if access_data.status_code == 200:
        access_credentials = parse_qs(access_data.content)
        access_token = access_credentials.get('oauth_token')[0]
        access_secret = access_credentials.get('oauth_token_secret')[0]
        print 'Add the following to plat/apikeys/twitter_keys.py:'
        print "ACCESS_KEY = '" + access_token + "'"
        print "ACCESS_SECRET = '" + access_secret + "'"
        exit()
    else:
        print 'Some sort of error'
        exit()

def get_oauth():
    if (not keys.CONSUMER_KEY or keys.CONSUMER_KEY == '' or
        not keys.CONSUMER_SECRET or keys.CONSUMER_SECRET == ''):
        get_api_keys()
    elif (not keys.ACCESS_KEY or keys.ACCESS_KEY == '' or
        not keys.ACCESS_SECRET or keys.ACCESS_SECRET == ''):
        get_access_keys()
    else:
        oauth = OAuth1(keys.CONSUMER_KEY,
                       client_secret = keys.CONSUMER_SECRET,
                       resource_owner_key = keys.ACCESS_KEY,
                       resource_owner_secret = keys.ACCESS_SECRET)
        return oauth

def post_status(status, media = None, oauth = None):
    if oauth == None:
        oauth = get_oauth()
    post_url = 'https://api.twitter.com/1.1/statuses/update.json'
    data = {'status' : status}
    if media != None:
        data['media_ids'] = media
    post_response = requests.post(url = post_url, data = data, auth = oauth)
    return post_response

def upload_media(filename, oauth = None):
    if oauth == None:
        oauth = get_oauth()
    post_url = 'https://upload.twitter.com/1.1/media/upload.json'
    datafile = open(filename, 'rb')
    data = {'media' : datafile}
    post_response = requests.post(url = post_url, files = data, auth = oauth)
    return post_response

def post_media(status, filename, oauth = None):
    if oauth == None:
        oauth = get_oauth()
    upload_response = upload_media(filename, oauth)
    media_id = json.loads(upload_response.content)['media_id_string']
    post_response = post_status(status, media_id, oauth)
    return post_response

def delete_media(status_id, oauth = None):
    if oauth == None:
        oauth = get_oauth()
    post_url_base = 'https://api.twitter.com/1.1/statuses/destroy/'
    post_url = post_url_base + status_id + '.json'
    post_response = requests.post(url = post_url, auth = oauth)
    return post_response

def download_media(imagename, url):
    image_response = requests.get(url)
    image_binary = Image.open(StringIO(image_response.content))
    image_binary.save(imagename)

def cycle_media(imagename, status, filename, delete = False, oauth = None):
    if oauth == None:
        oauth = get_oauth()
    status_response = post_media(status, filename, oauth)
    status_json = json.loads(status_response.content)
    image_url = status_json['entities']['media'][0]['media_url_https'] + ":large"
    download_media(imagename, image_url)
    if delete:
        delete_media(status_json['id_str'], oauth)
    
if __name__ == '__main__':
    oauth = get_oauth()
    test_request = requests.get(url = TEST_URL, auth = oauth)
    if test_request.status_code == 200:
        print 'Success'
    else:
        print 'Failed'
