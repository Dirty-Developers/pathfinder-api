from core.integrations import hbgactivity
from datetime import date, timedelta
from requests import HTTPError
from random import random
import logging as log
import math


def get_activities_path(origin, destination, checkin, checkout):
    pool = []
    gotten = []
    for point in __get_middle_points(origin, destination):
        rs = None
        try:
            rs = hbgactivity.search_by_geolocation(checkin, checkout, longitude=point[0], latitude=point[1])
        except HTTPError:
            log.warning("Error getting activities at point {}".format(point))

        for hbgact in rs:
            if hbgact['code'] not in gotten:
                gotten.append(hbgact['code'])
                pool.append(__map_activity(hbgact, checkin, checkout, point))
    return pool


def __map_activity(hbgact, checkin, checkout, point):
    content = hbgact.get("content", __build_content(point))
    geo = __build_geolocation(point)

    act = {
        'id': hbgact['code'],
        'name': hbgact['name'],
        'lon': content.get('geolocation', geo)['longitude'],
        'lat': content.get('geolocation', geo)['latitude'],
        'description': content['description'],
        'avail': [x for x in __build_avails(hbgact, checkin, checkout)],
        'tags': []
    }

    try:
        act['photo'] = content['media']['images'][0]['urls'][0]['resource']
    except KeyError:
        act['photo'] = ""

    try:
        act['address'] = content['location']['startingPoints'][0]['meetingPoint']['address']
    except KeyError:
        act['address'] = ""

    return act


def __build_geolocation(point):
    r = random()
    alpha = 2 * math.pi * random()
    lon = r * math.cos(alpha) + point[0]
    lat = r * math.sin(alpha) + point[1]
    return {
        'longitude': lon,
        'latitude': lat,
    }


def __build_content(point):
    return {
        'geolocation': __build_geolocation(point),
        'description': "",
    }


def __build_avails(hbgact, checkin, checkout):
    for n in range(int((checkout - checkin).days)+1):
        avail = {
            'time': '',
            'date': (checkin + timedelta(n)).strftime("%d-%m-%Y"),
            'price': list(filter(lambda x: x['paxType'] == 'ADULT', hbgact['amountsFrom']))[0]['amount']
        }
        yield avail


def __calc_unit_vector(vector):
    m = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return tuple(x/m for x in vector)


def __get_middle_points(origin, destination):
    u_vector = __calc_unit_vector((destination[0] - origin[0], destination[1] - origin[1]))
    d = __calc_distance(origin, destination)
    p = origin
    yield p
    while __calc_distance(origin, (p[0]+u_vector[0], p[1]+u_vector[1])) < d:
        p = (p[0]+u_vector[0], p[1]+u_vector[1])
        yield p
    yield destination


def __calc_distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


if __name__ == '__main__':
    checkin = date(2018, 6, 12)
    checkout = date(2018, 6, 14)

    mallorca = (3.0350702, 39.6104161)
    mallorca2 = (mallorca[0]-0.00001, mallorca[1]-0.00001)

    origin = (-4.305273, 39.750537)
    destination = (2.491839, 49.113252)
    activities = get_activities_path(origin, destination, checkin, checkout)
    print(len(activities))
