import abc

from ..domain.message import AoLabThingMessage


class AoLabSerialProtocol:
    @abc.abstractmethod
    def marshal(self, type, device_id, node_id, command):
        pass

    @abc.abstractmethod
    def unmarshal(self, message: str) -> AoLabThingMessage:
        pass
