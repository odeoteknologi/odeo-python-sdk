from odeo.models.list_sub_user_response import ListSubUserResponse
from odeo.models.sub_user import SubUser
from odeo.services.base_service import BaseService, authenticated


class SubUserService(BaseService):

    @authenticated
    def list_sub_users(self, page_token: str = None):
        params = {'page_token': page_token} if page_token is not None else {}
        response = self.request('GET', '/sub-users', params)

        return ListSubUserResponse.from_json(response.json())

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
