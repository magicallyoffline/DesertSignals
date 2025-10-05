"""
NASA Space Apps 2025 – Ground Robotics Simulation
-------------------------------------------------
Simulated autonomous ground robot node that:
 - Collects environmental readings from sensors.
 - Analyzes field conditions.
 - Relays verified results through secure comms.

This simulates how field robots (agricultural or environmental)
support satellite and drone networks with ground truth.
"""

import random
import time
from core.router import SecureRouter
from ground.sensor import GroundSensor


class GroundRobot:
    def __init__(self, name: str, location: str, router: SecureRouter):
        self.name = name
        self.location = location
        self.router = router
        self.sensor = GroundSensor(location, router)

    def assess_environment(self):
        """
        Analyze sensor data and produce a localized risk flag.
        """
        data = self.sensor.read_environment()
        risk = "normal"

        if data["temperature_c"] > 37 or data["humidity_pct"] < 30:
            risk = "heat_alert"
        elif data["soil_moisture_pct"] < 15:
            risk = "drought_warning"
        elif data["humidity_pct"] > 75:
            risk = "flood_risk"

        report = {
            "robot_id": self.name,
            "location": self.location,
            "risk_flag": risk,
            "timestamp": time.time(),
        }
        return report

    def transmit_report(self):
        """
        Encrypt and send report through secure router.
        """
        report = self.assess_environment()
        encrypted = self.router.encrypt_message(report)
        print(f"[Robot {self.name}] transmitting encrypted status.")
        return encrypted


# Example usage (safe to run)
if __name__ == "__main__":
    router = SecureRouter()
    robot = GroundRobot("Unit_01", "Miami_Environmental_Field", router)
    packet = robot.transmit_report()
    print("Encrypted payload:", packet)
