from odeo.services.base_service import BaseService


class SubUserService(BaseService):

    def list_sub_users(self, page_token: str = None):
        pass

    def create_sub_user(self, email: str, name: str, phone_number: str):
        pass

    def update_sub_user(self, email: str, name: str, phone_number: str):
        pass
