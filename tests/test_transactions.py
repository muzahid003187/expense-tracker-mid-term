from datetime import date

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def get_token():
    username = "testuser123"
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": "testuser123@gmail.com",
            "password": password
        }
    )

    if register_response.status_code not in [200, 400]:
        raise Exception("Registration failed")

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    return login_response.json()["access_token"]

def create_test_transaction():
    token = get_token()

    response = client.post(
        "/transactions",
        json={
            "title": "Test Food",
            "amount": 500,
            "type": "expense",
            "category": "Food",
            "date": str(date.today())
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response, token


def test_create_transaction():
    response, token = create_test_transaction()

    assert response.status_code == 200
    assert response.json()["title"] == "Test Food"


def test_get_transactions():
    response, token = create_test_transaction()

    response = client.get(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_specific_transaction():
    response, token = create_test_transaction()

    transaction_id = response.json()["id"]

    response = client.get(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id


def test_update_transaction():
    response, token = create_test_transaction()

    transaction_id = response.json()["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "title": "Updated Food",
            "amount": 800,
            "type": "expense",
            "category": "Food",
            "date": str(date.today())
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Food"
    assert response.json()["amount"] == 800


def test_delete_transaction():
    response, token = create_test_transaction()

    transaction_id = response.json()["id"]

    response = client.delete(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"