import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

class TestOrderList:
    
    @allure.title("Проверка наличия в теле ответа списка заказов")
    def test_get_order_list(self):
        
        allure.step("Отправка Get - запроса на получение списка заказов")
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')

        allure.step("Проверка статус кода")
        assert response.status_code == 200
        assert 'orders' in response.json()