"""
satellite/satellite_comms.py
Simulates encrypted inter-satellite crosslinks and downlinks to ground stations.
Based on RF/optical relay models used by NASA (e.g., TDRSS, LCRD).
"""

import random
import time
from core.router import SecureRouter


class SatelliteComms:
    """
    Handles communication simulation between satellites and ground segments.
    """

    def __init__(self, router: SecureRouter):
        self.router = router
        self.link_quality = 1.0  # 0–1, simulated link quality
        self.lag_ms = random.randint(50, 500)

    def crosslink(self, origin_id: str, target_id: str, data: dict):
        """
        Satellite-to-satellite encrypted relay.
        """
        packet = {"from": origin_id, "to": target_id, "data": data}
        time.sleep(self.lag_ms / 1000)
        self.router.secure_send(packet)

    def downlink(self, sat_id: str, ground_station: str, data: dict):
        """
        Satellite-to-ground transmission simulation.
        """
        loss_factor = random.uniform(0.95, 1.0) * self.link_quality
        if random.random() < (1 - loss_factor):
            print(f"[WARN] Downlink packet lost from {sat_id}")
            return
        packet = {"from": sat_id, "to": ground_station, "data": data}
        time.sleep(self.lag_ms / 1000)
        self.router.secure_send(packet)

    def update_link(self):
        """
        Periodically fluctuate link quality (e.g., atmospheric attenuation).
        """
        self.link_quality = max(0.7, min(1.0, self.link_quality + random.uniform(-0.05, 0.05)))
