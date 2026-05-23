import requests
from helpers import generate_random_string

class CourierAPI:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'

    @staticmethod
    def register_new_courier_and_return_login_password():

        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{CourierAPI.BASE_URL}/api/v1/courier', json=payload)

        if response.status_code == 201:
            return [login, password, first_name]

        return []
