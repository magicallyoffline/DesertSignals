"""
NASA Space Apps 2025 – Ground Sensor Simulation
----------------------------------------------
Simulated ground-based sensors that monitor environmental conditions:
 - Soil moisture
 - Air temperature
 - Humidity

These sensors provide the local verification layer for satellite data,
forming the 'bottom-up' half of the autonomous-space system.

All communications are routed securely through the core router.
"""

import random
import time
from core.router import SecureRouter


class GroundSensor:
    def __init__(self, location: str, router: SecureRouter):
        self.location = location
        self.router = router

    def read_environment(self):
        """
        Generate mock sensor readings with realistic ranges.
        """
        data = {
            "location": self.location,
            "temperature_c": round(random.uniform(28, 40), 2),
            "soil_moisture_pct": round(random.uniform(10, 45), 2),
            "humidity_pct": round(random.uniform(40, 80), 2),
            "timestamp": time.time(),
        }
        return data

    def transmit(self):
        """
        Securely send sensor data through the router.
        """
        reading = self.read_environment()
        encrypted = self.router.encrypt_message(reading)
        print(f"[Sensor @ {self.location}] transmitting encrypted packet.")
        return encrypted


# Example usage (safe to run)
if __name__ == "__main__":
    router = SecureRouter()
    sensor = GroundSensor("Miami_Test_Field", router)
    packet = sensor.transmit()
    print("Encrypted payload:", packet)
