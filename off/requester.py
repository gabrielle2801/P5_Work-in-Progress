import requests
# import json
from constants import OFF_API


def request_off(url):

    response = requests.get(OFF_API + url)

    if response.status_code != 200:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))

    else:
        return response


def request_search(url, query):

    response = requests.get(OFF_API + url, params=query)

    if response.status_code != 200:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))

    else:
        return response
