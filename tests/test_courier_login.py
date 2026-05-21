import requests
import pytest
import allure

from helpers import register_new_courier_and_return_login_password, generate_random_string

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

class TestLoginCourier:

    @allure.title("Проверка успешной авторизации курьера и возвращения id")
    def test_courier_can_login_successfully(self):
        
        allure.step("Регистрация курьера")
        courier_data = register_new_courier_and_return_login_password()
        
        allure.step("Подготовка данных для авторизации")
        payload = {
            "login": courier_data[0],     
            "password": courier_data[1]  
        }

        allure.step("Отправление POST - запроса на создание курьера")
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        allure.step("Проверка статус-кода ответа и наличия id курьера")
        assert response.status_code == 200
        assert "id" in response.json()
        

    @allure.title("Ошибка авторизации курьера при указании неверного логина или пароля: {wrong_data}")
    @pytest.mark.parametrize("wrong_data", ["login", "password"])
    def test_courier_authorization_with_wrong_login_or_password(self, wrong_data):

        allure.step("Регистрация курьера")
        courier_data = register_new_courier_and_return_login_password()
        
        allure.step("Подготовка данных авторизации")        
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        allure.step(f"Подмена поля '{wrong_data}' на неправильное случайное значение")
        payload[wrong_data] = generate_random_string(10)

        allure.step("Отправка POST - запроса с неверными данными")
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        allure.step("Проверка статус кода и появления сообщения об ошибке")
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"


    
    @allure.title("Ошибка авторизации курьера при отсутствии обязательного поля: {empty_data}")
    @pytest.mark.parametrize("empty_data", ["login", "password"])
    def test_courier_authorization_with_empty_login_or_password(self,empty_data):

        allure.step("Регистрация курьера")
        courier_data = register_new_courier_and_return_login_password()

        allure.step("Подготовка данных авторизации")         
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        allure.step(f"Подмена поля '{empty_data}' на неправильное случайное значение")
        payload.pop(empty_data)

        allure.step("Отправка POST - запроса с пустым обязательным полем")
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        allure.step("Проверка статус кода и появления сообщения об ошибке")

        assert response.status_code in [400,504]
        if response.status_code == 400:
            assert response.json().get("message") == "Недостаточно данных для входа"

    
    @allure.title("Ошибка авторизации курьера под несуществующим пользователем")
    def test_authorization_with_no_existing_user(self):
        
        allure.step("Генерация случйных несуществующих учетных данных")
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }

        allure.step("Отправка POST - запроса с данными несуществвующего курьера")
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        allure.step("Проверка статус кода и появления сообщения об ошибке")
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"
