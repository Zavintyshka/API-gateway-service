from fastapi.testclient import TestClient
from alembic import command
from sqlalchemy.orm import Session
from pytest import fixture
from unittest import mock
from api_gateway.main import app
from api_gateway.schemas import ReturnUserSchema, ProcessedFileSchema
from database.database_types import FileExtension, ServiceType
from database.models import Users, RawStorage, UserAchievementProgress
from database.settings import alembic_config
from database.database import SessionLocal
from .test_data import *
from uuid import uuid4


@fixture(scope="session")
def client():
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")
    return TestClient(app)


@fixture(scope="session")
def db():
    session = SessionLocal()
    yield session
    session.close()


class TestUser:
    def test_user_registration(self, client: TestClient, db: Session):
        response = client.post("/registration/", json=user_register_data)
        assert response.status_code == 201
        assert bool(db.query(Users).filter(Users.email == user_register_data["email"]).first())

    @fixture
    def test_user_authentication(self, client: TestClient, db: Session):
        response = client.post("/login/", data=user_login_data)
        assert response.status_code == 200
        jwt_data = response.json()
        assert bool(jwt_data.get("access_token"))
        assert jwt_data.get("token_type") == "Bearer"
        return jwt_data["access_token"]

    def test_get_user_data(self, client: TestClient, db: Session, test_user_authentication: str):
        response = client.get("/user/account/", headers={"Authorization": f"Bearer {test_user_authentication}"})
        assert response.status_code == 200
        user_data = ReturnUserSchema(**response.json())
        assert user_data.firstname == "Bob"

    def test_update_user_data(self, client: TestClient, db: Session, test_user_authentication: str):
        response = client.put("/user/account/",
                              headers={"Authorization": f"Bearer {test_user_authentication}"},
                              json=user_update_data)
        assert response.status_code == 200
        user_data = ReturnUserSchema(**response.json())
        assert user_data.firstname == "John"

    @mock.patch("grpc_services.api_gateway_grpc.VideoMicroserviceGrpc.make_request")
    def test_user_achievement_progress(self, mock_make_request, client: TestClient, db: Session,
                                       test_user_authentication: str):
        user_id = str(db.query(Users).filter(Users.email == user_register_data["email"]).first().id)
        for count in range(1, 6):
            process_data = get_process_data()
            mock_make_request.return_value = ProcessedFileSchema(file_uuid=uuid4(),
                                                                 file_extension=FileExtension.wav,
                                                                 user_id=user_id,
                                                                 service_type=ServiceType.video
                                                                 )
            file_row = RawStorage(file_uuid=process_data["file_uuid"],
                                  filename="some_path",
                                  file_extension=FileExtension.mp4,
                                  user_id=user_id,
                                  service_type=ServiceType.video)
            db.add(file_row)
            db.commit()
            response = client.post("/video/processes_file/",
                                   headers={"Authorization": f"Bearer {test_user_authentication}"},
                                   json=process_data)

            assert response.status_code == 201
            user_achievement_entry = db.query(UserAchievementProgress).filter(
                UserAchievementProgress.user_id == int(user_id),
                UserAchievementProgress.achievement_name == "WAV Devotee").first()
            assert user_achievement_entry.progress == count
            if user_achievement_entry.progress == 5:
                assert user_achievement_entry.completed
