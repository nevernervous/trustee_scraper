import os
from random import choice
from datetime import datetime

import requests

from myLogger import get_main_dir
from constants import proxy_username, proxy_password, headers


print(datetime.now())
with open(os.path.join(get_main_dir(), 'proxies.txt'), 'r') as f:
    proxieslist = f.read().splitlines()

proxy = choice(proxieslist)
proxies = {'http': 'http://{}:{}@{}'.format(proxy_username, proxy_password, proxy)}
proxies['https'] = proxies['http']

zillow_url = 'http://geoip.hidemyass.com'
r = requests.get(zillow_url, headers=headers, proxies=proxies)
print r.content

print(datetime.now())
