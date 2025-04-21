async def test_create_user(test_client, db):
    response = await test_client.post("/users/", json={"name": "my_name"})
    result = response.json()

    assert result["name"] == "my_name"


async def test_get_users(test_client, db):
    response = await test_client.get("/users/")
    result = response.json()

    assert result[0]["name"] == "my_name"
