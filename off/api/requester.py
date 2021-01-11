import requests
from constants import OFF_API


def request_off(url, params=None):

    response = requests.get(OFF_API + url, params=params)

    if response.status_code != 200:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))

    else:
        return response
