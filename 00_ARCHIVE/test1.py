import requests
import json


def request_off():

    query = {
        "action": "process",
        "tagtype_0": "categories",
        "tag_contains_0": "contains",
        "tag_0": "Boissons",
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
            print(product["unique_scans_n"])
            print(product["nova_groups_tags"])
            print(product["nutrition_grades"])
        except KeyError:
            print("no nova")
            print("no nutrition grades")


def main():

    request_off()


if __name__ == "__main__":
    main()
