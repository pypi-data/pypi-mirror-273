from .utils import validate_email, validate_key
from .base_api import BaseAPI


class CustomerAPI(BaseAPI):
    """
    Provides access to customer operations within the Partnero API.
    """
    def list_customers(self, limit: int = 15, page: int = 1) -> dict:
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', 'customers', params=params)

    def create_customer(self, partner_key, customer_key, email, name):
        """
        Create a new customer associated with a partner.

        Parameters:
            partner_key (str): The partner's unique identifier.
            customer_key (str): The customer's unique identifier.
            email (str): The customer's email address.
            name (str): The customer's name.

        Returns:
            dict: The response from the API after creating the customer.
        """
        validate_email(email)
        validate_key(partner_key, "partner_key")
        validate_key(customer_key, "customer_key")
        data = {'partner': {'key': partner_key}, 'key': customer_key, 'email': email, 'name': name}
        return self.send_request('POST', 'customers', data=data)

    def get_customer(self, email: str = None, customer_key: str = None) -> dict:
        """
        Search for customer based on provided parameters. Parameters are optional.
        :param email: Email of the customer to search for.
        :param customer_key: ID of the customer to search for.
        """
        params = {k: v for k, v in [('email', email), ('key', customer_key)] if v is not None}
        return self.send_request('GET', 'customers:search', params=params)

    def get_customer_transactions(self, customer_key: str, limit: int = 15, page: int = 1) -> dict:
        """
        Retrieve transactions associated with a specific customer.

        Parameters:
            customer_key (str): The unique identifier of the customer.
            limit (int): The number of transaction records to retrieve per page.
            page (int): The page number to retrieve.

        Returns:
            dict: The response from the API containing a list of transactions.
        """
        params = {'limit': limit, 'page': page}
        return self.send_request('GET', f'customers/{customer_key}/transactions', params=params)

    def update_customer(self, customer_key: str, email: str = None, name: str = None) -> dict:
        data = {k: v for k, v in [('email', email), ('name', name)] if v is not None}
        return self.send_request('PUT', f'customers/{customer_key}', data=data)

    def delete_customer(self, customer_key: str) -> dict:
        return self.send_request('DELETE', f'customers/{customer_key}')