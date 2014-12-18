#!/usr/bin/python
''' create a simple funnel that has some problems '''
import base64
import json
import os
import random
import socket
import struct
import sys
import time
import urllib, urllib2

local_ip = '69.12.252.210'
current_time = time.time()
four_days = 4 * 24 * 60 * 60
categories = ['Housewares', 'Bedding', 'Books', 'Clothing', 'Cookware', 'Candles', 'Waffles']
url = "http://api.mixpanel.com/track"

def generate_email():

    name_list = ['Charles', 'Steve', 'Geddes', 'Drew', 'John', 'Sarah', 'Niki', 'Keira', 'Johan', 'Satchmo', 'Russel', 'Jimbo', 'Romero', 'Juliet', 'Booger', 'Pooper', 'farty', 'hairy', 'smelly', 'dopey', 'Virginia']
    last_names = ['Fox', 'Smith', 'Hanks', 'Ryan', 'Manning', 'Streisand', 'Obama', 'Washington', 'Bush', 'booger', 'Roosevelt', 'Jefferson', 'Credenza', 'cornnut', 'peanut', 'yogurt', 'football', 'hockey', 'chocolate', 'boozer', 'Fancy']
    domains = ['gmail.com', 'aol.com', 'prodigy.com', 'live.com']
    return random.choice(name_list) + '.' + random.choice(last_names) + str(random.randint(1, 9999)) + '@' + random.choice(domains)

def create_event(event_name, properties):

    temp_event = {
                  'event': event_name,
                  'properties': properties
                 }
    return temp_event

def create_landing_event(user):

    return create_event("Landing Page", {
                                            'distinct_id': user['distinct_id'],
                                            'time': user['user_time'],
                                            'token': user['token'],
                                            'library': 'javascript',
                                            'ip': user['ip']
                                        }
                       )

def create_registration(user):

    return create_event("Registration Complete", {
                                                    'ip': user['ip'],
                                                    'mixpanel id': user['distinct_id'],
                                                    'email': user['email'],
                                                    'time': user['user_time'],
                                                    'token': user['token'],
                                                    'library': 'Java'
                                                 }
                       )

def create_purchase(user):

    return create_event("Purchase", {
                                        'distinct_id': user['distinct_id'],
                                        'time': user['user_time'],
                                        'token': user['token'],
                                        'library': 'javascript',
                                        'item category': random.choice(categories),
                                        'ip': user['ip']
                                    }
                       )

def eventer(step, user):

    progresser = random.choice([True, True, True, False])
    if step == 0:
        temp = create_landing_event(user)
    elif step == 1:
        user['email'] = generate_email()
        temp = create_registration(user)
    elif step == 2:
        user['distinct_id'] = user['email']
        temp = create_purchase(user)
    elif step == 3:
        temp = create_landing_event(user)
    elif step == 4:
        temp = create_purchase(user)

    step = step + 1 if progresser else 100

    return step, user, temp


def creator(api_token):

    events = {'Landing Page': [], 'Registration Complete': [], 'Purchase': []}

    for x in range(13):
        distinct_id = list('%030x' % random.randrange(16**55))
        for i in [14, 24, 33, 40]:
            distinct_id[i] = '-'

        distinct_id = ''.join(distinct_id)
        user_time = int(current_time - random.random() * four_days)
        user = {
                'distinct_id': distinct_id,
                'token': api_token,
                'user_time': user_time,
                'ip': '.'.join([str(random.randint(0,255)) for x in range(4)])
                }

        j = 0
        while j < 5:
            j, user, event =  eventer(j, user)
            events[event['event']].append(event)
            user['user_time'] += int(random.random()*(current_time - user['user_time'])/random.randint(1, 4))

    return events

def track(events, ip):

    payload = {'data': base64.b64encode(json.dumps(events)), 'ip': ip}
    response = urllib2.urlopen(url, urllib.urlencode(payload)).read()
    if response != "1":
        print 'shit', events, payload

def batcher(event_list, ip):

    while event_list:
        batch = event_list[:50]
        event_list = event_list[50:]
        track(batch, ip)

def json_csv(name, data):

    header = [name] + [str(key) for key in data[0]['properties'].keys()]
    events = sorted(data, key=lambda k: k['properties']['time'])

    with open(name + '.csv', 'w') as g:
        g.write(','.join(['event'] + header[1:]) + '\n')
        for event in events:
            g.write(','.join([name] + [str(event['properties'][key]) for key in header[1:]]) + '\n')


if __name__ == '__main__':

    if len(sys.argv) > 2:
        token = sys.argv[1]
        name = sys.argv[2]
    elif len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print 'no token supplied'
        exit()

    sample_events = creator(token)
    for i, event_name in enumerate(sample_events.keys()):
        print event_name
        batcher(sample_events[event_name], ip = 1 if i == 1 else 0)

        json_csv(event_name, sample_events[event_name])

    os.system('mkdir %s | mv *.csv %s/ | cp instructions.txt %s/' % (name, name, name) if name else (token, token, token))
