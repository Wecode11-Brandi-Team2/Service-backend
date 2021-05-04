class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_menu(self, first_category_id, session):
        categories = self.product_dao.get_menu(first_category_id, session)
        return categories

    def get_sellers(self, q, session):
        sellers = self.product_dao.get_sellers(q, session)
        return sellers

    def get_products(self, filter_dict, session):
        products = [
            {
                "id": product.id,
                "name": product.name,
                "image": product.main_img,
                "price": product.price,
                "sales_amount": product.sales_amount,
                "discount_rate": product.discount_rate,
                "discount_price": product.discount_price,
                "is_promotion": product.is_promotion,
                "seller_name": product.korean_name,
            }
            for product in self.product_dao.get_products(filter_dict, session)
        ]

        return products

    def get_product(self, product_id, session):
        product = self.product_dao.get_product(product_id, session)
        return product
