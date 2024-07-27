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


class VideoMicroserviceGrpc(GrpcBase):
    def __init__(self,
                 max_send_message_length: int = 1024 ** 3,
                 max_receive_message_length: int = 1024 ** 3):
        super().__init__(service_type=ServiceType.video,
                         max_send_message_length=max_send_message_length,
                         max_receive_message_length=max_receive_message_length)
        # specific parameters
        self.__grpc_message = VideoRequest

        self.init_grpc()

    def init_grpc(self):
        self.establish_connection()
        self.set_stub()

    #  --TEST METHODS--
    def generate_request(self):
        command = "some_command_code"
        with open("./storage/video_files/54/raw_files/a2691bb2-ffd3-4515-bd18-a6166bef63ed.mp4", "rb") as file:
            while chunk := file.read(1024 * 1024):
                yield self.__grpc_message(chunk=chunk, command=command)

    def make_requests(self):
        response = self.stub.ProcessVideo(self.generate_request())
        with open("./storage/video_files/54/processed_files/a2691bb2-ffd3-4515-bd18-a6166bef63ed.mp3", "wb") as file:
            for data in response:
                chunk = data.chunk
                print(data.detail)
                file.write(chunk)
        self.channel.close()
    #  --TEST METHODS--
