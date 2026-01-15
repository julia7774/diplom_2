import allure

from client import StellarBurgersClient


class TestOrderCreate:
    @allure.title("Проверка создания заказа")
    def test_success(self, user):
        _, _, _, token = user
        ingredients = StellarBurgersClient.ingredients_list()

        with allure.step("Отправить POST запрос на создание заказа"):
            response = StellarBurgersClient.order_create({"ingredients": ingredients}, {"Authorization": token})

        assert response.status_code == 200
        json_ = response.json()
        assert "name" in json_
        assert json_["name"] != ""
        assert "order" in json_
        assert "number" in json_["order"]
        assert json_["order"]["number"] > 0
        assert "success" in json_
        assert json_["success"] == True

    @allure.title("Проверка создания заказа если в запросе передан невалидный хэш ингредиента")
    def test_invalid_ingredient(self, user):
        _, _, _, token = user
        ingredients = ["invalid"]

        with allure.step("Отправить POST запрос на создание заказа"):
            response = StellarBurgersClient.order_create({"ingredients": ingredients}, {"Authorization": token})

        assert response.status_code == 500

    @allure.title("Проверка создания заказа если не передать ни один ингредиент")
    def test_empty_ingredients(self, user):
        _, _, _, token = user
        ingredients = []

        with allure.step("Отправить POST запрос на создание заказа"):
            response = StellarBurgersClient.order_create({"ingredients": ingredients}, {"Authorization": token})

        assert response.status_code == 400 
        json_ = response.json()
        assert "success" in json_
        assert json_["success"] == False
        assert "message" in json_
        assert json_["message"] == "Ingredient ids must be provided"
