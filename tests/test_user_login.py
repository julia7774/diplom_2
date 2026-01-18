import allure

import utils
from client import StellarBurgersClient


class TestUserLogin:
    @allure.title("Проверка авторизации пользователя")
    def test_success(self, user):
        email, login, password, _ = user

        with allure.step("Отправить POST запрос на автотризацию пользователя"):
            response = StellarBurgersClient.user_login({"email": email, "password": password})

        assert response.status_code == 200
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == True
        assert "accessToken" in json_
        assert json_["accessToken"].startswith("Bearer")
        assert "refreshToken" in json_
        assert json_["refreshToken"] != ""
        assert "user" in json_
        assert json_["user"] == {"email": email, "name": login}

    @allure.title("Проверка авторизации пользователя если указан невалидный логин")
    def test_invalid_login(self, user):
        _, _, password, _ = user

        with allure.step("Отправить POST запрос на авторизацию пользователя"):
            response = StellarBurgersClient.user_login({"email": utils.generate_email(), "password": password})

        assert response.status_code == 401
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == False
        assert "message" in json_
        assert json_["message"] == "email or password are incorrect"

    @allure.title("Проверка авторизации пользователя если указан невалидный логин")
    def test_invalid_password(self, user):
        email, _, _, _ = user

        with allure.step("Отправить POST запрос на авторизацию пользователя"):
            response = StellarBurgersClient.user_login({"email": email, "password": utils.generate_password()})

        assert response.status_code == 401
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == False
        assert "message" in json_
        assert json_["message"] == "email or password are incorrect"
