from fastapi import status

from project.modules.chats.models import ChatType


async def test_create_chat(test_client, create_users):
    user_1, user_2, _ = create_users
    payload = {"name": "My Chat", "type": ChatType.personal, "participant_ids": [str(user_1.id), str(user_2.id)]}

    response = await test_client.post("/chats/", json=payload)
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == payload["name"]
    assert result["type"] == payload["type"]
    assert set(result["participantIds"]) == set(payload["participant_ids"])


async def test_add_user_to_chat(test_client, create_users):
    user_1, user_2, user_3 = create_users
    create_payload = {"name": "Group Chat", "type": "group", "participant_ids": [str(user_1.id), str(user_2.id)]}

    create_response = await test_client.post("/chats/", json=create_payload)
    chat_result = create_response.json()
    chat_id = chat_result["id"]

    add_response = await test_client.post(f"/chats/{chat_id}/users/{str(user_3.id)}")
    result = add_response.json()

    assert add_response.status_code == status.HTTP_200_OK
    assert str(user_3.id) in result["participantIds"]
    assert set(result["participantIds"]) == set(create_payload["participant_ids"] + [str(user_3.id)])


async def test_get_chats_for_user(test_client, create_users):
    user_1, _, _ = create_users
    payload = {"type": ChatType.personal, "participant_ids": [str(user_1.id)]}

    await test_client.post("/chats/", json=payload)

    response = await test_client.get(f"/chats/?user_id={str(user_1.id)}")
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(result, list)
    assert any(str(user_1.id) in chat["participantIds"] for chat in result)
