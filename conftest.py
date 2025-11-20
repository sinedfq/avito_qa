import pytest

BASE_URL = "https://qa-internship.avito.com"
VALID_SELLER_ID = 412312
INVALID_SELLER_ID = -412312
VALID_ITEM_ID = "7ed158a7-b17f-401a-b588-2ee256b5aa91"
INVALID_ITEM_ID = "10929ab7-00db-4e4f-9a64-a9a03eb006b5"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def valid_seller_id():
    return VALID_SELLER_ID

@pytest.fixture
def invalid_seller_id():
    return INVALID_SELLER_ID

@pytest.fixture
def valid_item_id():
    return VALID_ITEM_ID

@pytest.fixture
def invalid_item_id():
    return INVALID_ITEM_ID

@pytest.fixture
def base_item_data():
    """Базовые данные для создания объявления"""
    return {
        "sellerID": VALID_SELLER_ID,
        "name": "testItem",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43
        }
    }

@pytest.fixture
def invalid_item_data():
    """Данные с невалидным sellerID"""
    return {
        "sellerID": "41231ab",
        "name": "testItem",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43
        }
    }

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "bug(reason): mark test as having known bug"
    )