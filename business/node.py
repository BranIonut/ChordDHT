from __future__ import annotations

import logging
import threading
import time

import grpc

from business.node_network_interface import NodeNetworkInterface


class Node:
    def __init__(self, node_id, m, network: NodeNetworkInterface):
        self.node_id = node_id
        self.m = m
        self.network = network

        self.successor: int | None = None
        self.predecessor: int | None = None
        self.finger_table: list[int | None] = [None] * self.m

        self.information: dict[int, str] = {}
        self.redundant_information: dict[int, str] = {}

        self.stats = {
            'lookups': 0,
            'stabilization': 0,
            'finger_fixes': 0,
            'join_time': None
        }

    def join(self, bootstrap_node):
        if bootstrap_node not in ("", None, "None"):
            self.init_finger_table(bootstrap_node)
            if self.successor not in ("", None, "None"):
                self.update_others()
        else:
            for i in range(self.m):
                self.finger_table[i] = self.node_id
            self.successor = self.node_id
            self.predecessor = self.node_id

        self.stats['join_time'] = time.ctime()

    def start(self, i):
        return (self.node_id + (2 ** i)) % (2 ** self.m)

    def init_finger_table(self, node: int):
        self.finger_table[0] = self.network.find_successor(node, self.start(0))
        self.successor = self.finger_table[0]
        self.predecessor = self.network.get_predecessor(self.successor)
        self.network.set_predecessor(self.successor, self.node_id)

        for i in range(self.m - 1):
            if self.in_range(self.start(i + 1), self.node_id, self.finger_table[i]):
                self.finger_table[i + 1] = self.finger_table[i]
            else:
                self.finger_table[i + 1] = self.network.find_successor(self.node_id, self.start(i + 1))
        self.network.notify(self.predecessor, self.node_id)

    def update_others(self):
        for i in range(self.m):
            id_to_update = (self.node_id - 2 ** i) % (2 ** self.m)
            p = self.find_predecessor(id_to_update)
            self.network.update_finger_table(p, self.node_id, i)

    def update_finger_table(self, s: int, i: int):
        if self.finger_table[i] in ("", None, "None") or self.in_range(s, self.node_id, self.finger_table[i]):
            self.finger_table[i] = s
            if self.predecessor not in ("", None, "None") and self.predecessor != self.node_id:
                self.network.update_finger_table(self.predecessor, s, i)

    @staticmethod
    def in_range(key, start, end, include_start=False, include_end=False):

        # print(f' start: {start}, end: {end}, key: {key}')

        start = int(start)
        end = int(end)
        key = int(key)

        if start == end:
            return key != start
        if start < end:
            if include_start and include_end:
                return start <= key <= end
            elif include_start:
                return start <= key < end
            elif include_end:
                return start < key <= end
            else:
                return start < key < end
        else:
            if include_start and include_end:
                return key >= start or key <= end
            elif include_start:
                return key >= start or key < end
            elif include_end:
                return key > start or key <= end
            else:
                return key > start or key < end

    def find_successor(self, key: int) -> int:
        self.stats['lookups'] += 1
        if self.successor == self.node_id:
            return self.node_id

        n = self.find_predecessor(key)
        if n == self.node_id:
            return self.successor
        return self.network.find_successor(n, key)

    def find_predecessor(self, key: int):
        self.stats['lookups'] += 1
        if self.successor == self.node_id:
            return self.node_id

        n = self.node_id
        successor = self.successor
        iterations = 0
        while not self.in_range(key, n, successor, include_end=True) and iterations < self.m + 1:
            prev_n = n
            n = self.closest_preceding_node(key)
            if n == prev_n:
                break
            successor = self.network.find_successor(self.node_id, n)
            iterations += 1

        return n

    def closest_preceding_node(self, key):
        for i in range(self.m - 1, -1, -1):
            node_id = self.finger_table[i]
            if node_id not in ("", None, "None") and self.in_range(node_id, self.node_id, key):
                return node_id
        return self.node_id

    def handle_dead_node(self, dead_node: int):
        if self.successor == dead_node:
            self.successor = self.find_alive_successor()

        if self.predecessor == dead_node:
            self.predecessor = None

        for i in range(self.m):
            if self.finger_table[i] == dead_node:
                self.finger_table[i] = None

    def find_alive_successor(self) -> int:
        for node_id in self.finger_table:
            if node_id and node_id != self.node_id:
                try:
                    self.network.find_successor(self.node_id, node_id)
                    return node_id
                except grpc.RpcError:
                    continue
        return self.node_id

    def print_predecessor_successor(self) -> str:
        return f'Node {self.node_id} successor: {self.successor}, predecessor: {self.predecessor}\n'

    def print_finger_table(self) -> str:
        output: str = ''
        output = output + f'Node {self.node_id} finger table:\n'
        if self.finger_table:
            for i in range(self.m):
                node = self.finger_table[i]
                output = output + f'\tsucc({self.start(i)}): {node if node else "None"}\n'
        else:
            output += 'No finger table elements to show\n'

        return output

    def print_stats(self) -> str:
        output: str = ''
        output += f'Node {self.node_id} stats:\n'
        output += f'\tLookups: {self.stats["lookups"]}\n'
        output += f'\tStabilization: {self.stats["stabilization"]}\n'
        output += f'\tFinger fixes: {self.stats["finger_fixes"]}\n'
        output += f'\tJoining time: {self.stats["join_time"]}\n'

        return output

    def leave(self):
        if self.successor and self.successor != self.node_id:
            for key, value in self.information.items():
                self.network.add_information(self.successor, key, value)

        if self.predecessor != self.node_id:
            self.network.set_successor(self.predecessor, self.successor)

        if self.successor != self.node_id:
            self.network.set_predecessor(self.successor, self.predecessor)

        if self.predecessor != self.node_id:
            self.network.notify(self.predecessor, self.successor)
        if self.successor != self.node_id:
            self.network.notify(self.successor, self.predecessor)

    def fix_fingers(self):
        self.stats['finger_fixes'] += 1
        for i in range(self.m):
            try:
                successor = self.network.find_successor(self.node_id, self.start(i))
                if successor is not None:
                    self.finger_table[i] = successor
            except grpc.RpcError:
                continue

    def stabilize(self):
        self.stats['stabilization'] += 1
        try:
            x = self.network.get_predecessor(self.successor)
            if x and self.in_range(x, self.node_id, self.successor, include_end=True):
                self.successor = x
        except grpc.RpcError:
            logging.error(f"[Node {self.node_id}] Detected dead successor: {self.successor}")
            self.successor = self.find_alive_successor()

        try:
            self.network.notify(self.successor, self.node_id)
        except grpc.RpcError:
            self.successor = self.find_alive_successor()

        if self.predecessor is not None:
            try:
                _ = self.network.get_predecessor(self.predecessor)
            except grpc.RpcError:
                logging.error(f"[Node {self.node_id}] Detected dead predecessor: {self.predecessor}")
                self.predecessor = None
        else:
            self.predecessor = self.node_id

        if self.successor == self.node_id and (self.predecessor is None or self.predecessor == self.node_id):
            self.predecessor = self.node_id
            self.successor = self.node_id

    def notify(self, node: int):
        logging.info(f"[Node {self.node_id}] Received notify({node}) with current predecessor = {self.predecessor}")
        if self.predecessor is None or self.in_range(node, self.predecessor, self.node_id):
            logging.info(f"[Node {self.node_id}] Updating predecessor from {self.predecessor} to {node}")
            self.predecessor = node
        else:
            logging.info(f"[Node {self.node_id}] Did NOT update predecessor")

    def node_has_info(self, info: int):
        # print(f"[Node {self.node_id}]: searching information for key {info}.")
        if self.information.__contains__(info):
            # print(f"Info found: {self.information[info]}")
            return self.information[info]
        # print(f"Info not found...")
        return None

    def get_information(self, info_key: int):
        responsible_node = self.find_successor(info_key)
        # print(f"[get_information] {info_key} predecessor is {responsible_node}")
        if responsible_node == self.node_id:
            return self.node_has_info(info_key)

        information = self.network.get_information(responsible_node, info_key)

        return information if information != 'None' else None

    def create_info(self, info_key: int, info: str) -> bool:
        info_already_exists = self.get_information(info_key)

        if info_already_exists:
            return False
        responsible_node = self.find_successor(info_key)
        if responsible_node == self.node_id:
            self.add_information(info_key, info)
            return True

        self.network.add_information(responsible_node, info_key, info)

        # successor_node = self.network.find_successor(self.node_id, responsible_node)
        # for _ in range(2):
        #     successor_node.__add_redundant_info(info_key, info)
        #     successor_node = self.network.find_successor(self.node_id, successor_node)
        return True

    def remove_info(self, info_key: int):
        info_already_exists = self.get_information(info_key)

        if not info_already_exists:
            return False
        responsible_node = self.find_successor(info_key)
        if responsible_node == self.node_id:
            self.remove_information(info_key)
            return True

        self.network.remove_information(responsible_node, info_key)
        return True

    def start_background_tasks(self):
        def loop():
            while True:
                logging.info(f'[start_background_tasks][{self.node_id}] stabilization and fixing fingers')
                self.stabilize()
                self.fix_fingers()
                time.sleep(5)

        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def remove_redundant_info(self, info_key: int):
        self.redundant_information.pop(info_key, None)

    def remove_information(self, info_key: int):
        self.information.pop(info_key, None)

    def add_information(self, info_key: int, info: str):
        self.information[info_key] = info

    def add_redundant_info(self, info_key: int, info: str):
        self.redundant_information[info_key] = info
