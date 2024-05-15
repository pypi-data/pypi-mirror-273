from .base_api import BaseAPI


class PartnerAPI(BaseAPI):
    def list_partners(self, limit: int = 15, page: int = 1) -> dict:
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', 'partners', params=params)

    def create_partner(self, email: str, name: str, password: str, id: str = None, key: str = None) -> dict:
        data = {
            'email': email,
            'name': name,
            'password': password,
            'id': id,
            'key': key
        }
        return self.send_request('POST', 'partners', data=data)

    def get_partner(self, email: str = None, name: str = None, partner_id: str = None) -> dict:
        """
        Search for partners based on provided parameters. Parameters are optional.
        :param email: Email of the partner to search for.
        :param name: Name of the partner to search for.
        :param partner_id: ID of the partner to search for.
        """
        params = {k: v for k, v in [('email', email), ('name', name), ('id', partner_id)] if v is not None}
        return self.send_request('GET', 'partners:search', params=params)

    def update_partner(self, partner_id: str, email: str = None, name: str = None, surname: str = None, password: str = None) -> dict:
        data = {k: v for k, v in [('email', email), ('name', name), ('surname', surname), ('password', password)] if v is not None}
        return self.send_request('PUT', f'partners/{partner_id}', data=data)

    def delete_partner(self, partner_id: str) -> dict:
        return self.send_request('DELETE', f'partners/{partner_id}')
