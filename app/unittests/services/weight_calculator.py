"""
    File Name   : unittests\services\weight_calculator.py
    Author      : Darryl Fernandes
    Python Ver. : 3.5.1
    Description : Unit test script to validate the weight_calculator service module
    Source File : services\weight_calculator.py
"""

import unittest
from unittest import mock
from app.services import weight_calculator
from app.services.weight_calculator import calculate_average_cubic_weight


class TestAverageCubicWeight(unittest.TestCase):

    def setUp(self):
        self.baseurl = 'unittest://mocking.com'
        self.start_endpoint = '/api/products/1'

        weight_calculator.BASE_URL = self.baseurl
        weight_calculator.START_ENDPOINT = self.start_endpoint

        self.url_1_response = '''
            {
                "objects": [
                    {
                        "category": "Gadgets",
                        "title": "10 Pack Family Car Sticker Decals",
                        "weight": 120.0,
                        "size": {
                            "width": 15.0,
                            "length": 13.0,
                            "height": 1.0
                        }
                    },
                    {
                        "category": "Air Conditioners",
                        "title": "Window Seal for Portable Air Conditioner Outlets",
                        "weight": 235.0,
                        "size": {
                            "width": 26.0,
                            "length": 26.0,
                            "height": 5.0
                        }
                    }] , 
                "next": "/api/products/2"
            }'''

        self.url_2_response = '''
            {
                "objects": [
                    {
                        "category": "Oral Care", 
                        "title": "8 Pack Replacement Toothbrush Heads (Medium Bristles) - Oral-B Compatible", 
                        "weight": 60.0, 
                        "size": {
                            "width": 8.7, 
                            "length": 22.7, 
                            "height": 1.5
                        }
                    }
                ], 
                "next": "/api/products/a"
            }'''

        self.url_3_response = '''
            {
                "objects": [
                    {
                        "category": "Air Conditioners", 
                        "title": "Kogan 14,000 BTU Portable Air Conditioner (4.1KW, Reverse Cycle)", 
                        "weight": 35450.0, 
                        "size": {
                            "width": 49.5, 
                            "length": 56.8, 
                            "height": 87.5
                        }
                    }
                ], 
                "next": "/api/products/b"
            }'''

        self.url_last_response = '''
            {
                "objects": [
                    {
                        "category": "Shoes", 
                        "title": "Sports Gel Insoles (Men's)", 
                        "weight": 216.0, 
                        "size": {
                            "width": 9.8, 
                            "length": 32.0, 
                            "height": 1.0
                        }
                    }
                ], 
                "next": null
            }'''

        self.url_no_desired_category_response = '''
            {
                "objects": [
                    {
                        "category": "Shoes", 
                        "title": "Sports Gel Insoles (Men's)", 
                        "weight": 216.0, 
                        "size": {
                            "width": 9.8, 
                            "length": 32.0, 
                            "height": 1.0
                        }
                    }
                ], 
                "next": null
            }'''

        self.url_response_map = {'{}{}'.format(self.baseurl, self.start_endpoint): self.url_1_response,
                                 '{}/api/products/2'.format(self.baseurl): self.url_2_response,
                                 '{}/api/products/a'.format(self.baseurl): self.url_3_response,
                                 '{}/api/products/b'.format(self.baseurl): self.url_last_response,
                                 '{}/api/products/10'.format(self.baseurl): self.url_no_desired_category_response,
                                 }

    def mock_url_response(self, *args):
        if args[0] in self.url_response_map:
            mock_response = mock.Mock()
            mock_response_read = mock_response.read.return_value
            mock_response_read.decode.return_value = self.url_response_map.get(args[0])
            return mock_response

    @mock.patch('urllib.request.urlopen')
    def test_average_cubic_weight_with_no_desired_category_data(self, url_open):
        category = 'Air Conditioners'
        weight_calculator.START_ENDPOINT = '/api/products/10'
        url_open.side_effect = self.mock_url_response
        self.assertEqual(0, calculate_average_cubic_weight(category),
                         msg='The calculated average weight of the category {} is incorrect'.format(category))

    @mock.patch('urllib.request.urlopen')
    def test_average_cubic_weight_with_correct_json_data(self, url_open):
        category = 'Air Conditioners'
        url_open.side_effect = self.mock_url_response
        self.assertEqual(31.174, calculate_average_cubic_weight(category),
                         msg='The calculated average weight of the category {} is incorrect'.format(category))

    def test_average_cubic_weight_with_incorrect_json_data(self):
        category = 'Air Conditioners'
        with mock.patch('urllib.request.urlopen') as mock_request:
            mock_response = mock_request.return_value
            mock_response_read = mock_response.read.return_value
            mock_response_read.decode.return_value = 'Some incorrect non-json data format '
            self.assertRaises(Exception, calculate_average_cubic_weight, category)


if __name__ == '__main__':
    unittest.main()
