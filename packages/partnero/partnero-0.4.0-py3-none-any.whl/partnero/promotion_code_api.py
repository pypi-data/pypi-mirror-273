from .base_api import BaseAPI


class PromotionCodeAPI(BaseAPI):
    def list_promotion_codes(self, limit: int = 15, page: int = 1) -> dict:
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', 'promotion-codes', params=params)

    def create_promotion_code(self, coupon_id: int, code: str, restrictions: dict) -> dict:
        data = {'coupon_id': coupon_id, 'code': code, **restrictions}
        return self.send_request('POST', 'promotion-codes', data=data)

    def fetch_promotion_code(self, promotion_code: str) -> dict:
        return self.send_request('GET', f'promotion-codes/{promotion_code}')

    def update_promotion_code(self, promotion_code: str, updates: dict) -> dict:
        return self.send_request('PUT', f'promotion-codes/{promotion_code}', data=updates)

    def delete_promotion_code(self, promotion_code: str) -> dict:
        return self.send_request('DELETE', f'promotion-codes/{promotion_code}')
