from http.client import responses

import pytest
import requests
import re


class TestAvitoAPI:

    def test_post_valid(self, base_url, base_item_data):

        """ТС-1: Валидный POST запрос на создание объявления"""
        response = requests.post(f"{base_url}/api/1/item", json=base_item_data)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        response_data = response.json()
        assert "status" in response_data, "В ответе отсутствует поле status"
        status_message = response_data["status"]
        assert "Сохранили объявление" in status_message, "Некорректное сообщение статуса"
        uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        match = re.search(uuid_pattern, status_message)
        assert match is not None, "В сообщении отсутствует UUID"

        item_id = match.group()
        print(f"Создано объявление с ID: {item_id}")

    def test_post_invalid_seller_id(self, base_url, base_item_data):
        """ТС-2: Невалидный POST запрос на создание объявления. Неверный sellerID"""
        data = base_item_data.copy()
        data["sellerID"] = "41231ab"
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    @pytest.mark.xfail(reason="Баг: Отрицательный sellerID возвращает 200 вместо 400")
    def test_post_negative_seller_id(self, base_url, base_item_data):
        """ТС-3: Невалидный POST запрос на создание объявления. Отрицательный sellerID"""
        data = base_item_data.copy()
        data["sellerID"] = -412312
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"


    def test_post_without_seller_id(self, base_url, base_item_data):
        """ТС-4: Невалидный POST запрос. Отсутствует поле sellerID"""
        data = base_item_data.copy()
        del data["sellerID"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_invalid_name(self, base_url, base_item_data):
        """ТС-5: Невалидный POST запрос. Невалидное поле name"""

        data = base_item_data.copy()
        data["name"] = 1234
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_empty_name(self, base_url, base_item_data):
        """ТС-6: Невалидный POST запрос. Поле name содержит пустую строку"""

        data = base_item_data.copy()
        data["name"] = ""
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_without_name(self, base_url, base_item_data):
        """ТС-7: Невалидный POST запрос. Отсутствует поле name"""

        data = base_item_data.copy()
        del data["name"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_invalid_price(self, base_url, base_item_data):
        """ТС-8: Невалидный POST запрос. Поле price содержит строку"""

        data = base_item_data.copy()
        data["price"] = "9000"
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    @pytest.mark.xfail(reason="Баг: Отрицательный price возвращает 200 вместо 400")
    def test_post_negative_price(self, base_url, base_item_data):
        """ТС-9: Невалидный POST запрос. Поле price содержит отрицательное число"""

        data = base_item_data.copy()
        data["price"] = -9000
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_empy_price(self, base_url, base_item_data):
        """ТС-10: Невалидный POST запрос. Поле price = 0"""

        data = base_item_data.copy()
        data["price"] = 0
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_without_price(self, base_url, base_item_data):
        """ТС-11: Невалидный POST запрос. Поле price = 0"""

        data = base_item_data.copy()
        del data["price"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_invalid_likes(self, base_url, base_item_data):
        """ТС-12: Невалидный POST запрос. Невалидное поле likes"""

        data = base_item_data.copy()
        data["statistics"]["likes"] = "21"
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    @pytest.mark.xfail(reason="Баг: Отрицательный likes возвращает 200 вместо 400")
    def test_post_negative_likes(self, base_url, base_item_data):
        """ТС-13: Невалидный POST запрос. Поле likes содержит отрицательное число"""

        data = base_item_data.copy()
        data["statistics"]["likes"] = -21
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_without_likes(self, base_url, base_item_data):
        """ТС-14: Невалидный POST запрос. Поле likes отсутствует"""

        data = base_item_data.copy()
        del data["statistics"]["likes"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_invalid_view(self, base_url, base_item_data):
        """ТС-15: Невалидный POST запрос. Поле viewCount содержит строку"""

        data = base_item_data.copy()
        data["statistics"]["viewCount"] = "21"
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    @pytest.mark.xfail(reason="Баг: Отрицательный viewCount возвращает 200 вместо 400")
    def test_post_negative_view(self, base_url, base_item_data):
        """ТС-16: Невалидный POST запрос. Поле viewCount содержит отрицательное число"""

        data = base_item_data.copy()
        data["statistics"]["viewCount"] = -21
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_without_view(self, base_url, base_item_data):
        """ТС-17: Невалидный POST запрос. Поле viewCount отсутствует"""

        data = base_item_data.copy()
        del data["statistics"]["viewCount"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_invalid_contacts(self, base_url, base_item_data):
        """ТС-18: Невалидный POST запрос. Поле contacts содержит строку"""

        data = base_item_data.copy()
        data["statistics"]["contacts"] = "21"
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    def test_post_without_contacts(self, base_url, base_item_data):
        """ТС-19: Невалидный POST запрос. Поле contacts отсутствует"""

        data = base_item_data.copy()
        del data["statistics"]["contacts"]
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

    @pytest.mark.xfail(reason="Баг: Отрицательный contacts возвращает 200 вместо 400")
    def test_post_negative_contacts(self, base_url, base_item_data):
        """ТС-20: Невалидный POST запрос. Поле contacts содержит отрицательное число"""

        data = base_item_data.copy()
        data["statistics"]["contacts"] = -21
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

