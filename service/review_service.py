class ReviewService:
    def __init__(self, review_dao):
        self.review_dao = review_dao

    def get_review(self, session, product_id):
        review_info = self.review_dao.get_review(session, product_id)
        return review_info

    def insert_review(self, session, user_id, data):
        response = self.review_dao.insert_review(session, user_id, data)
        return response

