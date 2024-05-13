from typing import List
import grpc
from google.protobuf import empty_pb2
from services.cameras.models import CameraMeta
from services.grpc import camera_service_pb2 as service_pb2
from services.grpc.camera_service_pb2_grpc import CameraServiceStub
from services.grpc.grpcutilsc import pb2_to_local
from services.grpc.pb2utils import RemoveError, wrapper_rpc_error

_EMPTY = empty_pb2.Empty()


class GrpcChannel:
    def __init__(self, host='localhost', port=49001):
        addr = f'{host}:{port}'

        self.channel = grpc.insecure_channel(addr)


class CameraServiceClient:

    def __init__(self, channel: GrpcChannel):
        self._stub = CameraServiceStub(channel.channel)
        pass

    @wrapper_rpc_error
    def get_camera_metas(self) -> List[CameraMeta]:
        response = self._stub.GetCameraMetas(_EMPTY)
        metas = pb2_to_local.to_CameraMetas(response)
        return metas

    @wrapper_rpc_error
    def get_image(self, sn: str) -> bytes:
        response = self._stub.GetImage(service_pb2.InputString(value=sn))
        output = pb2_to_local.to_Bytes(response)
        return output;

    @wrapper_rpc_error
    def reset(self):
        response = self._stub.Reset(_EMPTY)
        return;


def create_camera_service_api(host, port) -> CameraServiceClient:
    c = GrpcChannel(host, port)
    return CameraServiceClient(c)
