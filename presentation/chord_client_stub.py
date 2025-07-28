import grpc

from business.node import Node
from business.node_network_interface import NodeNetworkInterface
from . import chord_pb2
from . import chord_pb2_grpc


class ChordClientStub(NodeNetworkInterface):
    def __init__(self, address_map: dict[int, str]):
        self.address_map = address_map
        self.local_node = None

    def _get_stub(self, node_id: int):
        try:
            address = self.address_map[node_id]
        except KeyError:
            raise grpc.RpcError

        channel = grpc.insecure_channel(address)
        return chord_pb2_grpc.ChordStub(channel)

    def set_local_node(self, node: Node):
        self.local_node = node

    def find_successor(self, target_id: int, key: int) -> int | None:
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.FindSuccessorRequest(target_id=str(target_id), key=str(key))
            res = stub.FindSuccessor(req, timeout=2)
            if res.successor_id == "None" or not res.successor_id:
                return None
            return int(res.successor_id)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def get_predecessor(self, target_id: int) -> int | None:

        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.FindPredecessorRequest(target_id=str(target_id))
            res = stub.FindPredecessor(req, timeout=2)
            if res.predecessor_id == "None":
                return None
            return int(res.predecessor_id)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def set_predecessor(self, target_id: int, new_predecessor_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.SetPredecessorRequest(target_id=str(target_id), new_predecessor_id=str(new_predecessor_id))
            stub.SetPredecessor(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def set_successor(self, target_id: int, successor_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.SetSuccessorRequest(target_id=str(target_id), new_successor_id=str(successor_id))
            stub.SetSuccessor(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def notify(self, target_id: int, sender_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.NotifyRequest(target_id=str(target_id), sender_id=str(sender_id))
            stub.Notify(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def update_finger_table(self, target_id: int, new_node_id: int, index: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.UpdateFingerTableRequest(target_id=str(target_id), new_node_id=str(new_node_id),
                                                     index=str(index))
            stub.UpdateFingerTable(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)
            return None

    def get_information(self, target_node_id: int, info_key: int) -> [str | None]:
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.GetInfoRequest(target_id=str(target_node_id), key=str(info_key))
            res = stub.GetInformation(req, timeout=2)
            return res.information
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_node_id)

    def add_information(self, target_node_id: int, info_key: int, info: str):
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.AddInfoRequest(info_key=str(info_key), info=str(info))
            stub.AddInformation(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_node_id)

    def remove_information(self, target_node_id: int, info_key: int):
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.RemoveInfoRequest(target_id=str(target_node_id), info_key=str(info_key))
            stub.RemoveInformation(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_node_id)
