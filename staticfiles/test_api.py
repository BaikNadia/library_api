import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


def test_register():
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "password": "testpass123",
        "password2": "testpass123",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "user_type": "reader"
    }

    response = requests.post(url, json=data)
    print("=== REGISTER ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 201 else None


def test_login():
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }

    response = requests.post(url, json=data)
    print("\n=== LOGIN ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 200 else None


def test_protected_endpoint(access_token):
    url = f"{BASE_URL}/books/"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    print("\n=== PROTECTED ENDPOINT ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    # Сначала регистрируем пользователя
    register_result = test_register()

    # Затем логинимся
    login_result = test_login()

    # Тестируем защищенный endpoint
    if login_result and 'access' in login_result:
        test_protected_endpoint(login_result['access'])
