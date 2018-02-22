from json import dumps
from hashlib import sha256
from requests import post, HTTPError
from time import time
from availability import PaxTypes

apikey = 'hebajhkc4jj2mvd5tsjzqsss'
secret = 'SpkwyeghW3'
base_uri = 'https://api.test.hotelbeds.com/hotel-api/1.0/'
operation = 'bookings'
headers = {
    'Api-Key': apikey,
    'Accept': 'application/json',
    'Content-Type': 'application/json; encoding=utf-8'
}


def get_pax_age(age):
    if age > 110:
        age = 28
    return age


def get_pax(age, name, surname):
    pax = {"roomId": 1,
           "type": PaxTypes.Adult.value,
           "age": get_pax_age(age),
           "name": name,
           "surname": surname}
    return pax


def get_confirm_rq(ratekey, age, name, surname):
    request = {"holder": {"name": name,
                          "surname": surname
                          },
               "rooms": [{
                   "rateKey": ratekey,
                   "paxes": [{"roomId": "1",
                              "type": PaxTypes.Adult.value,
                              "name": name,
                              "surname": surname
                              }]
               }],
               "clientReference": "dFarras"
               }
    return request
