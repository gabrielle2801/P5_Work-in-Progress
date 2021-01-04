from view import HomepageView, Category, ProductbyCategory, Detail_product, Subtitute
from constants import RECHERCHE_PAR_CATEGORY, HOMEPAGE, PRODUCT, DETAIL_PRODUCT
from constants import SAVE_SUBTITUT


class Controller:
    def __init__(self):
        self.page = HOMEPAGE
        self.running = True
        self.input = ""
        self.category = ""
        self.product = ""
        self.subtitute = ""
        self.name = ""
        self.nutriscore = ""
        self.description = ""
        self.store = ""
        self.url = ""
        self.run()

    def run(self):
        while self.running:
            if self.page == HOMEPAGE:
                view = HomepageView()
                view.display()
                self.page = view.get_next_page()
            elif self.page == RECHERCHE_PAR_CATEGORY:
                view = Category()
                view.display()
                self.page, self.category = view.get_next_page()
            elif self.page == PRODUCT:
                view = ProductbyCategory()
                view.display(self.category)
                self.page, self.product = view.get_next_page(self.category)
            elif self.page == DETAIL_PRODUCT:
                view = Detail_product()
                view.display(self.product, self.category)
                self.page, self.subtitute = view.get_next_page(self.name,
                                                               self.nutriscore,
                                                               self.description,
                                                               self.url,
                                                               self.store)
            elif self.page == SAVE_SUBTITUT:
                view = Subtitute()
                view.display(self.name, self.nutriscore,
                             self.description, self.url, self.store)
                self.subtitute = view.get_next_page(self.name,
                                                    self.nutriscore,
                                                    self.description,
                                                    self.url,
                                                    self.store)
