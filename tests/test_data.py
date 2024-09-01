from uuid import uuid4

from api_gateway.api_gateway_types import VideoActionType

user_register_data = {
    "username": "TestUser",
    "email": "TestUser@yandex.ru",
    "password": "Some123Password&*",
    "firstname": "Bob",
    "lastname": "Bob"
}

user_login_data = {"username": "TestUser", "password": "Some123Password&*"}

user_update_data = {"firstname": "John",
                    "lastname": "john",
                    "email": user_register_data["email"]}


def get_process_data():
    return {"file_uuid": str(uuid4()),
            "action_type": VideoActionType.convert.value,
            "action": "mp4;wav"
            }
