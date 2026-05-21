
import requests
import pytest
import allure

from helpers import register_new_courier_and_return_login_password, generate_random_string

BASE_URL = 'https://qa-scooter.praktikum-services.ru'


class TestCreateCourier:

    @allure.title("Успешное создание курьера со всеми обязтельными полями")
    def test_courier_can_be_created_successfully(self):
        
        allure.step("Генерация случайных данных нового курьера")
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        allure.step("Отправка POST-запроса на создание курьера")
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        allure.step("Проверка статус кода и тела ответа")
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Проверка на запрет создания двух абсолютно одинаковых курьеров")
    def test_cannot_create_two_identical_couriers(self):

        allure.step("Регистрация первого курьера")
        courier_data = register_new_courier_and_return_login_password()
        
        allure.step("Подготовка данных дубликата курьера")
        payload = {
            "login": courier_data[0],       
            "password": courier_data[1],    
            "firstName": courier_data[2]    
        }
        
        allure.step("Отправление POST-запроса на создание курьера-дубликата")
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        allure.step("Проверка статус кода и появления сообщения об ошибке")
        assert response.status_code == 409
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    
    @allure.title("Проверка нвозможности создания курьера с логином, который уже занят")
    def test_cannot_create_courier_with_existing_login(self):
        
        allure.step("Регистрация курьера")
        courier_data = register_new_courier_and_return_login_password()
        existing_login = courier_data[0]
        
        allure.step("Подготовка данных нового курьера с уже занятым логином")
        payload = {
            "login": existing_login,
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        
        allure.step("Отправка POST-запроса на создание нового курьера с уже занятым логином")
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        allure.step("Проверка статус кода ответа и появления сообщения об ошибке")
        assert response.status_code == 409
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."


    @allure.title("Проверка невозможности создания курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_cannot_create_courier_without_mandatory_fields(self, missing_field):
        
        allure.step("Генерация данных нового курьера ")
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        allure.step(f"Удаление обязательного поля '{missing_field}' из запроса")
        payload.pop(missing_field)
        
        allure.step(f"Отправка POST - запроса на создание курьера без обязательного поля '{missing_field}")
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        allure.step("Проверка статус кода ответа и появления сообщения об ошибке")
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи"
