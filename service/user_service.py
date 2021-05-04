import jwt

from config import SECRET_KEY, ALGORITHM


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def check_google_user(self, user_info, session):
        user = self.user_dao.check_google_user(user_info, session)
        if not user:
            return None
        return user

    def google_sign_up_user(self, user_info, session):
        new_user_info = self.user_dao.insert_google_user(user_info, session)
        return new_user_info

    def generate_access_token(self, user_info):
        access_token = jwt.encode({"user_id": user_info}, SECRET_KEY, ALGORITHM).decode("utf-8")
        return access_token

    def insert_shipping_address(self, shipping_address_info, user_id, session):
        count_shipping_address = self.user_dao.count_shipping_address(user_id, session)
        if count_shipping_address < 5:
            if count_shipping_address == 0:
                shipping_address_info["is_default"] = 1
            elif shipping_address_info["is_default"] == 1:
                self.user_dao.update_is_default(user_id, session)
            new_shipping_address_info = self.user_dao.insert_shipping_address(
                shipping_address_info, user_id, session
            )
            return new_shipping_address_info

    def select_shipping_address(self, user_id, session):
        shipping_address_infos = self.user_dao.select_shipping_address(user_id, session)
        shipping_address_info = [
            dict(shipping_address_info) for shipping_address_info in shipping_address_infos
        ]
        return shipping_address_info

    def update_shipping_address(self, shipping_address_info, user_id, session):
        if shipping_address_info["is_default"] == 1:
            self.user_dao.update_is_default(user_id, session)
        self.user_dao.update_shipping_address(shipping_address_info, user_id, session)

    def delete_shipping_address(self, user_id, delete_info, session):
        check_is_delete = self.user_dao.check_is_default(user_id, delete_info, session)
        if check_is_delete:
            self.user_dao.new_is_default(user_id, session)
        shipping_address_info = self.user_dao.delete_shipping_address(user_id, delete_info, session)
        return shipping_address_info

