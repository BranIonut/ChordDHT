import os
import sys
import threading
import time
import logging
import signal
from time import sleep

from presentation.chord_server import serve
from business.node import Node
from presentation.kubernetes_network import KubernetesNetwork

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_node_id_from_pod_name(pod_name: str) -> int:
    try:
        if pod_name.startswith("chord-"):
            return int(pod_name.split("-")[-1])
        else:
            raise ValueError(f"Invalid pod name format: {pod_name}")
    except (ValueError, IndexError) as e:
        logger.error(f"Could not extract node ID from pod name '{pod_name}': {e}")
        raise


def launch_node(node_id: int, m: int) -> Node:
    logger.info(f"Launching node {node_id} with m={m}")

    network = KubernetesNetwork(
        namespace=os.getenv("POD_NAMESPACE", "chord-dht"),
        headless_service="chord-headless",
        app_label="chord-node"
    )
    node = Node(node_id, m, network)
    network.set_local_node(node)

    server_thread = threading.Thread(target=serve, args=(node, 50050), daemon=True)
    server_thread.start()
    logger.info(f"gRPC server started for node {node_id}")

    delay = node_id * 10
    logger.info(f"Delaying {delay} seconds before bootstrap discovery...")
    time.sleep(delay)

    logger.info(f"Node {node_id} discovering bootstrap nodes...")
    bootstrap_id = network.discover_bootstrap()
    logger.info(f"Node {bootstrap_id} bootstrap node!!!!!!!!")


    if bootstrap_id:
        logger.info(f"Node {node_id} joined with bootstrap {bootstrap_id}")
    else:
        logger.info(f"Node {node_id} joined without bootstrap")

    node.join(bootstrap_id)
    logger.info(f"Node {node_id} joined the Chord ring")

    node.start_background_tasks()
    logger.info(f"Node {node_id} background tasks started")

    return node


def signal_handler(signum, node, network):
    logger.info(f"Received signal {signum}. Shutting down gracefully...")

    try:
        node.leave()
        logger.info("Node left the Chord ring")

        network.cleanup()
        logger.info("Network connections cleaned up")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    sys.exit(0)


def main():
    m = 6  # Chord ring size parameter (2^m nodes max)

    node_id = 0

    pod_name = os.getenv("POD_NAME")
    if pod_name:
        try:
            node_id = extract_node_id_from_pod_name(pod_name)
            logger.info(f"Extracted node ID {node_id} from pod name {pod_name}")
        except ValueError:
            pass

    if node_id is None and len(sys.argv) >= 2:
        try:
            node_id = int(sys.argv[1])
            logger.info(f"Using node ID {node_id} from command line")
        except ValueError:
            logger.error(f"Invalid node ID provided: {sys.argv[1]}")
            sys.exit(1)

    if node_id is None:
        logger.error("No valid node ID found. Set POD_NAME environment variable or provide as argument.")
        sys.exit(1)

    if not (0 <= node_id < 2 ** m):
        logger.error(f"Node ID {node_id} is out of range [0, {2 ** m - 1}]")
        sys.exit(1)

    try:
        node = launch_node(node_id, m)
        network = node.network

        signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, node, network))
        signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, node, network))

        logger.info(f"Node {node_id} is running. Press Ctrl+C to stop.")

        status_interval = 10  # seconds
        last_status_time = 0

        while True:
            current_time = time.time()

            if current_time - last_status_time >= status_interval:
                try:
                    logger.info("=== Node Status ===")

                    successor_predecessor = node.print_predecessor_successor()
                    logger.info(successor_predecessor)

                    finger_table = node.print_finger_table()
                    logger.info(finger_table)

                    node_stats = node.print_stats()
                    logger.info(node_stats)

                    logger.info("==================")
                    last_status_time = current_time
                except Exception as e:
                    logger.error(f"Error printing status: {e}")

            sleep(5)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        signal_handler(signal.SIGINT, None, node, network)
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()