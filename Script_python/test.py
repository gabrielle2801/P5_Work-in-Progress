import requests
import json


def request_off():

    response = requests.get(
        "https://fr.openfoodfacts.org/categories.json")

    if response.status_code != 200:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))

    else:
        results = response.json()
        data_category = results.get('tags')
        print(results.keys())
        category_name = [data.get('name', 'None') for data in data_category]
        popular_cat = category_name[5]
        print(popular_cat)
        query = {"action": "process",
                 "categories": popular_cat,
                 "sort_by": "unique_scans_n",
                 "page_size": 10,
                 "json": 1}

        response_2 = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", params=query)
        results_2 = response_2.json()
        print(results_2.keys())
        products = results_2["products"]
        for product in products:
            print(product["product_name"])


def main():

    request_off()


if __name__ == "__main__":
    main()
