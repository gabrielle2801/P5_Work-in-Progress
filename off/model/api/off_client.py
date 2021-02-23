from off.model.api.requester import request_off
from off.constants import MAX_CATEGORIES, MAX_PRODUCTS


class OpenFoodFactsApi:

    def get_categories(self):
        response_category = request_off("categories.json?sort_by=products")
        results_category = response_category.json()
        data_category = results_category.get('tags')
        categories = [data.get('name') for data in data_category
                      if data.get("name")]
        category_name = categories[0:MAX_CATEGORIES]
        print(category_name)
        return category_name

    def get_products(self, category_name):
        print(category_name)
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category_name,
            "sort_by": "unique_scans_n",
            "page_size": MAX_PRODUCTS,
            "json": 1}
        print(query)
        response_product = request_off("cgi/search.pl?", query)
        print(response_product)
        result_product = response_product.json()
        return result_product["products"]
