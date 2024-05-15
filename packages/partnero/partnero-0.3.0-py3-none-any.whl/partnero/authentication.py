from typing import Dict


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Authentication(metaclass=SingletonMeta):
    api_key = None

    @classmethod
    def configure(cls, api_key):
        cls.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("API key has not been set.")
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
