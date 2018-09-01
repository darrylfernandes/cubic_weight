"""
    File Name   : util/url_data_extractor.py
    Author      : Darryl Fernandes
    Description : Script to extract different formats of data from URL
    Source File : unittests/util/url_data_extractor.py
"""

import json
from urllib import request


def extract_data(url, data_type='json'):
    """

    :param url: resource locator
    :param data_type: The data format type expected to be returned when request is made to the url (defaulted to json)
                      Options: json, text, xml. Currently only json is supported
    :return: json
    """

    if data_type == 'json':
        response = request.urlopen(url)
        try:
            return json.loads(response.read().decode())
        except ValueError:
            raise Exception('Resource data is not a valid Json format')
