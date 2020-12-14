import requests
import json


def request_off():

    response = requests.get(
        "https://fr.openfoodfacts.org/categories.json?sort_by=products")

    if response.status_code != 200:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))

    else:
        results = response.json()
        data_category = results.get('tags')
        print(results.keys())
        category_name = [data.get('name', 'None') for data in data_category]
        popular_cat = category_name[0:11]
        print(popular_cat)

        for category in popular_cat:
            query = {"action": "process",
                     "tagtype_0": "categories",
                     "tag_contains_0": "contains",
                     "tag_0": category,
                     "sort_by": "unique_scans_n",
                     "page_size": 10,
                     "json": 1}

            response_2 = requests.get(
                "https://fr.openfoodfacts.org/cgi/search.pl?", params=query)
            results_2 = response_2.json()
            print(results_2.keys())
            products = results_2["products"]
            with open("produits.json", "w") as write_file:
                json.dump(results_2, write_file)
                print("ok  i")
            for product in products:
                try:
                    print(product["product_name"])
                    print(product["nova_groups_tags"])
                    print(product["nutrition_grades"])
                except KeyError:
                    print("no nova")
                    print("no nutrition grades")


def main():

    request_off()


if __name__ == "__main__":
    main()
