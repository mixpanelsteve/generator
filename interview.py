''' create a simple funnel that has some problems '''
import credentials
import json
import random
import socket
import struct
import time

local_ip = '69.12.252.210'
current_time = time.time()
four_days = 4 * 24 * 60 * 60
categories = ['Housewares', 'Bedding', 'Books', 'Clothing', 'Cookware', 'Candles', 'Waffles']
events = {'Landing Page': [], 'Registration Complete': [], 'Purchase': []}

def generate_email():
    name_list = ['Charles', 'Steve', 'Geddes', 'Drew', 'John', 'Sarah', 'Niki', 'Keira', 'Johan', 'Satchmo', 'Russel', 'Jimbo', 'Romero', 'Juliet', 'Booger', 'Pooper', 'farty', 'hairy', 'smelly', 'dopey', 'Virginia']
    last_names = ['Fox', 'Smith', 'Hanks', 'Ryan', 'Manning', 'Streisand', 'Obama', 'Washington', 'Bush', 'booger', 'Roosevelt', 'Jefferson', 'Credenza', 'cornnut', 'peanut', 'yogurt', 'football', 'hockey', 'chocolate', 'boozer', 'Fancy']
    domains = ['gmail.com', 'aol.com', 'prodigy.com', 'live.com']
    return random.choice(name_list) + '.' + random.choice(last_names) + str(random.randint(1, 9999)) + '@' + random.choice(domains)

def create_event(event_name, properties):
    temp_event = {'event': event_name,
                  'properties': properties
                 }
    events[event_name].append(temp_event)

def create_landing_event(user):
    create_event("Landing Page", {'distinct_id': user['distinct_id'], 'time': user['user_time'], 'token': credentials.API_TOKEN, 'library': 'javascript', 'ip': user['ip']})

def create_registration(user):
    create_event("Registration Complete", {'ip': user['ip'], 'time': user['user_time'], 'token': credentials.API_TOKEN, 'library': 'Java'})

def create_purchase(user):
    create_event("Purchase", {'distinct_id': user['distinct_id'], 'time': user['user_time'], 'token': credentials.API_TOKEN, 'library': 'javascript', 'item category': random.choice(categories), 'ip': user['ip']})

def eventer(step, user):

    progresser = random.choice([True, True, False, True, False, True])
    if step == 0:
        create_landing_event(user)
    elif step == 1:
        create_registration(user)
        user['distinct_id'] = generate_email()
    elif step == 2:
        create_purchase(user)
    elif step == 3:
        create_landing_event(user)
        user['user_time'] += random.randint(1, 2000)
        create_purchase(user)

    step = step + 1 if progresser else 100

    return step, user


def creator():
    for x in range(13172):
        distinct_id = list('%030x' % random.randrange(16**55))
        for i in [14, 24, 33, 40]:
            distinct_id[i] = '-'

        distinct_id = ''.join(distinct_id)
        user_time = int(current_time - random.random() * four_days)
        user = {'distinct_id': distinct_id, 'user_time': user_time, 'ip': socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))}

        j = 0
        while j < 4:
            j, user =  eventer(j, user)
            user['user_time'] += int(random.random()*(current_time - user['user_time'])/random.randint(1, 4))

creator()
for event_name in events.keys():
    with open(event_name + ".json", "w") as f:
        for line in events[event_name]:
            f.write(json.dumps(line) + '\n')
