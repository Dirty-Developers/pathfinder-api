#!/usr/bin/env python
# -*- coding: utf-8 -*
import sqlite as db


def save(agenda, events):
    a_id = db.store_agenda(title=agenda['title'], user_id=agenda['user_id'])
    for e in events:
        db.add_event(agenda_id=a_id, event_id=e['id'], checkin=e['checkin'], checkout=e['checkout'])
    return a_id


def retrieve(agenda_id):
    return db.retrieve_agenda(agenda_id)


def list(user_id):
    return db.list_agendas(user_id)


