from os import environ
from time import time, sleep
from json import dumps
from hashlib import sha256
from requests import post, HTTPError
from datetime import date
from threading import Lock

APIKEY = environ['HOTELAPI_KEY']
SECRET = environ['HOTELAPI_SECRET']

BASE_URI = 'https://api.test.hotelbeds.com/activity-api/3.0/'
HEADERS = {
            'Api-Key': APIKEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json; encoding=utf-8'
           }
ITEMS_PER_PAGE = 25

__lock = Lock()
__timestamp = 0
__index = 0


def __wait_for_qps():
    global __index
    __index = (__index + 1) % 2
    if __index == 0:
        global __timestamp
        time_diff = time() - __timestamp
        if time_diff <= 1:
            sleep(time_diff)
        __timestamp = time()


def __send_post(path, data):
    with __lock:
        __wait_for_qps()
        raw_sig = "{}{}{}".format(APIKEY, SECRET, int(time()))
        signature = sha256(raw_sig.encode('utf-8')).hexdigest()
        head = {**HEADERS}
        head['X-Signature'] = signature

        response = post("/".join([BASE_URI, path]), headers=head, data=dumps(data))

    if response.status_code != 200:
        raise HTTPError("hbgactivity response code: [{}] {}".format(response.status_code, response.text))

    parsed_rs = response.json()
    if 'errors' in parsed_rs:
        raise HTTPError("hbgactivity response with errors: {}".format(parsed_rs['errors'][0]['text']))

    return parsed_rs


def __search_request(from_date, to_date, filters, page=1):
    rq = {
        "from": from_date.strftime("%Y-%m-%d"),
        "to": to_date.strftime("%Y-%m-%d"),
        "filters": [{"searchFilterItems": filters}],
        "pagination": {
            "itemsPerPage": ITEMS_PER_PAGE,
            "page": page
        },
        "order": "DEFAULT"
    }

    return __send_post('activities', rq)


def search_by_destination(from_date, to_date, destination, page=1):
    f = [{"type": "destination", "value": destination}]
    return __search_request(from_date, to_date, f, page)['activities']


def search_by_geolocation(from_date, to_date, longitude, latitude, page=1):
    f = [{"type": "gps", "longitude": longitude, "latitude": latitude}]
    return __search_request(from_date, to_date, f, page)['activities']


if __name__ == '__main__':
    fdate = date(2018, 6, 14)
    tdate = date(2018, 6, 16)

    rs = search_by_destination(fdate, tdate, "PMI")
    print(rs)
    print("DONE")

    rs = search_by_geolocation(fdate, tdate, longitude=2.938843, latitude=39.604432)
    print("DONE")
