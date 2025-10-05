"""
router.py
NASA Space Apps 2025 – Secure Routing Layer

Simulated encrypted message routing between autonomous nodes:
    - Satellites, drones, ground sensors, agencies, aircraft.
Uses post-quantum hybrid encryption (AES + Kyber + Dilithium + HMAC)
from pqcrypto.py for end-to-end confidentiality and integrity.

Author: [Your Name]
"""

import random
import time
from core.pqcrypto import PQCryptoHybrid


class SecureRouter:
    """
    SecureRouter acts as the backbone of the autonomous_space network.
    Every communication between nodes is wrapped in:
      1. Kyber key encapsulation
      2. AES-256 encryption
      3. Dilithium signature
      4. HMAC integrity verification
    """

    def __init__(self, crypto_engine: PQCryptoHybrid):
        self.crypto = crypto_engine
        self.nodes = {}
        self.latency = (0.05, 0.25)  # seconds, simulating comms delay

    # -------------------------------------------------------------
    # Node Registry
    # -------------------------------------------------------------
    def register_node(self, node):
        """Register an autonomous node with a unique ID."""
        if node.node_id in self.nodes:
            raise ValueError(f"Duplicate node ID: {node.node_id}")
        self.nodes[node.node_id] = node
        print(f"[ROUTER] Node registered: {node.node_id}")

    def list_nodes(self):
        """Return list of registered nodes."""
        return list(self.nodes.keys())

    # -------------------------------------------------------------
    # Packet Transmission
    # -------------------------------------------------------------
    def send(self, node_id: str, message: str):
        """
        Simulate encrypted transmission to a node.
        Encrypt → send → receive → decrypt.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Target node not found: {node_id}")

        node = self.nodes[node_id]
        print(f"[ROUTER] Preparing secure transmission to {node_id} ...")

        # Step 1: Encrypt message packet
        packet = self.crypto.encrypt_message(message)

        # Step 2: Simulate latency
        time.sleep(random.uniform(*self.latency))

        # Step 3: Deliver to node (simulate decryption)
        response = node.receive_secure_packet(packet, self.crypto)

        return response

    def broadcast(self, message: str, node_filter=None):
        """
        Broadcast an encrypted message to all or filtered nodes.
        node_filter: list of IDs or function(node) -> bool
        """
        results = {}
        for node_id, node in self.nodes.items():
            if node_filter and not (node_id in node_filter or node_filter(node)):
                continue
            results[node_id] = self.send(node_id, message)
        return results

    # -------------------------------------------------------------
    # Diagnostics
    # -------------------------------------------------------------
    def audit_traffic(self):
        """Print a snapshot of network nodes and simulated latency."""
        print("\n[ROUTER] === Network Audit ===")
        for node_id, node in self.nodes.items():
            print(f" - {node_id} ({node.__class__.__name__})")
        print("==============================\n")
