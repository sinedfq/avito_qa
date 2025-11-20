import pytest
import requests

class TestGetRequests:

    def test_get_valid(self, base_url, valid_item_id):
        """ТС-21: Валидный GET запрос на получение объявления"""
        response = requests.get(f"{base_url}/api/1/item/{valid_item_id}")

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        items_list = response.json()

        assert isinstance(items_list, list), "Ответ должен быть списком"
        assert len(items_list) > 0, "Список объявлений не должен быть пустым"

        item_data = items_list[0]

        expected_fields = ["id", "sellerId", "name", "price", "createdAt", "statistics"]
        for field in expected_fields:
            assert field in item_data, f"В ответе отсутствует поле {field}"

        statistics_fields = ["likes", "viewCount", "contacts"]
        for field in statistics_fields:
            assert field in item_data["statistics"], f"В statistics отсутствует поле {field}"

    def test_get_invalid(self, base_url, invalid_item_id):
        """ТС-22: Невалидный GET запрос на получение объявления. UUID новости сгенерирован"""
        response = requests.get(f"{base_url}/api/1/item/{invalid_item_id}")

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"


    def test_get_valid_statistic_first(self, base_url, valid_item_id):
        """ТС-23: Валидный GET запрос на получение статистики объявления. """
        response = requests.get(f"{base_url}/api/1/statistic/{valid_item_id}")

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        statistics_list = response.json()

        assert isinstance(statistics_list, list), "Ответ должен быть списком"
        assert len(statistics_list) > 0, "Список объявлений не должен быть пустым"

        statistic_data = statistics_list[0]

        expected_fields = ["likes", "viewCount", "contacts"]
        for field in expected_fields:
            assert field in statistic_data, f"В statistics отсутствует поле {field}"


    def test_get_invalid_statistic_first(self, base_url, invalid_item_id):
        """ТС-24: Невалидный GET запрос на получение статистики объявления. UUID новости сгенерирован"""
        response = requests.get(f"{base_url}/api/1/statistic/{invalid_item_id}")

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"


    def test_get_valid_seller_ads(self, base_url, invalid_item_id, valid_seller_id):
        """ТС-25: Валидный GET запрос на получение всех объявлений пользователя."""
        response = requests.get(f"{base_url}/api/1/{valid_seller_id}/item")

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data_list = response.json()

        assert isinstance(data_list, list), "Ответ должен быть списком"
        assert len(data_list) > 0, "Список объявлений не должен быть пустым"

        ads_list = data_list[0]

        expected_fields = ["id", "sellerId", "name", "price", "createdAt"]
        for field in expected_fields:
            assert field in ads_list, f"В ответе отсутствует поле {field}"

        statistics_fields = ["likes", "viewCount", "contacts"]
        for field in statistics_fields:
            assert field in ads_list["statistics"], f"В statistics отсутствует поле {field}"


    @pytest.mark.xfail(reason="Баг: Отрицательный sellerID возвращает 200 вместо 400")
    def test_get_invalid_seller_ads(self, base_url, invalid_item_id, invalid_seller_id):
        """ТС-26: Невалидный GET запрос на получение всех объявлений пользователя."""
        response = requests.get(f"{base_url}/api/1/{invalid_seller_id}/item")

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"


    def test_get_valid_statistic_second(self, base_url, valid_item_id):
        """ТС-27: Валидный GET запрос на получение объявления"""
        response = requests.get(f"{base_url}/api/2/statistic/{valid_item_id}")

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        statistics_list = response.json()

        assert isinstance(statistics_list, list), "Ответ должен быть списком"
        assert len(statistics_list) > 0, "Список объявлений не должен быть пустым"

        statistic_data = statistics_list[0]

        expected_fields = ["likes", "viewCount", "contacts"]
        for field in expected_fields:
            assert field in statistic_data, f"В statistics отсутствует поле {field}"


    def test_get_invalid_statistic_second(self, base_url, invalid_item_id):
        """ТС-28: Невалидный GET запрос на получение статистики объявления. UUID новости сгенерирован"""
        response = requests.get(f"{base_url}/api/2/statistic/{invalid_item_id}")

        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
