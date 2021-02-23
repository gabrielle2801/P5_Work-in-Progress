from off.view.view import HomepageView, CategoryListView, ProductByCategoryView,\
    ProductDetailView, SubstituteListView, ProductByNameView,\
    ProductByNameListView, ProductReminderView
from off.model.query.manager import DBManager
from off.constants import PRODUCT_DETAIL, SAVE_SUBSTITUT, SUBSTITUTES_LIST,\
    FOUND_PRODUCT, HOMEPAGE, RESEARCH_BY_CATEGORY, PRODUCTS_FOR_CATEGORY,\
    RESEARCH_BY_NAME, PRODUCT_REMINDER


class Controller:
    def __init__(self):
        self.page = HOMEPAGE
        self.running = True
        self.input = ""
        self.choice = None
        self.choice_category = None
        self.choice_product = None
        self.substitute_proposed = None
        self.run()

    def run(self):
        manager = DBManager()
        while self.running:
            if self.page == HOMEPAGE:
                view = HomepageView()
                view.display()
                self.page = view.get_next_page()
            elif self.page == RESEARCH_BY_CATEGORY:
                categories = manager.get_categories()
                view = CategoryListView()
                view.display(categories=categories)
                self.page, self.choice_category = view.get_next_page()
            elif self.page == PRODUCTS_FOR_CATEGORY:
                products = manager.get_products_for_category(
                    self.choice_category)
                view = ProductByCategoryView()
                view.display(products=products)
                self.page, self.choice_product = view.get_next_page()
            elif self.page == PRODUCT_DETAIL:
                product = manager.get_products(product_id=self.choice_product)
                substituts = manager.get_substitutes(
                    product_id=self.choice_product,
                    category_id=self.choice_category)
                store = manager.get_stores_for_product(
                    product_id=self.choice_product)
                store_substitut = manager.get_stores_for_substituts(
                    substitut_list=substituts)
                view = ProductDetailView()
                view.display(product, substituts, store, store_substitut)
                self.page, self.choice = view.get_next_page(
                    substituts=substituts)
            elif self.page == SAVE_SUBSTITUT:
                product_id, substitut_id = self.choice_product, self.choice
                manager.create_substitute(product_id, substitut_id)
                self.page = HOMEPAGE
            elif self.page == RESEARCH_BY_NAME:
                view = ProductByNameView()
                view.display()
                self.page, self.input, self.choice_category = view.get_next_page()
            elif self.page == FOUND_PRODUCT:
                product_found = manager.search_product(self.input)
                view = ProductByNameListView()
                view.display(products=product_found)
                self.page, self.choice_product = view.get_next_page(
                    products=product_found)
            elif self.page == SUBSTITUTES_LIST:
                substituts = manager.get_substitute_saved()
                products = manager.get_products(product_id=self.choice_product)
                view = SubstituteListView()
                view.display(substituts=substituts)
                self.page, self.choice_product = view.get_next_page(
                    products=products)
            elif self.page == PRODUCT_REMINDER:
                products = manager.get_products(product_id=self.choice_product)
                store = manager.get_stores_for_product(
                    product_id=self.choice_product)
                view = ProductReminderView()
                view.display(products, store)
                self.page, self.choice = view.get_next_page()
