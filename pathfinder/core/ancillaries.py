from integrations.apitude import get_hotels_by_radio
from integrations.yelp import search
from datetime import date, datetime,timedelta

inDate = datetime.strptime('20180501', "%Y%m%d").date()
outDate = datetime.strptime('20180503', "%Y%m%d").date()


def format_daily_rates(daily_rates, checkin: date):
    refined_daily_rates = []
    aux_date = checkin
    for daily_rate in daily_rates:
        aux_date += timedelta(days=1)
        daily_avail = {
            "date": aux_date.strftime("%Y-%m-%d"),
            "price": daily_rate['dailyNet']
        }
        refined_daily_rates.append(daily_avail)
    return refined_daily_rates


def format_hotels(hotels_rs, checkin: date):
    refined_hotels = []
    if hotels_rs['hotels']['total'] == 0:
        return refined_hotels
    raw_hotels = hotels_rs['hotels']['hotels']
    for hotel in raw_hotels:
        refined_hotel = {
            "id": hotel['code'],
            "name": hotel['name'],
            "longitude": hotel['longitude'],
            "latitude": hotel['latitude'],
            "avail": [format_daily_rates(hotel['rooms'][0]['rates'][0]['dailyRates'], checkin)]
        }
        refined_hotels.append(refined_hotel)
    return refined_hotels


def format_tags(raw_tags):
    refined_tags = []
    for tag in raw_tags:
        refined_tags.append(tag['alias'])
    return refined_tags


def format_restaurants(restaurants_rs):
    refined_restaurants = []
    if restaurants_rs['total'] == 0:
        return refined_restaurants
    raw_restaurants = restaurants_rs['businesses']
    for restaurant in raw_restaurants:
        refined_restaurant = {
            "id": restaurant['id'],
            "name": restaurant['name'],
            "longitude": restaurant['coordinates']['longitude'],
            "latitude": restaurant['coordinates']['latitude'],
            "description": restaurant['url'],
            "address": restaurant['location']['address1'],
            "photo": restaurant['image_url'],
            "tags": format_tags(restaurant['categories'])
        }
        refined_restaurants.append(refined_restaurant)
    return refined_restaurants


def get_ancillaries(lon, lat, checkin: date, checkout: date):
    hotels = get_hotels_by_radio(lon, lat, 30, 'km', checkin, checkout)

    restaurants = search(longitude=lon, latitude=lat)

    ancillaries = {
        "hotels": format_hotels(hotels, checkin),
        "restaurants": format_restaurants(restaurants)
    }
    return ancillaries


# print("first try")
# print(get_ancillaries(1, 1, inDate, outDate))
# print("second try")
# print(get_ancillaries(-3.703364, 40.416691, inDate, outDate))
