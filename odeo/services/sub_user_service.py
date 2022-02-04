from odeo.models.sub_user import SubUser
from odeo.services.base_service import BaseService, authenticated


class SubUserService(BaseService):

    @authenticated
    def list_sub_users(self, page_token: str = None):
        params = {'page_token': page_token} if page_token is not None else {}
        content = self.request('GET', '/sub-users', params).json()
        sub_users = list(map(lambda sub_user: SubUser.from_json(sub_user), content['sub_users']))

        return sub_users, content['next_page_token']

    def create_sub_user(self, email: str, name: str, phone_number: str):
        pass

    def update_sub_user(self, email: str, name: str, phone_number: str):
        pass
