from integrations.availability import PaxTypes


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
