"""
    File Name   : unittests/services/weight_calculator.py
    Author      : Darryl Fernandes
    Description : Unit test script to validate the service method to calculate weight and other factors of the products
    Source File : services/weight_calculator.py
"""

from app.app_constants import START_ENDPOINT, BASE_URL
from app.util.url_data_extractor import extract_data


def get_industry_standard_cubic_weight(dimension):
    return (dimension.get('width', 0)/100) * (dimension.get('length', 0)/100) * (dimension.get('height', 0)/100) * 250


def is_product_dimension_provided(product):
    return product.get('size', None) and product['size'].get('width', 0) and product['size'].get('length', 0) \
           and product['size'].get('height', 0)


def get_all_products():
    end_point = START_ENDPOINT
    base_url = BASE_URL
    while end_point:
        url = '{}{}'.format(base_url, end_point)
        json_data = extract_data(url)
        for product in json_data.get('objects', []):
            yield product
        end_point = json_data.get('next', None)


def calculate_average_cubic_weight(category):
    list_cubic_weights = [get_industry_standard_cubic_weight(product['size']) for product in get_all_products()
                          if product.get('category', None) == category and is_product_dimension_provided(product)]

    return round(sum(list_cubic_weights)/len(list_cubic_weights), 3) if list_cubic_weights else 0


if __name__ == '__main__':
    print('Execution Started...')
    category = 'Air Conditioners'
    print('The average cubic weight for the category ({}) is :- {}'.format(
        category, calculate_average_cubic_weight(category)))
    print('Execution Completed...')
