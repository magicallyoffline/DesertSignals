"""
aircraft/aircraft_comms.py
Secure broadcast and relay communication simulation for aircraft.

Mimics encrypted ADS-B-like transmissions with integrity protection.
All transmissions are simulated locally through SecureRouter abstraction.

References:
 - ADS-B protocol (Automatic Dependent Surveillance–Broadcast)
 - NASA UTM comms models (Langley Research Center)
"""

import random
import time
from core.router import SecureRouter


class AircraftComms:
    """
    Simulated air-to-air and air-to-ground communication handler.
    """

    def __init__(self, router: SecureRouter):
        self.router = router
        self.peers = []

    def register_peer(self, aircraft_id: str):
        """
        Register aircraft in simulated airspace mesh.
        """
        if aircraft_id not in self.peers:
            self.peers.append(aircraft_id)

    def air_to_air_broadcast(self, origin_id: str, payload: dict):
        """
        Secure broadcast to other aircraft within range.
        """
        for peer in self.peers:
            if peer != origin_id:
                packet = {
                    "from": origin_id,
                    "to": peer,
                    "type": "AIR_TO_AIR",
                    "payload": payload,
                }
                self.router.secure_send(packet)
                time.sleep(random.uniform(0.05, 0.15))

    def air_to_ground(self, aircraft_id: str, data: dict):
        """
        Transmit telemetry to ground systems.
        """
        packet = {
            "from": aircraft_id,
            "to": "GroundOps",
            "type": "AIR_TO_GROUND",
            "data": data,
        }
        self.router.secure_send(packet)
        time.sleep(random.uniform(0.1, 0.3))
