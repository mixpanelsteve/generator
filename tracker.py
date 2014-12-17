import base64
import json
import urllib, urllib2

funnel_events = ['Landing Page', 'Registration Complete', 'Purchase']
url = 'http://api.mixpanel.com/track'

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

for i, event in enumerate(funnel_events):
    with open(event + '.json', 'r') as f:
        ip = 1 if i == 1 else 0
        batcher([json.loads(line) for line in f.read().split('\n')[:-1]], ip)
