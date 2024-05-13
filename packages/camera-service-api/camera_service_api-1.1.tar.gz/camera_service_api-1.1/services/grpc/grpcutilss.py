from datetime import datetime
from typing import List, Union

from services.cameras.models import CameraMeta
from services.grpc import camera_service_pb2 as service_pb2
from services.grpc.pb2utils import value_or_empty


class local_to_pb2:
    @staticmethod
    def to_CameraMeta(s: CameraMeta) -> service_pb2.CameraMeta:
        x = service_pb2.CameraMeta()
        x.cameraType = value_or_empty(s.cameraType)
        x.serialNumber = value_or_empty(s.serialNumber)  # value_or_empty_dict(s, 'name')
        x.modelName = value_or_empty(s.modelName)
        x.manufactureName = value_or_empty(s.manufactureName)
        x.deviceVersion = value_or_empty(s.deviceVersion)
        x.userDefinedName = value_or_empty(s.userDefinedName)
        if s.info is not None:
            for kk in s.info:
                vv = s.info[kk]
                x.info[kk] = vv

        return x

    @staticmethod
    def to_CameraMetas(metas: List[CameraMeta]) -> service_pb2.CameraMetas:
        output = []
        if metas is not None or len(metas) > 0:
            for a in metas:
                output.append(local_to_pb2.to_CameraMeta(a))

        return service_pb2.CameraMetas(data=output)

    @staticmethod
    def to_BytesBody(content: bytes) -> service_pb2.BytesBody:
        x = service_pb2.BytesBody(content=content)
        return x

    @staticmethod
    def to_InputString(value: str) -> service_pb2.InputString:
        x = service_pb2.InputString(value=value)
        return x
