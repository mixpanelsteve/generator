import json

filenames = ["Landing Page", "Registration Complete", "Purchase"]

def json_csv(name, data):
    header = [name] + [str(key) for key in data[0]['properties'].keys()]
    with open(name + '.csv', 'w') as g:
        g.write(','.join(['event'] + header[1:]) + '\n')
        for event in data:
            g.write(','.join([name] + [str(event['properties'][key]) for key in header[1:]]) + '\n')

for event in filenames:
    with open(event + '.json', 'r') as f:
        data = f.read().split('\n')[:-1]

    data = [json.loads(line) for line in data]
    json_csv(event, data)
