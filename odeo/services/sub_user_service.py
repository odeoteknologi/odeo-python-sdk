from odeo.models.sub_user import SubUser
from odeo.services.base_service import BaseService, authenticated


class SubUserService(BaseService):

    @authenticated
    def list_sub_users(self, page_token: str = None):
        params = {'page_token': page_token} if page_token is not None else {}
        content = self.request('GET', '/sub-users', params).json()
        sub_users = list(map(lambda sub_user: SubUser.from_json(sub_user), content['sub_users']))

        return sub_users, content['next_page_token']

    @authenticated
    def create_sub_user(self, email: str, name: str, phone_number: str):
        response = self.request(
            'POST', '/sub-users', {'email': email, 'name': name, 'phone_number': phone_number}
        )

        return self._raise_exception_on_error(response, lambda c: SubUser.from_json(c))

    @authenticated
    def update_sub_user(self, user_id: int, email: str, name: str, phone_number: str):
        response = self.request(
            'PUT',
            f'/sub-users/{user_id}',
            {'email': email, 'name': name, 'phone_number': phone_number}
        )

        return self._raise_exception_on_error(response, lambda c: SubUser.from_json(c))
