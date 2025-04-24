from fastapi import status


async def test_get_message_history(test_client, create_chats, create_messages):
    chat_1, _ = create_chats
    response = await test_client.get(f"/messages/history/{str(chat_1.id)}", params={"limit": 3, "offset": 0})
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(result, list)
    assert len(result) == 3
    assert "id" in result[0]
    assert "text" in result[0]


async def test_get_message_history_no_messages(test_client, create_chats):
    chat_1, _ = create_chats
    response = await test_client.get(f"/messages/history/{str(chat_1.id)}", params={"limit": 3, "offset": 0})
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(result, list)
    assert result == []
