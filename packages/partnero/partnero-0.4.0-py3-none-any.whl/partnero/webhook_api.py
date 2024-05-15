from .base_api import BaseAPI


class WebhookAPI(BaseAPI):
    def list_webhooks(self, limit: int = 10, page: int = 1) -> dict:
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', 'webhooks', params=params)

    def create_webhook(self, name: str, url: str, events: list, is_active: bool = True) -> dict:
        data = {
            'name': name,
            'url': url,
            'events': events,
            'is_active': is_active
        }
        return self.send_request('POST', 'webhooks', data=data)

    def fetch_webhook(self, webhook_key: str) -> dict:
        return self.send_request('GET', f'webhooks/{webhook_key}')

    def update_webhook(self, webhook_key: str, name: str = None, url: str = None, is_active: bool = None, events: list = None) -> dict:
        data = {k: v for k, v in [('name', name), ('url', url), ('is_active', is_active), ('events', events)] if v is not None}
        return self.send_request('PUT', f'webhooks/{webhook_key}', data=data)

    def delete_webhook(self, webhook_key: str) -> dict:
        return self.send_request('DELETE', f'webhooks/{webhook_key}')
