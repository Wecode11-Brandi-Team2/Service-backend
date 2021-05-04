import datetime


class OrderService:
    def __init__(self, order_dao):
        self.order_dao = order_dao

    def insert_orders(self, order_info, user_id, session):
        new_order = self.order_dao.insert_orders(order_info, user_id, session)
        return new_order

    def select_order_item(self, user_id, session):
        order_item_infos = self.order_dao.select_order_item(user_id, session)
        order_item_info = [dict(order_item_info) for order_item_info in order_item_infos]
        return order_item_info

    def insert_cancel_reason(self, cancel_info, user_id, session):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order_dao.end_record(cancel_info, now, session)
        self.order_dao.insert_cancel_reason(cancel_info, now, session)

    def insert_refund_reason(self, refund_info, user_id, session):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order_dao.end_record(refund_info, now, session)
        self.order_dao.insert_refund_reason(refund_info, now, session)

    def insert_refund_cancel(self, refund_cancel, user_id, session):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order_dao.end_record(refund_cancel, now, session)
        self.order_dao.insert_refund_cancel(refund_cancel, now, session)
