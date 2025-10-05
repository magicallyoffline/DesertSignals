"""
aircraft/aircraft.py
Autonomous aircraft simulation for Desert Skies / Autonomous Space.

Simulates an AI-assisted aircraft node that performs environment sensing
and safety broadcasts using secure communication envelopes.

References:
 - NASA Aeronautics UTM (Unmanned Aircraft Systems Traffic Management)
 - FAA ADS-B Standards (RTCA DO-260B)
 - NASA "Sky for All" Initiative
"""

import time
import random
from core.router import SecureRouter


class AircraftNode:
    """
    Simulated aircraft with safety and telemetry broadcast capability.
    """

    def __init__(self, tail_number: str, router: SecureRouter, altitude: int = 10000):
        self.tail_number = tail_number
        self.router = router
        self.altitude = altitude
        self.speed = 480  # knots
        self.status = "CRUISE"
        self.health = 100.0

    def broadcast_status(self) -> dict:
        """
        Simulate ADS-B-like broadcast of aircraft state and safety info.
        """
        broadcast = {
            "timestamp": time.time(),
            "aircraft_id": self.tail_number,
            "altitude_ft": self.altitude,
            "speed_knots": self.speed,
            "status": self.status,
            "position": {
                "lat": round(random.uniform(35.0, 38.0), 4),
                "lon": round(random.uniform(-117.0, -114.0), 4),
            },
            "hazard_detected": self.detect_hazard(),
        }
        return broadcast

    def detect_hazard(self):
        """
        Simulates onboard AI hazard detection for turbulence or weather anomalies.
        """
        if random.random() < 0.15:
            return random.choice(["turbulence", "lightning", "wind_shear"])
        return None

    def transmit(self, payload: dict):
        """
        Sends telemetry to ground control or relay satellite securely.
        """
        message = {"from": self.tail_number, "to": "ControlRelay", "payload": payload}
        self.router.secure_send(message)

    def perform_flight_cycle(self):
        """
        Perform a single flight broadcast cycle.
        """
        data = self.broadcast_status()
        self.transmit(data)
        self._simulate_flight_drift()
        time.sleep(0.5)

    def _simulate_flight_drift(self):
        """
        Randomly vary altitude/speed to simulate flight dynamics.
        """
        self.altitude += random.randint(-50, 50)
        self.speed += random.randint(-5, 5)
        self.health -= random.uniform(0.01, 0.1)
        if self.health < 75:
            self.status = "MAINT_REQUIRED"


if __name__ == "__main__":
    from core.pqcrypto import PQCryptoHybrid
    router = SecureRouter(PQCryptoHybrid())
    aircraft = AircraftNode("NASA-UTM-001", router)
    for _ in range(3):
        aircraft.perform_flight_cycle()
