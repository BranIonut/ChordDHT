import sys
import threading
import time
from asyncio import timeout
from socket import socket

import grpc

from presentation.chord_pb2 import FindSuccessorRequest
from presentation.chord_pb2_grpc import ChordStub
from presentation.docker_network import DockerNetwork
from presentation.chord_server import serve
from business.node import Node

SERVICE_TEMPLATE="chord-node-{}.chord-headless.chord-dht-namespace.svc.cluster.local:50050"

def is_node_alive(index: int, node_id: int) -> bool:
    if index == node_id:
        return False

    address = SERVICE_TEMPLATE.format(index)
    try:
        socket.gethostbyname(address.split(':')[0])

        channel = grpc.insecure_channel(address)
        stub = ChordStub(channel)

        response = stub.FindSuccessor(FindSuccessorRequest(target_id=str(index), key="0"), timeout=2)
        return True
    except Exception as e:
        return False

def discover_bootstrap_node(node_id: int, max_nodes: int = 10) -> int | None:
    for id in range(max_nodes):
        if is_node_alive(id, node_id):
            print(f"[DISCOVERY] Found bootstrap node: {id}")
            return id
    print("[DISCOVERY] No bootstrap node found.")
    return None

def launch_node(node_id: int, m: int) -> Node:
    client = DockerNetwork()
    node = Node(node_id, m, client)
    client.set_local_node(node)

    t = threading.Thread(target=serve, args=(node, 50050), daemon=True)
    t.start()
    time.sleep(1)

    bootstrap_id = discover_bootstrap_node(node_id, max_nodes=10)
    node.join(bootstrap_id)
    node.start_background_tasks()
    return node