from requester import request_off, request_search
from constants import MAX


class OpenFoodFactsApi:
    def __init__(self):
        print("ok")

    def get_categories(self):
        response_category = request_off("categories.json?sort_by=products")
        results_category = response_category.json()
        data_category = results_category.get('tags')
        category_name = [data.get('name') for data in data_category
                         if data.get("name")]
        popular_category = category_name[0:MAX]
        print(popular_category)
        return popular_category

    def get_products(self, popular_category):
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": popular_category,
            "sort_by": "unique_scans_n",
            "page_size": 10,
            "json": 1}

        response_product = request_search("cgi/search.pl?", query)
        result_product = response_product.json()
        return result_product["products"]

    def get_producthealthy(self, popular_category):
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": popular_category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": "A",
            "sort_by": "unique_scans_n",
            "page_size": 10,
            "json": 1}

        response_healthy = request_search("cgi/search.pl?", query)
        result_healthy = response_healthy.json()
        return result_healthy["products"]
