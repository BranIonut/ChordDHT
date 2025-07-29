# Chord DHT – Distributed Hash Table Implementation

This is a **fully-distributed implementation of the Chord protocol** for consistent hashing and decentralized data storage. Each node runs independently in a Docker container, communicates via gRPC, and can autonomously join or leave the network.

## Features

- Fully functional Chord ring (modulo `2^m` identifier space)
- gRPC-based communication between nodes
- Node discovery via automatic bootstrap with `nmap`
- Finger table implementation (`m` entries) for O(log N) lookup
- Replication and redundant data handling
- Fault tolerance: dead node detection via `grpc.RpcError`
- Dynamic stabilization and finger fixing in background
- Support for node `join`, `leave`, and key re-distribution
- Unit-tested with `unittest`

---

## Protocol Overview

The Chord protocol is a structured peer-to-peer protocol for implementing a **Distributed Hash Table (DHT)**. It maps both nodes and keys onto the same identifier space using consistent hashing (typically SHA-1). Keys are stored on the **successor node**.

Each node maintains:
- Its **successor** and **predecessor**
- A **finger table** for efficient routing
- A map of **owned data** and **replicated data**


