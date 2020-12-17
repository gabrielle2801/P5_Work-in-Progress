# import json
from requester import request_off, request_search


class OpenFoodFactsApi:
    def __init__(self):
        print("ok")

    def get_categories(self):
        response = request_off("categories.json?sort_by=products")
        results = response.json()
        data_category = results.get('tags')
        category_name = [data.get('name', 'None') for data in data_category]
        popular_cat = category_name[0:10]
        print(popular_cat)
        return popular_cat

    def get_products(self, popular_cat):
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": popular_cat,
            "sort_by": "unique_scans_n",
            "page_size": 10,
            "json": 1}

        response_2 = request_search("cgi/search.pl?", query)
        result_2 = response_2.json()
        return result_2["products"]

    def get_stores(self):
        response_3 = request_off("stores.json")
        result_3 = response_3.json()
        data_store = result_3.get('tags')
        store_name = [data.get('name', 'None') for data in data_store]
        print(len(store_name))
        return store_name
