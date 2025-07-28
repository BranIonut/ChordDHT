import unittest
import grpc

from business.node import Node
from business.node_network_interface import NodeNetworkInterface


class TestNetwork(NodeNetworkInterface):
    def __init__(self):
        self.nodes: dict[int, Node] = {}
        self.dead: set[int] = set()

    def register_node(self, node: Node):
        self.nodes[node.node_id] = node

    def find_successor(self, requester_id: int, key: int) -> int:
        return self.nodes[requester_id].find_successor(key)

    def get_predecessor(self, node_id: int) -> int | None:
        return self.nodes[node_id].predecessor

    def set_predecessor(self, node_id: int, predecessor_id: int):
        self.nodes[node_id].predecessor = predecessor_id

    def set_successor(self, node_id: int, successor_id: int):
        self.nodes[node_id].successor = successor_id

    def notify(self, node_id: int, potential_pred_id: int):
        self.nodes[node_id].notify(potential_pred_id)

    def update_finger_table(self, node_id: int, s: int, i: int):
        self.nodes[node_id].update_finger_table(s, i)


class TestNodeNetwork(unittest.TestCase):
    def setUp(self):
        self.network = TestNetwork()
        self.m = 5
        self.nodes = {}

        for node_id in [7, 3, 8, 21, 30, 12, 27]:
            self.nodes[node_id] = Node(node_id, self.m, self.network)
            self.network.register_node(self.nodes[node_id])


    def test_join(self):

        self.nodes[3].join(None)
        self.assertEqual(self.nodes[3].successor, 3)
        self.assertEqual(self.nodes[3].predecessor, 3)

        self.nodes[7].join(self.nodes[3].node_id)

        self.nodes[3].fix_fingers()
        self.nodes[3].stabilize()
        self.nodes[7].fix_fingers()
        self.nodes[7].stabilize()

        self.assertEqual(self.nodes[7].successor, 3)
        self.assertEqual(self.nodes[7].predecessor, 3)
        self.assertEqual(self.nodes[3].successor, 7)
        self.assertEqual(self.nodes[3].predecessor, 7)

    def test_find_successor(self):
        bootstrap_id = 3
        self.nodes[3].join(None)
        self.assertEqual(self.nodes[3].successor, 3)

        for node_id in [7, 8, 12, 21, 27, 30]:
            self.nodes[node_id].join(bootstrap_id)

        for _ in range(self.m):
            for node in self.nodes.values():
                node.stabilize()
            for node in self.nodes.values():
                node.fix_fingers()

        self.assertEqual(self.nodes[7].find_successor(9), 12)

    def test_find_predecessor(self):
        bootstrap_id = 3
        self.nodes[3].join(None)
        self.assertEqual(self.nodes[3].successor, 3)

        for node_id in [7, 8, 12, 21, 27, 30]:
            self.nodes[node_id].join(bootstrap_id)

        for _ in range(11):
            for node in self.nodes.values():
                node.stabilize()
            for node in self.nodes.values():
                node.fix_fingers()

        self.assertEqual(self.nodes[12].find_predecessor(17), 12)
        self.assertEqual(self.nodes[21].find_predecessor(1), 30)



if __name__ == "__main__":
    unittest.main()
