class EventDao:
    def select_event_list(self, event_info, session):
        query = """SELECT 
                        id,
                        banner_image
                    FROM events
                    WHERE is_displayed = :is_displayed
                    ORDER BY id ASC
                    LIMIT :limit
                    OFFSET :offset
                """

        row = session.execute(
            query,
            {
                "is_displayed": event_info["is_displayed"],
                "limit": event_info["limit"],
                "offset": event_info["offset"],
            },
        ).fetchall()

        return row

    def select_event_detail(self, event_info, session):
        query = """ SELECT
                        simple_description,
                        detail_description,
                        video_url,
                        detail_image
                    FROM events
                    WHERE is_deleted = 0
                    AND id = :id
                """

        row = session.execute(query, {"id": event_info["id"]}).fetchall()

        return row

    def check_buttons(self, event_info, session):
        query = """ SELECT DISTINCT
                        e_bt.id AS button_id
                    FROM events AS e
                    INNER JOIN event_button AS e_bt ON e.id = e_bt.event_id
                    INNER JOIN event_product_mappings AS e_pd ON e.id = e_pd.event_id
                    WHERE e.is_deleted = 0
                    AND e.id = :id
                """

        row = session.execute(query, {"id": event_info["id"]}).fetchall()

        return row

    def select_event_products(self, event_info, session):
        query = """ SELECT 
                        p_info.name,
                        p_info.main_img AS image,
                        p_info.price,
                        s_info.korean_name AS seller_name
                    FROM events AS e
                    INNER JOIN event_product_mappings AS e_pd ON e.id = e_pd.event_id
                    INNER JOIN products AS p ON e_pd.product_id = p.id
                    INNER JOIN product_info AS p_info ON p.id = p_info.product_id
                    INNER JOIN sellers AS s ON p_info.seller_id = s.id
                    INNER JOIN seller_info AS s_info ON s.id = s_info.seller_id
                    WHERE e.is_deleted = 0
                    AND e.id = :id
                """

        if event_info["button_id"] != 0:
            query += " AND e_pd.button_id = :button_id"

        query += " LIMIT :limit OFFSET :offset"

        row = session.execute(
            query,
            {
                "id": event_info["id"],
                "button_id": event_info["button_id"],
                "limit": event_info["limit"],
                "offset": event_info["offset"],
            },
        ).fetchall()

        return row
