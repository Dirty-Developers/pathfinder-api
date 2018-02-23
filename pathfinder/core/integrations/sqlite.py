#!/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3
import logging as log
from sqlite3 import Error
from os import environ as env


__db = sqlite3.connect(env['DB_PATH'])
__db.row_factory = sqlite3.Row


def __cursor():
    return __db.cursor()


def __store(sql):
    last = None
    cursor = __cursor()
    try:
        cursor.execute(sql)
        __db.commit()
    except Error as e:
        log.error(e)
    finally:
        last = cursor.lastrowid
        cursor.close()
    return last


def __retrieve(sql):
    query = None
    cursor = __cursor()
    try:
        select = cursor.execute(sql)
        query = [dict(r) for r in select.fetchall()]
    except Error as e:
        log.error(e)
    finally:
        cursor.close()
    return query


def store_agenda(**agenda):
    """
    Create a new agenda
    """
    if agenda.get('agenda_id'):
        #overwrite
        sql = "UPDATE agenda SET title = '{}', user_id = '{}' WHERE agenda_id = '{}'".format(agenda['title'], agenda['user_id'], agenda['agenda_id'])
        return __store(sql)
    elif agenda.get('title'):
        #create 
        sql = "INSERT INTO agenda(title, user_id) VALUES('{}','{}')".format(agenda['title'], agenda['user_id'])
        return __store(sql)
    else:
        raise Exception("Bad use of agenda: " + str(agenda))


def store_event(**event):
    """
    Create new event
    """
    if event.get('type'):
        sql = "INSERT INTO event(title, longitude, latitude, event_type) VALUES('{}','{}','{}','{}')".format(event['title'], event['longitude'], event['latitude'], event['type'])
    else:
        sql = "INSERT INTO event(title, longitude, latitude) VALUES('{}','{}','{}')".format(event['title'], event['longitude'], event['latitude'])
    return __store(sql)


def add_event(**relation):
    sql = "INSERT INTO agenda_event(agenda_id, event_id, checkin, checkout) VALUES('{}','{}','{}','{}')".format(relation['agenda_id'], relation['event_id'], relation['checkin'], relation['checkout'])
    return __store(sql)


def retrieve_agenda(agenda_id):
    return __retrieve("SELECT * FROM agenda WHERE agenda_id='{}'".format(agenda_id))[0]



def retrieve_event(event_id):
    return __retrieve("SELECT * FROM event WHERE event_id='{}'".format(event_id))[0]


def retrieve_events(agenda_id):
    return __retrieve("SELECT * FROM agenda_event WHERE agenda_id='{}'".format(agenda_id))


def list_agendas(user_id):
    return __retrieve("SELECT * FROM agenda WHERE user_id='{}'".format(user_id))


