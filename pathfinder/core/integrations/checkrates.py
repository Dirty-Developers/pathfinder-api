from json import dumps
from hashlib import sha256
from requests import post, HTTPError
from time import time

apikey = 'hebajhkc4jj2mvd5tsjzqsss'
secret = 'SpkwyeghW3'
base_uri = 'https://api.test.hotelbeds.com/hotel-api/1.0/'
operation = 'checkrates'
headers = {
    'Api-Key': apikey,
    'Accept': 'application/json',
    'Content-Type': 'application/json; encoding=utf-8'
}

def get_rooms(ratekey):
    rooms = {"rateKey": ratekey}
    return rooms


def get_checkrate_rq(ratekey):
    request = {"language": "ENG",
               "upselling": "False",
               "rooms": [get_rooms(ratekey)]}
    print(request)
    return request
