"""
drone/drone_comms.py
Secure mesh communication layer for drone swarm simulation.
Implements AES + HMAC routing via SecureRouter abstraction.
"""

import random
import time
from core.router import SecureRouter


class DroneMeshComms:
    """
    Simulates drone-to-drone or drone-to-gateway communication.
    """

    def __init__(self, router: SecureRouter):
        self.router = router
        self.signal_strength = 1.0  # 0–1
        self.mesh_nodes = []

    def register_node(self, node_id: str):
        if node_id not in self.mesh_nodes:
            self.mesh_nodes.append(node_id)

    def broadcast(self, origin_id: str, data: dict):
        """
        Broadcast data to all registered drones via secure channel.
        """
        for node in self.mesh_nodes:
            if node != origin_id:
                packet = {"from": origin_id, "to": node, "data": data}
                self.router.secure_send(packet)
                time.sleep(random.uniform(0.05, 0.2))

    def relay_to_satellite(self, drone_id: str, data: dict):
        """
        Send data to satellite relay node (simulated uplink).
        """
        latency = random.uniform(100, 400) / 1000  # ms
        time.sleep(latency)
        packet = {"from": drone_id, "to": "SatelliteRelay", "data": data}
        self.router.secure_send(packet)

    def update_signal(self):
        """
        Adjusts signal based on environment interference.
        """
        drift = random.uniform(-0.05, 0.05)
        self.signal_strength = max(0.6, min(1.0, self.signal_strength + drift))
