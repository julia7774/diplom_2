import allure
import pytest

import utils
from client import StellarBurgersClient


@pytest.fixture
def user():
    email = utils.generate_email()
    login = utils.generate_login()
    password = utils.generate_password()

    with allure.step("Создание тестового пользователя"):
        response = StellarBurgersClient.user_create({"email": email, "name": login, "password": password})

    if response.status_code != 200:
        pytest.fail("Ошибка создания тестового пользователя")

    return email, login, password, response.json()["accessToken"]
