#!/usr/bin/env python
# -*- coding: utf-8 -*
from requests import get, HTTPError
from os import environ as env


HEADERS = {'Accept': "application/json", 'Content-Type': "application/json", 'Authorization': "Bearer " + env['yelp_key']}
URL = "https://api.yelp.com/v3/businesses/"


def lookup(business_id):
    """Detailed business content

    Args:
        business_id: Required. Yelp id of the business

    Ref: https://www.yelp.com/developers/documentation/v3/business
    """
    return __connect(business_id)


def search(**args):
    """
    Returns up to 1000 businesses based on the provided search criteria.
    It has some basic information about the business.

    Args:
        location: Required if either latitude or longitude is not provided. 
                    Specifies the combination of "address, neighborhood, city, state or zip, optional country" 
        latitude: Decimal. Required if location is not provided. Latitude of the location you want to search nearby.
        longitude: Decimal. Required if location is not provided. Longitude of the location you want to search nearby.
        term: Optional. keyword you are looking for in a business (food, restaurants...)

        For optional arguments check reference

    Ref: https://www.yelp.com/developers/documentation/v3/business_search
    """
    return __connect("search", **args)


def matches(**args):
    """
    Match business data from other sources against businesses on Yelp, based on minimal provided information.

    Args:
        name: Required. Name of the business. Maximum length is 64; only digits, letters, spaces, and !#$%&+,­./:?@'are allowed.
        city: Required. City of the business. Maximum length is 64; only digits, letters, spaces, and ­’.() are allowed.
        state: Required. State code of this business. Maximum length is 3.
        country: Required. Country code of this business. Maximum length is 2.

        For optional arguments check reference.

    Returns:
        JSON. Up to 10 businesses that are the best matches based on the information provided.

    Ref: https://www.yelp.com/developers/documentation/v3/business_match
    """
    return __connect("matches/lookup", **args)


def __connect(trail, **args):
    url = URL + trail
    result = get(url, params=args, headers=HEADERS)
    if not result.ok:
        raise HTTPError("{}: {}".format(result.reason, url))
    return result.json()


