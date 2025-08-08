import logging

import grpc
from kubernetes import client, config
from business.node import Node
from business.node_network_interface import NodeNetworkInterface
from presentation import chord_pb2
from presentation.chord_pb2_grpc import ChordStub


class KubernetesNetwork(NodeNetworkInterface):
    def __init__(self, namespace="chord-dht", headless_service="chord-headless", app_label="chord-node"):
        self.stubs = {}
        self.local_node = None
        self.namespace = namespace
        self.headless_service = headless_service
        self.app_label = app_label
        self.k8s_client = None
        self.port = 50050
        self.address_map = {}

        self.init_k8s_client()

    def init_k8s_client(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config()
            except config.ConfigException:
                logging.exception("Failed to load kubeconfig")
                raise
        self.k8s_client = client.CoreV1Api()

    def _resolve_address(self, node_id: int) -> str:
        return f"chord-{node_id}.{self.headless_service}.{self.namespace}.svc.cluster.local:{self.port}"

    def _get_stub(self, node_id: int) -> ChordStub:
        if node_id not in self.stubs:
            dns_address = self._resolve_address(node_id)
            channel = grpc.insecure_channel(dns_address)
            self.stubs[node_id] = ChordStub(channel)
        return self.stubs[node_id]

    def set_local_node(self, node: Node):
        self.local_node = node

    def discover_bootstrap(self):
        try:
            pods = self.k8s_client.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.app_label}"
            )

            bootstrap_candidates = []
            for pod in pods.items:
                if pod.status.phase == 'Running' and pod.status.pod_ip and pod.metadata.name != f"chord-{self.local_node.node_id}":
                    try:
                        pod_name = pod.metadata.name
                        if pod_name.startswith(f"chord-"):
                            node_id = int(pod_name.split("-")[-1])
                            bootstrap_candidates.append(node_id)
                            logging.info(f"Discovered potential bootstrap node: {pod_name}")
                    except (ValueError, IndexError):
                        logging.warning(f"Could not parse node ID from pod name: {pod.metadata.name}")
                        continue

            for node_id in bootstrap_candidates:
                try:
                    result = self.get_predecessor(node_id)
                    self.address_map[node_id] = self._resolve_address(node_id)
                    logging.info(f"RESULT: {result}")
                    logging.info(f"Discovered bootstrap node: {node_id}")
                    return node_id
                except grpc.RpcError as rpc_error:
                    logging.debug(f"Node {node_id} not responsive: {rpc_error}")
                    continue

            logging.info("No responsive bootstrap nodes found. Starting as initial node.")
            return None

        except Exception as e:
            logging.error(f"Error during bootstrap discovery: {e}")
            return None

    def discover_all_nodes(self) -> list[int]:
        try:
            pods = self.k8s_client.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.app_label}"
            )

            node_ids = []

            for pod in pods.items:
                if pod.status.phase == 'Running' and pod.status.pod_ip:
                    try:
                        pod_name = pod.metadata.name
                        if pod_name.startswith(f"chord-"):
                            node_id = int(pod_name.split("-")[-1])
                            node_ids.append(node_id)
                    except (ValueError, IndexError):
                        continue

            return sorted(node_ids)

        except Exception as e:
            logging.error(f"Error during discover all nodes: {e}")
            return []

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

    def set_predecessor(self, target_id: int, new_predecessor_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.SetPredecessorRequest(target_id=str(target_id), new_predecessor_id=str(new_predecessor_id))
            stub.SetPredecessor(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)

    def set_successor(self, target_id: int, successor_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.SetSuccessorRequest(target_id=str(target_id), new_successor_id=str(successor_id))
            stub.SetSuccessor(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)

    def notify(self, target_id: int, sender_id: int):
        try:
            stub = self._get_stub(target_id)
            req = chord_pb2.NotifyRequest(target_id=str(target_id), sender_id=str(sender_id))
            stub.Notify(req, timeout=2)
        except grpc.RpcError:
            self.local_node.handle_dead_node(target_id)

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

    def get_all_info(self, target_node_id: int):
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.GetAllInfoRequest()
            res = stub.GetAllNodeInfo(req, timeout=2)
            return res.info_line
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

    def print_node_info(self, target_node_id: int):
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.GetNodeInfoRequest(target_id=str(target_node_id))
            stub.GetNodeInformation(req, timeout=2)
        except grpc.RpcError:
            if self.local_node:
                self.local_node.handle_dead_node(target_node_id)

    def print_stats(self, target_node_id: int):
        try:
            stub = self._get_stub(target_node_id)
            req = chord_pb2.GetNodeStatsRequest(target_id=str(target_node_id))
            stub.GetNodeStats(req, timeout=2)
        except grpc.RpcError:
            if self.local_node:
                self.local_node.handle_dead_node(target_node_id)

    def cleanup(self):
        for stub in self.stubs.values():
            try:
                channel = stub._channel
                if hasattr(channel, 'close'):
                    channel.close()
            except Exception as e:
                logging.error(f"Error closing gRPC channel: {e}")
        self.stubs.clear()
