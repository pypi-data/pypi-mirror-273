from datetime import datetime
from typing import List, Union

from services.cameras.models import CameraMeta
from services.grpc import camera_service_pb2 as service_pb2
from services.grpc.pb2utils import value_or_empty


class pb2_to_local:

    @staticmethod
    def InputString_to_str(s: service_pb2.InputString) -> str:
        return s.value
    #

    @staticmethod
    def to_CameraMeta(s: service_pb2.CameraMeta) -> CameraMeta:
        x = CameraMeta()
        x.cameraType = s.cameraType
        x.serialNumber = s.serialNumber  # value_or_empty_dict(s, 'name')
        x.modelName = s.modelName
        x.manufactureName = s.manufactureName
        x.deviceVersion = s.deviceVersion
        x.userDefinedName = s.userDefinedName

        for key in s.info:
            x.info[key] = s.info[key]

        return x


    @staticmethod
    def to_CameraMetas(metas: service_pb2.CameraMetas) -> List[CameraMeta]:
        output = []
        inp = metas.data
        if inp is None or len(inp) == 0:
            return output;
        for a in inp:
            output.append(pb2_to_local.to_CameraMeta(a))
        return output

    @staticmethod
    def to_Bytes (s: service_pb2.BytesBody) -> bytes :
        return s.content
