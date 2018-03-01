import sys, json

for line in sys.stdin:
    print json.dumps(json.loads(line))
