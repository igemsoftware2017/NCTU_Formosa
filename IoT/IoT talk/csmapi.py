import requests

ENDPOINT = None

class CSMError(Exception):
    pass

def register(mac_addr, profile):
    r = requests.post(
        ENDPOINT + '/' + mac_addr,
        json={'profile': profile},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True


def deregister(mac_addr):
    r = requests.delete(ENDPOINT + '/' + mac_addr)
    if r.status_code != 200: raise CSMError(r.text)
    return True


def push(mac_addr, df_name, data):
    r = requests.put(
        ENDPOINT + '/' + mac_addr + '/' + df_name,
        json={'data': data},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True


def pull(mac_addr, df_name):
    r = requests.get(ENDPOINT + '/' + mac_addr + '/' + df_name)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['samples']

def get_alias(mac_addr, df_name):
    r = requests.get(ENDPOINT + '/get_alias/' + mac_addr + '/' + df_name)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['alias_name']

def tree():
    r = requests.get(ENDPOINT + '/tree')
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()
