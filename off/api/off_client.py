from api.requester import request_off
from constants import MAX


class OpenFoodFactsApi:
    def __init__(self):
        print("ok")

    def get_categories(self):
        response_category = request_off("categories.json?sort_by=products")
        results_category = response_category.json()
        data_category = results_category.get('tags')
        categories = [data.get('name') for data in data_category
                      if data.get("name")]
        category_name = categories[0:MAX]
        return category_name

    def get_products(self, category_name):
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category_name,
            "sort_by": "unique_scans_n",
            "page_size": 100,
            "json": 1}

        response_product = request_off("cgi/search.pl?", query)
        result_product = response_product.json()
        return result_product["products"]
