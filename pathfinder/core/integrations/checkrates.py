
def get_rooms(ratekey):
    rooms = {"rateKey": ratekey}
    return rooms


def get_checkrate_rq(ratekey):
    request = {"language": "ENG",
               "upselling": "False",
               "rooms": [get_rooms(ratekey)]}
    return request
