class ReviewDao:
    def get_review(self, session, product_id):
        querry = """
        SELECT
            rating,
            content,
            reviews.created_at,
            users.login_id,
            review_status.status_name
        FROM reviews

        INNER JOIN users
        ON reviews.user_id = users.id

        INNER JOIN review_status
        ON reviews.review_status_id = review_status.id
        
        INNER JOIN order_item_info
        ON reviews.order_item_info_id = order_item_info.id

        INNER JOIN products
        ON products.id = order_item_info.product_id

        WHERE products.id = :product_id
        """

        reviews = session.execute(querry, {"product_id": product_id}).fetchall()
        return reviews

    def insert_review(self, session, user_id, data):
        querry_into_reviews = """
        INSERT INTO reviews(
            user_id,
            order_item_info_id,
            review_status_id,
            rating,
            content,
            created_at,
            is_deleted,
            product_id
        )
        VALUES(
            :user_id,
            :order_item_info_id,
            :review_status_id,
            :rating,
            :content,
            now(),
            0,
            :product_id
        )
        """

        # querry line
        session.execute(
            querry_into_reviews,
            {
                "user_id": user_id,
                "order_item_info_id": data["order_item_info_id"],
                "review_status_id": data["review_status_id"],
                "rating": data["rating"],
                "content": data["content"],
                "product_id": data["product_id"],
            },
        )

