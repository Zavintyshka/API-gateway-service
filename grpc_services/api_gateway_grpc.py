import uuid
from pathlib import Path

import grpc

from api_gateway.api_gateway_types import MicroservicesStoragePath, FileStatePath, VideoActionType
from api_gateway.api_gateway_tools import generate_path
from api_gateway.schemas import ProcessedFileSchema
from .settings import VIDEO_MICROSERVICE_URL, AUDIO_MICROSERVICE_URL, IMAGE_MICROSERVICE_URL
from .video_grpc import VideoServiceStub, VideoRequest
from database.database_types import ServiceType, FileExtension


class GrpcBase:
    def __init__(self,
                 user_id: str,
                 action_type: VideoActionType,
                 action: str,
                 service_type: ServiceType,
                 max_send_message_length: int = 1024 ** 3,
                 max_receive_message_length: int = 1024 ** 3):
        # file parameters
        self.user_id = user_id
        self.action_type = action_type
        self.action = action
        self.file_ext, self.to_ext, *rest = self.action.split(";")

        # base parameters
        self.service_type = service_type
        self.ip = self.get_ip()
        self.max_send_message_length = max_send_message_length
        self.max_receive_message_length = max_receive_message_length
        # connection parameters
        self.channel = None
        self.stub = None
        # inner parameters
        self.__microservice_stub = self.get_microservice_stub()
        self.__grpc_message = None
        self.__microservice_path = None
        self.__microservice_type = None

    def init_grpc(self):
        self.establish_connection()

    def get_microservice_stub(self):
        match self.service_type:
            case ServiceType.video:
                return VideoServiceStub
            case ServiceType.audio:
                raise NotImplementedError
            case ServiceType.image:
                raise NotImplementedError

    def get_ip(self):
        match self.service_type:
            case ServiceType.video:
                return VIDEO_MICROSERVICE_URL
            case ServiceType.audio:
                return AUDIO_MICROSERVICE_URL
            case ServiceType.image:
                return IMAGE_MICROSERVICE_URL

    def establish_connection(self):
        self.channel = grpc.insecure_channel(target=self.ip,
                                             options=[
                                                 ('grpc.max_send_message_length', self.max_send_message_length),
                                                 ('grpc.max_receive_message_length', self.max_receive_message_length),
                                             ])

    def set_stub(self):
        # if not self.channel:
        #     raise # Соединение еще не установлено. Установите с помощью метода establish_connection
        self.stub = self.__microservice_stub(self.channel)

    def make_request(self, filename: str):
        raise NotImplementedError

    def generate_path(self, filename: str, file_state_path: FileStatePath) -> Path:
        raise NotImplementedError


class VideoMicroserviceGrpc(GrpcBase):
    def __init__(self,
                 user_id: str,
                 action_type: VideoActionType,
                 action: str,
                 max_send_message_length: int = 1024 ** 3,
                 max_receive_message_length: int = 1024 ** 3):
        super().__init__(user_id=user_id,
                         action_type=action_type,
                         action=action,
                         service_type=ServiceType.video,
                         max_send_message_length=max_send_message_length,
                         max_receive_message_length=max_receive_message_length)

        # specific parameters
        self.__grpc_message = VideoRequest
        self.__microservice_path = MicroservicesStoragePath.video_service
        self.__microservice_type = ServiceType.video
        self.init_grpc()

    def init_grpc(self):
        super().init_grpc()
        self.set_stub()

    def generate_path(self, filename: str, file_state_path: FileStatePath) -> Path:
        return generate_path(filename=filename,
                             microservice_path=self.__microservice_path,
                             user_id=self.user_id,
                             file_state_path=file_state_path)

    def generate_request(self, filename: str):
        raw_file_location = self.generate_path(filename=filename,
                                               file_state_path=FileStatePath.raw)
        with raw_file_location.open("rb") as file:
            while chunk := file.read(1024 * 1024):
                yield self.__grpc_message(chunk=chunk, action_type=self.action_type.value, action=self.action)

    def save_processed_file(self, filename: str, response_iterator):
        processed_file_location: Path = self.generate_path(filename=filename,
                                                           file_state_path=FileStatePath.processed)
        with processed_file_location.open("wb") as file:
            for response in response_iterator:
                chunk = response.chunk
                file.write(chunk)

    def make_request(self, raw_file_uuid: str) -> ProcessedFileSchema:
        filename = f"{raw_file_uuid}.{self.file_ext}"
        processed_file_uuid = uuid.uuid4()
        request = self.generate_request(filename)
        response_iterator = self.stub.ProcessVideo(request)
        self.save_processed_file(f"{processed_file_uuid}.{self.to_ext}", response_iterator)
        self.channel.close()
        processed_file_schema = ProcessedFileSchema(file_uuid=processed_file_uuid,
                                                    user_id=self.user_id,
                                                    file_extension=self.action.split(";")[1],
                                                    service_type=self.__microservice_type)
        return processed_file_schema
