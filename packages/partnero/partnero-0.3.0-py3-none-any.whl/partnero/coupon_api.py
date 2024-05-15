from .base_api import BaseAPI


class CouponAPI(BaseAPI):
    def list_coupons(self, limit: int = 15, page: int = 1) -> dict:
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', 'coupons', params=params)

    def create_coupon(self, name: str, discount_type: str, discount_amount: float, duration_type: str, duration_value: int, redemption_limit: int) -> dict:
        data = {
            'name': name,
            'coupon_discount_type': discount_type,
            'coupon_discount_amount': discount_amount,
            'coupon_duration_type': duration_type,
            'coupon_duration_value': duration_value,
            'redemption_times_value': redemption_limit
        }
        return self.send_request('POST', 'coupons', data=data)

    def fetch_coupon(self, coupon_uuid: str) -> dict:
        return self.send_request('GET', f'coupons/{coupon_uuid}')

    def update_coupon(self, coupon_uuid: str, name: str = None, active: bool = None) -> dict:
        data = {k: v for k, v in [('name', name), ('active', active)] if v is not None}
        return self.send_request('PUT', f'coupons/{coupon_uuid}', data=data)

    def delete_coupon(self, coupon_uuid: str) -> dict:
        return self.send_request('DELETE', f'coupons/{coupon_uuid}')
