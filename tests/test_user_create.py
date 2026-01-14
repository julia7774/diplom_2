import allure
import pytest

import utils
from client import StellarBurgersClient


class TestUserCreate:
    @allure.title("Проверка создания пользователя")
    def test_success(self):
        email = utils.generate_email()
        login = utils.generate_login()
        password = utils.generate_password()

        with allure.step("Отправить POST запрос на создание пользователя"):
            response = StellarBurgersClient.user_create({"email": email, "name": login, "password": password})

        assert response.status_code == 200
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == True
        assert "user" in json_
        assert json_["user"] == {"email": email, "name": login}
        assert "accessToken" in json_
        assert json_["accessToken"].startswith("Bearer")
        assert "refreshToken" in json_
        assert json_["refreshToken"] != ""

    @allure.title("Проверка создания пользователя если пользователь существует")
    def test_already_exists(self, user):
        email, login, password, _ = user

        with allure.step("Отправить POST запрос на создание пользователя"):
            response = StellarBurgersClient.user_create({"email": email, "name": login, "password": password})

        assert response.status_code == 403
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == False
        assert "message" in json_
        assert json_["message"] == "User already exists"

    @allure.title("Проверка создания пользователя если нет одного из полей")
    @pytest.mark.parametrize(
        "payload, step",
        [
            ({"name": utils.generate_login(), "password": utils.generate_password()}, "почта"),
            ({"email": utils.generate_email(), "password": utils.generate_password()}, "логин"),
            ({"email": utils.generate_email(), "name": utils.generate_login()}, "пароль"),
            ({"email": utils.generate_email()}, "логин, пароль"),
            ({"name": utils.generate_login()}, "почта, пароль"),
            ({"password": utils.generate_password()}, "почта, логин"),
            ({}, "почта, логин, пароль")
        ]
    )
    def test_skip_required_field(self, payload, step):
        with allure.step(f"Отправить POST запрос на создание  пользователя без указания: {step}"):
            response = StellarBurgersClient.user_create(payload)

        assert response.status_code == 403
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == False
        assert "message" in json_
        assert json_["message"] == "Email, password and name are required fields"
