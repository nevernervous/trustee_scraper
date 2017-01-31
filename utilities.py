import os
from random import choice

import requests

from myLogger import get_main_dir
from constants import proxy_username, proxy_password


with open(os.path.join(get_main_dir(), 'proxies.txt'), 'r') as f:
    proxieslist = f.read().splitlines()


def get_gimme_proxy():
    r = requests.get('http://gimmeproxy.com/api/getProxy?get=true&maxCheckPeriod=300').json()
    proxy = r['ipPort']
    proxies = {'http': 'http://%s' % proxy, 'https': 'http://%s' % proxy}
    return proxies


def get_proxy():
    # return get_gimme_proxy()
    proxy = choice(proxieslist)
    proxies = {'http': 'http://{}:{}@{}'.format(proxy_username, proxy_password, proxy)}
    proxies['https'] = proxies['http']
    return proxies
