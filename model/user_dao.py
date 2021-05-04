class UserDao:
    def insert_google_user(self, user_info, session):
        query = """INSERT INTO users (
                        email, 
                        name,
                        phone_number,
                        login_id,
                        platform_id,
                        created_at,
                        is_deleted
                    )
                    VALUES(
                        :email,
                        :sign_up_name,
                        :phone_number,
                        :login_id,
                        2,
                        now(),
                        0
                )"""
        row = session.execute(
            query,
            {
                "email": user_info["email"],
                "sign_up_name": user_info["name"],
                "phone_number": user_info["phone_number"],
                "login_id": user_info["login_id"],
            },
        ).lastrowid

        return row

    def check_google_user(self, user_info, session):
        query = """ SELECT email, id
                    FROM users
                    WHERE email = :email
                """
        row = session.execute(query, {"email": user_info["email"]}).fetchall()

        return row

    def count_shipping_address(self, user_id, session):
        query = """ SELECT COUNT(*) AS count
                    FROM shipping_address
                    WHERE user_id = :user_id
                    AND is_deleted = 0
                """
        count_shipping_address = session.execute(query, {"user_id": user_id["user_id"]}).fetchone()

        return count_shipping_address[0]

    def check_is_default(self, user_id, check_info, session):
        query = """ SELECT id
                    FROM shipping_address
                    WHERE user_id = :user_id
                    AND is_default = 1
                    AND id = :id
                """
        row = session.execute(query, {"user_id": user_id["user_id"], "id": check_info}).fetchall()

        return row

    def update_is_default(self, user_id, session):
        query = """ UPDATE shipping_address
                    SET is_default = 0,
                        created_at = now()
                    WHERE user_id = :user_id
                    AND is_default = 1
                """
        session.execute(query, {"user_id": user_id["user_id"]})

    def new_is_default(self, user_id, session):
        query = """ UPDATE shipping_address
                    SET is_default = 1,
                        created_at = now()
                    WHERE user_id = :user_id
                    AND is_default = 0
                    AND is_deleted = 0
                    ORDER BY created_at DESC LIMIT 1
                """
        session.execute(query, {"user_id": user_id["user_id"]})

    def insert_shipping_address(self, shipping_address_info, user_id, session):
        query = """INSERT INTO shipping_address (
                        user_id, 
                        zone_code,
                        address,
                        detail_address,
                        phone_number,
                        reciever,
                        is_default,
                        is_deleted,
                        created_at
                    )
                    VALUES(
                        :user_id,
                        :zone_code,
                        :address,
                        :detail_address,
                        :phone_number,
                        :reciever,
                        :is_default,
                        0,
                        now()
                )"""
        row = session.execute(
            query,
            {
                "user_id": user_id["user_id"],
                "zone_code": shipping_address_info["zone_code"],
                "address": shipping_address_info["address"],
                "detail_address": shipping_address_info["detail_address"],
                "phone_number": shipping_address_info["phone_number"],
                "reciever": shipping_address_info["reciever"],
                "is_default": shipping_address_info["is_default"],
            },
        ).lastrowid

        return row

    def select_shipping_address(self, user_id, session):
        query = """ SELECT
                    id,
                    user_id,
                    zone_code,
                    address,
                    detail_address,
                    phone_number,
                    reciever,
                    is_default
                    FROM  shipping_address
                    WHERE user_id = :user_id
                    AND is_deleted = 0
                    ORDER BY is_default DESC
                """
        row = session.execute(query, {"user_id": user_id["user_id"]}).fetchall()

        return row

    def update_shipping_address(self, shipping_address_info, user_id, session):
        query = """ UPDATE shipping_address
                    SET zone_code      = :zone_code,
                        address        = :address,
                        detail_address = :detail_address,
                        phone_number   = :phone_number,
                        reciever       = :reciever,
                        is_default     = :is_default,
                        created_at     = now()
                    WHERE id = :id
                    AND   user_id = :user_id
                """

        session.execute(
            query,
            {
                "user_id": user_id["user_id"],
                "zone_code": shipping_address_info["zone_code"],
                "address": shipping_address_info["address"],
                "detail_address": shipping_address_info["detail_address"],
                "phone_number": shipping_address_info["phone_number"],
                "reciever": shipping_address_info["reciever"],
                "is_default": shipping_address_info["is_default"],
                "id": shipping_address_info["id"],
            },
        )

    def delete_shipping_address(self, user_id, delete_info, session):
        query = """ UPDATE shipping_address
                    SET is_deleted = 1,
                        created_at = now()
                    WHERE  id = :id
                    AND user_id = :user_id
                    AND is_deleted = 0
                """

        session.execute(query, {"user_id": user_id["user_id"], "id": delete_info})

