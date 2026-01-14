import requests

import urls


class StellarBurgersClient:
    @staticmethod
    def user_create(payload):
        return requests.post(urls.USER_CREATE, json=payload)

    @staticmethod
    def user_login(payload):
        return requests.post(urls.USER_LOGIN, json=payload)

    @staticmethod
    def order_create(payload, headers):
        return requests.post(urls.ORDER_CREATE, json=payload, headers=headers)

    @staticmethod
    def ingredients_list():
        response = requests.get(urls.INGREDIENTS_LIST)
        return [item["_id"] for item in response.json()["data"]]
