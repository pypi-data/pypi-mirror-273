# Partnero SDK

The Partnero SDK provides a simple and powerful Python interface to the Partnero API, allowing developers to manage customers, partners, transactions, webhooks, coupons, and promotion codes programmatically. It simplifies interactions by providing a centralized client (`PartneroClient`) that handles configuration and request management.

[Partnero API Documentation](https://developers.partnero.com/reference/general.html)

## Installation

To install the Partnero SDK, run the following command:

```bash
pip install partnero
```

## Configuration

Before using the SDK, configure the `PartneroClient` with your API token:

```python
from partnero import PartneroClient

# Replace 'your_api_token_here' with your actual API token
client = PartneroClient(api_key='your_api_token_here')
```

## Usage

With `PartneroClient`, you can easily access different parts of the Partnero API. Here's how you can use it to manage customers, partners, transactions, and webhooks:

### Customer Management

**List Customers**

```python
customers = client.customers.list_customers(limit=10, page=1)
print(customers)
```

**Create a New Customer**

```python
new_customer = client.customers.create_customer(
    partner_key='your_partner_key',
    customer_key='unique_customer_key',
    email='customer@example.com',
    name='Customer Name'
)
print(new_customer)
```

### Partner Management

**List Partners**

```python
partners = client.partners.list_partners(limit=5, page=1)
print(partners)
```

**Register a New Partner**

```python
new_partner = client.partners.create_partner(
    email='newpartner@example.com',
    name='New Partner',
    password='securepassword123'
)
print(new_partner)
```

### Transaction Management

**List Transactions**

```python
transactions = client.transactions.list_transactions(limit=5, page=1)
print(transactions)
```

**Create a Transaction**

```python
new_transaction = client.transactions.create_transaction(
    customer_key='customer_key',
    transaction_key='unique_transaction_key',
    amount=39.99,
    product_id='product_id',
    product_type='type',
    action='purchase'
)
print(new_transaction)
```

### Webhook Management

**List Webhooks**

```python
webhooks = client.webhooks.list_webhooks(limit=5, page=1)
print(webhooks)
```

**Create a Webhook**

```python
new_webhook = client.webhooks.create_webhook(
    name='Order Placed',
    url='https://yourdomain.com/webhooks/order_placed',
    events=['order_placed'],
    is_active=True
)
print(new_webhook)
```

## Contributions

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This SDK is released under the MIT License. See the LICENSE file for more details.

---