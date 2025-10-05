"""
satellite/satellite.py
Autonomous satellite node simulation for Desert Skies / Autonomous Space.

Models data relay and observation nodes similar to NASA's Earth Observing System (EOS)
satellites — e.g., Landsat, ECOSTRESS, GRACE-FO, GOES.
Each satellite periodically collects mock Earth data and routes it securely.

References:
- NASA EOSDIS: https://earthdata.nasa.gov
- NASA SCaN Communications: https://www.nasa.gov/directorates/heo/scan
"""

import time
import random
from core.router import SecureRouter


class SatelliteNode:
    """
    Represents a satellite capable of generating environmental observations
    and relaying them via encrypted crosslinks or downlinks.
    """

    def __init__(self, sat_id: str, router: SecureRouter, orbit_type="LEO"):
        self.sat_id = sat_id
        self.router = router
        self.orbit_type = orbit_type
        self.health = "Nominal"
        self.power_level = 100.0

    def collect_observation(self) -> dict:
        """
        Simulates retrieval of Earth surface and atmospheric data.
        """
        data = {
            "temperature": round(random.uniform(290, 320), 2),   # Kelvin
            "humidity": round(random.uniform(10, 70), 1),        # %
            "groundwater": round(random.uniform(-2.0, 2.0), 3),  # GRACE-FO anomaly
            "surface_temp": round(random.uniform(280, 330), 1),
            "timestamp": time.time(),
            "satellite_id": self.sat_id,
        }
        return data

    def broadcast(self, payload: dict, target: str = "GroundStation"):
        """
        Encrypts and transmits data using SecureRouter.
        """
        message = {"from": self.sat_id, "to": target, "payload": payload}
        self.router.secure_send(message)

    def execute_cycle(self):
        """
        One full observation + downlink cycle.
        """
        obs = self.collect_observation()
        self.broadcast(obs)
        self._drain_power()

    def _drain_power(self):
        self.power_level -= random.uniform(0.1, 0.5)
        if self.power_level <= 10:
            self.health = "LowPower"


# Example test run
if __name__ == "__main__":
    from core.pqcrypto import PQCryptoHybrid
    router = SecureRouter(PQCryptoHybrid())
    sat = SatelliteNode("SAT-LEO-01", router)
    for _ in range(2):
        sat.execute_cycle()
        time.sleep(0.5)
