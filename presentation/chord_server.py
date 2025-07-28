from concurrent import futures

import grpc

from business.node import Node
from business.node_network_interface import NodeNetworkInterface
from . import chord_pb2_grpc
from . import chord_pb2
from presentation.chord_pb2_grpc import ChordServicer


class ChordServer(ChordServicer):

    def __init__(self, node: Node):
        self.node = node

    def FindSuccessor(self, request, context):
        successor = self.node.find_successor(int(request.key))
        return chord_pb2.FindSuccessorResponse(successor_id=str(successor))

    def FindPredecessor(self, request, context):
        predecessor = self.node.predecessor
        if predecessor is None:
            predecessor = self.node.node_id
        return chord_pb2.FindPredecessorResponse(predecessor_id=str(predecessor))

    def SetPredecessor(self, request, context):
        self.node.predecessor = int(request.new_predecessor_id)
        return chord_pb2.SetPredecessorResponse()

    def Notify(self, request, context):
        self.node.notify(int(request.sender_id))
        return chord_pb2.NotifyResponse()

    def UpdateFingerTable(self, request, context):
        self.node.update_finger_table(int(request.new_node_id), int(request.index))
        return chord_pb2.UpdateFingerTableResponse()

    def FixFingers(self, request, context):
        self.node.fix_fingers()
        return chord_pb2.FixFingersResponse()

    def Stabilize(self, request, context):
        self.node.stabilize()
        return chord_pb2.StabilizeResponse()

    def GetInformation(self, request, context):
        info = self.node.node_has_info(int(request.key))
        return chord_pb2.GetInfoResponse(information=info if info is not None else "None")

    def AddInformation(self, request, context):
        self.node.add_information(int(request.info_key), request.info)
        return chord_pb2.AddInfoResponse()

    def RemoveInformation(self, request, context):
        self.node.remove_info(int(request.info_key))
        return chord_pb2.RemoveInfoResponse()


def serve(node, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chord_pb2_grpc.add_ChordServicer_to_server(ChordServer(node), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'Node {node.node_id} gRPC Server running on port {port}')
    server.wait_for_termination()
