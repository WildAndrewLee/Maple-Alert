import json
import os
from object import Object

secrets = Object()

path = os.path.abspath(os.path.join('/maple-alert', 'secrets.json'))

with open(path) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    secrets.update(s)

del path