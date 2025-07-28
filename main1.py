import sys
import threading
import time
from itertools import repeat

from presentation.chord_client_stub import ChordClientStub
from presentation.chord_server import serve
from business.node import Node

ADDRESS_MAP = {
    i: f"localhost:{50050 + i}" for i in range(33)
}


def node_already_exists(nodes: list[Node], x: int) -> bool:
    for i in range(len(nodes)):
        if nodes[i].node_id == x:
            return True
    return False


def launch_node(node_id: int, m: int, port: int, bootstrap_id: int | None = None) -> Node:
    client = ChordClientStub(ADDRESS_MAP)
    node = Node(node_id, m, client)
    client.set_local_node(node)

    t = threading.Thread(target=serve, args=(node, port), daemon=True)
    t.start()
    time.sleep(1)

    node.join(bootstrap_id)
    node.start_background_tasks()
    return node


def main():
    m = 6
    nodes = {}
    node_id = 0

    if len(sys.argv) == 3:
        node_id = int(sys.argv[1])
        bootstrap_id = int(sys.argv[2])
        port = int(ADDRESS_MAP[node_id].split(":")[1])
        nodes[node_id] = launch_node(node_id, m, port, bootstrap_id)

    elif len(sys.argv) == 2:
        node_id = int(sys.argv[1])
        port = int(ADDRESS_MAP[node_id].split(":")[1])
        nodes[node_id] = launch_node(node_id, m, port)
        print(f"[INFO] Node {node_id} joined without bootstrap.")

    if node_id == 14:
        nodes[node_id].information[5] = "abcdefghijklmnop"

    while True:
        cmd = input(f'\nType your command: [help] for more information\n[Node {node_id}]: ')

        if cmd.lower() == 'help':
            print('Help menu:')
            print('\t-> fix - fixes and stabilizes finger table, successor and predecessor of current node')
            print('\t-> print - prints successor, predecessor and finger table of current node')
            print('\t-> stats - shows numbers of fixes, stabilization, searches of current node')
            print('\t-> info [info_key] - searches and shows information about given key')
            print('\t-> create [info_key] [info_value] - creates information about given key, if not already exists')
            print('\t-> remove [info_key] [info_value] - removes information about given key, if exists')
            print('\t-> leave - leaves current node')

        elif cmd.lower() == 'exit':
            exit(0)

        elif cmd.lower() == 'fix':
            nodes[node_id].fix_fingers()
            nodes[node_id].stabilize()

        elif cmd.lower() == 'print':
            nodes[node_id].print_predecessor_successor()
            nodes[node_id].print_finger_table()

        elif cmd.lower().split(' ')[0] == 'create':
            if len(cmd.lower().split(' ', 2)) != 3:
                print("Invalid command. Correct format: create [info_key] [info_value]")
                continue
            x = int(cmd.split(' ')[1])
            y = cmd.split(' ', 3)[2]
            print(f"{x}, {y}")
            nodes[node_id].create_info(int(cmd.split(' ')[1]), cmd.split(' ', 3)[2])

        elif cmd.lower().split(' ')[0] == 'info':
            if len(cmd.lower().split(' ')) != 2:
                print("Invalid command. Correct format: info [info_key]")
                continue
            info = nodes[node_id].get_information(int(cmd.split(' ')[1]))
            if info is not None:
                print(f"Info({cmd.split(' ')[1]}): {info}")
            else:
                print(f"Info was not found...")

        elif cmd.lower().split(' ')[0] == 'remove':
            if len(cmd.lower().split(' ')) != 2:
                print("Invalid command. Correct format: remove [info_key]")
                continue
            info = nodes[node_id].remove_info(int(cmd.split(' ')[1]))
            if info:
                print(f"Info removed successfully...")
            else:
                print(f"Info was not removed...")

        elif cmd.lower().split(' ')[0] == 'successor':
            if len(cmd.lower().split(' ')) != 2:
                print("Invalid command. Correct format: successor [key]")
                continue
            print(f'{nodes[node_id].find_successor(int(cmd.lower().split(" ")[1]))}')


if __name__ == "__main__":
    main()
