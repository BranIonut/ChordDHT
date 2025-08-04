import grpc
import nmap
from business.node import Node
from business.node_network_interface import NodeNetworkInterface
from presentation import chord_pb2
from presentation.chord_pb2_grpc import ChordStub


class DockerNetwork(NodeNetworkInterface):
    def __init__(self):
        self.stubs = {}
        self.local_node = None
        self.address_map = {}

    def discover_bootstrap(self):
        print(f'Scanning network for other bootstraps...')
        nm = nmap.PortScanner()
        nm.scan('172.18.0.2-254', arguments='-sn')
        for host in nm.all_hosts():
            print(f'Discovered host: {host}')
            last_octet = int(host.split('.')[-1])
            node_id = last_octet - 1

            if node_id > 0 and node_id != self.local_node.node_id:
                try:
                    self.get_predecessor(node_id)
                    self.address_map[node_id] = self._resolve_address(node_id)
                    return node_id
                except grpc.RpcError:
                    continue
        print(f'No bootstraps found. Joining by itself...')
        return None

    @staticmethod
    def _resolve_address(node_id: int) -> str:
        return f"172.18.0.{node_id + 1}:50050"

    def _get_stub(self, node_id: int) -> ChordStub:
        if node_id not in self.stubs:
            address = self._resolve_address(node_id)
            channel = grpc.insecure_channel(address)
            self.stubs[node_id] = ChordStub(channel)
        return self.stubs[node_id]

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
