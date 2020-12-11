import time
import hmac
import hashlib
import requests
from pprint import pprint
'''
All private API requires 3 authentication parameters and zero or more API specific parameters.
    access_key  Your access key.
    tonce       tonce is a timestamp in integer, stands for milliseconds elapsed since Unix epoch.
                Tonce must be within 30 seconds of server's current time. Each tonce can only be used once.
    signature   Signature of the API request, generated by you, use your secret key.

if it useful you can make a donation
GIO: GQksGKKU6PotrByC8hQzBRwMAN7FuMNugF
ETH: 0x290fE67efA690AE7924DB416d4239daC9c309b97
'''
DEBUG = True

# your API keys
access_key = ''
secret_key = b''

tonce = int(time.time()) * 1000

if DEBUG:
    print(f'tonce: {tonce}')

# the request query sorted in alphabetic order, including access_key and tonce,
# e.g. access_key=xxx&foo=bar&tonce=123456789
request = f'access_key={access_key}&tonce={tonce}'

# HTTP verb like GET/POST in uppercase
verb = 'GET'

# request path like /webapi/v3/markets
uri = '/webapi/v3/deposits'

# The combined string looks like: GET|/webapi/v3/markets|access_key=xxx&foo=bar&tonce=123456789
message = f'{verb}|{uri}|{request}'

if DEBUG:
    print(f'request: {request}\nmessage: {message}')

signature = hmac.new(
    secret_key,
    message.encode(),
    hashlib.sha256
).hexdigest()

if DEBUG:
    print(f'signature: {signature}')

query = f'https://graviex.net{uri}?{request}&signature={signature}'
response = requests.get(query)

if DEBUG:
    print(f'query: {query}\nresponse: {response}')

content = response.json()
pprint(f'content: {content}')