import urllib3
import json

TIMEOUT = 1


def fetch_url(url):
    http = urllib3.PoolManager()
    try:
        resp = http.request('GET', url, timeout=TIMEOUT)
    except Exception as e:
        return ''
    return resp.data.decode('utf-8')


def parse():
    site = fetch_url('10.0.0.28?json')

    if site:
        site = json.loads(site)

    return site
