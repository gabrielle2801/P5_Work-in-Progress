from view.view import HomepageView, CategoryListView, ProductByCategoryView
from view.view import ProductDetailView, ResearchListView, SubtituteListView, ProductByNameView
from query.manager import DBManager
from constants import HOMEPAGE, RESEARCH_BY_CATEGORY, PRODUCTS_FOR_CATEGORY, RESEARCH_BY_NAME
from constants import PRODUCT_DETAIL, SAVE_SUBTITUT, SUBTITUTES_LIST, SUBTITUTES_RESEARCH


class Controller:
    def __init__(self):
        self.page = HOMEPAGE
        self.running = True
        self.input = ""
        self.choice = None
        self.choice_category = None
        self.choice_product = None
        self.run()

    def run(self):
        manager = DBManager()
        while self.running:
            if self.page == HOMEPAGE:
                view = HomepageView()
                view.display()
                self.page = view.get_next_page()
            elif self.page == RESEARCH_BY_NAME:
                products = manager.get_product_by_name(self.input)
                view = ProductByNameView()
                view.display(products=products)
                self.page, self.input = view.get_next_page()
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
                subtituts = manager.get_subtitutes(
                    product_id=self.choice_product, category_id=self.choice_category)
                store = manager.get_stores_for_product(
                    product_id=self.choice_product)
                view = ProductDetailView()
                view.display(product, subtituts, store)
                self.page, self.choice = view.get_next_page()
            elif self.page == SAVE_SUBTITUT:
                product_id, subtitut_id = self.choice_product, self.choice
                manager.create_subtitute(product_id, subtitut_id)
                self.page = HOMEPAGE
                self.choice = product_id
            elif self.page == SUBTITUTES_LIST:
                products = manager.get_research_list()
                view = ResearchListView()
                view.display(products=products)
                self.page, self.choice = view.get_next_page()
            elif self.page == SUBTITUTES_RESEARCH:
                subtituts = manager.get_subtitute_saved()
                view = SubtituteListView()
                view.display(subtituts=subtituts)
                self.page, self.choice_product = view.get_next_page()
