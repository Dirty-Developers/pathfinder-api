# https://api.test.hotelbeds.com/hotel-api/swagger/index.html#!/hotels/availability
from enum import Enum
from datetime import date, datetime


class PaxTypes(Enum):
    Adult = 'AD'
    Children = 'CH'


def get_debug(allow_destination):
    debug = {"allowDestinationSearch": allow_destination}
    return debug


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


def get_occupancy(age, name, surname):
    occupancy = {"rooms": 1,
                 "adults": 1,
                 "children": 0,
                 "pax": [get_pax(age, name, surname)]}
    return occupancy


def get_stay(checkin: date, checkout: date):
    stay = {"checkIn": checkin.strftime("%Y-%m-%d"),
            "checkOut": checkout.strftime("%Y-%m-%d")}
    return stay


def get_destination(destination):
    destination = {"code": destination}
    return destination


def get_geolocation(longitude, latitude, radius, unit='km'):
    geolocation = {"longitude": longitude,
                   "latitude": latitude,
                   "radius": radius,
                   "unit": unit}
    return geolocation


def get_availability_rq(checkin: date, checkout: date, age=900, name='Diego', surname='Farras', daily_rate=False):
    request = {"dailyRate": daily_rate,
                     "language": "ENG",
                     "stay": get_stay(checkin, checkout),
                     "occupancies": [get_occupancy(age, name, surname)]}
    return request


inDate = datetime.strptime('20180501', "%Y%m%d").date()
outDate = datetime.strptime('20180503', "%Y%m%d").date()
code = 'BCN'
sourceMarket = 'ES'


def get_geolocation_rq(longitude, latitude, radio, unit, checkin: date, checkout: date, age=900, name='Diego', surname='Farras', daily_rate=False):
    request = get_availability_rq(checkin, checkout, age, name, surname, daily_rate)
    request["geolocation"] = get_geolocation(longitude, latitude, radio, unit)
    return request


def get_destination_rq(destination, checkin: date, checkout: date, age=900, name='Diego', surname='Farras', daily_rate=False):
    request = get_availability_rq(checkin, checkout, age, name, surname, daily_rate)
    request["destination"] = get_destination(destination)
    request["debug"] = get_debug("True")
    return request
