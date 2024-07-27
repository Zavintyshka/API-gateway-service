import grpc
from .settings import VIDEO_MICROSERVICE_URL, AUDIO_MICROSERVICE_URL, IMAGE_MICROSERVICE_URL
from .video_grpc import VideoServiceStub, VideoRequest
from database.database_types import ServiceType


class GrpcBase:
    def __init__(self, service_type: ServiceType,
                 max_send_message_length: int = 1024 ** 3,
                 max_receive_message_length: int = 1024 ** 3):
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

    def init_grpc(self):
        raise NotImplementedError

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

    def make_requests(self):
        raise NotImplementedError
