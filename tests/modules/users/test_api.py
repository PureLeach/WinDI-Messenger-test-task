from fastapi import status


async def test_create_user(test_client):
    payload = {"name": "Alice", "email": "alice@example.com", "password": "securepassword123"}

    response = await test_client.post("/users/", json=payload)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == payload["name"]
    assert result["email"] == payload["email"]
