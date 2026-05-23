import requests
import pytest
import data
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

class TestCreateOrder:

    
    @allure.title("Создание заказа с цветом: {color_value}")
    @pytest.mark.parametrize("color_value",(["BLACK"],["GREY"],["BLACK", "GREY"], []))
    def test_order_create(self, color_value):

        allure.step("Подготовка тестовых данных для заказа")
        order_info = data.order_data(color_value)

        allure.step("Отправка POST-запроса на создание заказа")
        response = requests.post(f'{BASE_URL}/api/v1/orders', json=order_info)

        allure.step("Проверка стаутс кода ответа")
        assert response.status_code == 201

        allure.step("Проверка наличия track-номера в теле ответа")
        assert "track" in response.json()