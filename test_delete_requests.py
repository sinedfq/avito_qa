import re

import pytest
import requests

class TestDeleteRequests:
    def test_delete_valid_ads(self, base_url, base_item_data):
        """ТС-29: Полный flow - создание, получение ID, удаление объявления"""
        create_response = requests.post(f"{base_url}/api/1/item", json=base_item_data)
        assert create_response.status_code == 200, "Не удалось создать объявление"

        create_data = create_response.json()
        assert "status" in create_data, "В ответе отсутствует поле status"

        status_message = create_data["status"]
        uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        match = re.search(uuid_pattern, status_message)

        assert match is not None, "Не удалось извлечь ID из статусного сообщения"
        created_item_id = match.group()

        get_response = requests.get(f"{base_url}/api/1/item/{created_item_id}")
        assert get_response.status_code == 200, "Созданное объявление не найдено"

        items_list = get_response.json()
        assert isinstance(items_list, list) and len(items_list) > 0, "Список объявлений пуст"

        delete_response = requests.delete(f"{base_url}/api/2/item/{created_item_id}")
        assert delete_response.status_code == 200, f"Ожидался статус 200, получен {delete_response.status_code}"

        get_after_delete = requests.get(f"{base_url}/api/1/item/{created_item_id}")
        if get_after_delete.status_code == 200:
            items_after_delete = get_after_delete.json()
            assert len(items_after_delete) == 0, "Объявление не было удалено - список не пустой"
        else:
            assert get_after_delete.status_code == 404, f"После удаления ожидался 404, получен {get_after_delete.status_code}"


    def test_delete_invalid_ads(self, base_url, invalid_item_id):
        """ТС-30: Удаление невалидного объявления"""
        response = requests.delete(f"{base_url}/api/2/item/{invalid_item_id}")

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"