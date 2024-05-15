from .authentication import Authentication
from .coupon_api import CouponAPI
from .customer_api import CustomerAPI
from .partner_api import PartnerAPI
from .promotion_code_api import PromotionCodeAPI
from .transaction_api import TransactionAPI
from .webhook_api import WebhookAPI


class PartneroClient:
    def __init__(self, api_key: str):
        Authentication.configure(api_key=api_key)
        self.coupon = CouponAPI()
        self.customer = CustomerAPI()
        self.partner = PartnerAPI()
        self.promotion_code = PromotionCodeAPI()
        self.transaction = TransactionAPI()
        self.webhook = WebhookAPI()


__all__ = [
    "PartneroClient"
]
