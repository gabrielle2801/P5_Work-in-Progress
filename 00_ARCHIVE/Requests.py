import requests
import json

r = requests.get('https://world.openfoodfacts.org/categories.json').json()
with open("categories_openfoodfacts.json", "w") as write_file:
    json.dump(r, write_file)

r2 = requests.get('https://world.openfoodfacts.org/ingredients.json').json()
with open("ingredients_openfoodfacts.json", "w") as write_file:
    json.dump(r2, write_file)
