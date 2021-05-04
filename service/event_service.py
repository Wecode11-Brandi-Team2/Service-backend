class EventService:
    def __init__(self, event_dao):
        self.event_dao = event_dao

    def select_event_list(self, event_info, session):
        event_lists = self.event_dao.select_event_list(event_info, session)
        return [dict(event_list) for event_list in event_lists]

    def select_event_detail(self, event_info, session):
        event_detail_lists = self.event_dao.select_event_detail(event_info, session)
        event_buttons = self.event_dao.check_buttons(event_info, session)
        return (
            [dict(event_detail_list) for event_detail_list in event_detail_lists],
            [dict(event_button) for event_button in event_buttons],
        )

    def select_event_products(self, event_info, session):
        event_products = self.event_dao.select_event_products(event_info, session)
        return [dict(event_product) for event_product in event_products]
