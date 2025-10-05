"""
autonomous_space.py
Global Autonomous Observation Simulation
Post-Quantum Encrypted Communication Network
NASA x USGS Inspired System

Author: [m0rs3c0d3]
Hackathon: NASA Space Apps 2025
"""

from core.pqcrypto import PQCryptoHybrid
from core.router import SecureRouter
from core.risk import RiskEngine
from core.consensus import ConsensusEngine
from core.policy import PolicyManager
from core.safety import SafetyManager

from satellite.satellite import SatelliteNode
from drone.drone import DroneNode
from ground.sensor import GroundSensor
from agency.agency import AgencyRegistry

import json
import time
import random

# Simulated NASA API for global cities/regions
def get_active_regions():
    """
    Pretend API call to NASA EarthData/POWER or OpenET datasets.
    In real deployment, this could query lat/lon or bounding boxes.
    """
    return [
        {"name": "Las Vegas", "country": "USA", "coords": [36.17, -115.14]},
        {"name": "Phoenix", "country": "USA", "coords": [33.45, -112.07]},
        {"name": "Los Angeles", "country": "USA", "coords": [34.05, -118.25]},
        {"name": "Houston", "country": "USA", "coords": [29.76, -95.37]},
        {"name": "Miami", "country": "USA", "coords": [25.76, -80.19]},
        {"name": "London", "country": "UK", "coords": [51.51, -0.13]},
        {"name": "Tokyo", "country": "Japan", "coords": [35.68, 139.76]},
        {"name": "Nairobi", "country": "Kenya", "coords": [-1.28, 36.82]},
        {"name": "Delhi", "country": "India", "coords": [28.61, 77.20]},
        {"name": "Sao Paulo", "country": "Brazil", "coords": [-23.55, -46.63]}
    ]


def initialize_system():
    print("[SYSTEM] Initializing Global Autonomous Network...")

    # Core systems
    crypto = PQCryptoHybrid()
    router = SecureRouter(crypto)
    risk = RiskEngine()
    consensus = ConsensusEngine()
    policy = PolicyManager()
    safety = SafetyManager()

    # Agency registry (NASA, USGS, NOAA, ESA, JAXA)
    agencies = AgencyRegistry()
    agencies.register_defaults()

    # Dynamic region setup
    regions = get_active_regions()
    print(f"[SYSTEM] {len(regions)} regions loaded.")

    # Register nodes for each region
    for r in regions:
        name = r["name"].replace(" ", "_")
        sat = SatelliteNode(f"SAT-{name}", orbit="LEO", region=r)
        drone = DroneNode(f"DRONE-{name}", region=r)
        sensor = GroundSensor(f"SENSOR-{name}", metrics=["temp", "humidity", "water"], region=r)
        router.register_node(sat)
        router.register_node(drone)
        router.register_node(sensor)

    print("[SYSTEM] Global network initialized with PQC encryption and policy layers.")
    return crypto, router, risk, consensus, policy, safety, agencies, regions


def run_cycle(router, risk, consensus, agencies, regions):
    """
    Run one cycle of autonomous observation across all regions.
    """

    print("\n[SIM] Running global observation cycle...\n")

    reports = {}

    for region in regions:
        region_id = region["name"].replace(" ", "_")

        sat_data = router.send(f"SAT-{region_id}", "Collect imagery")
        drone_data = router.send(f"DRONE-{region_id}", "Measure ET and heat")
        ground_data = router.send(f"SENSOR-{region_id}", "Send ground truth")

        all_data = {"sat": sat_data, "drone": drone_data, "ground": ground_data}
        risk_report = risk.analyze(all_data)
        verified = consensus.verify(all_data, agencies)
        reports[region_id] = {
            "risk": risk_report,
            "verified": verified
        }

        if verified:
            safety.audit(all_data)

        print(f"[CYCLE] {region['name']}: verified={verified}")

    print("\n[SIM] Global cycle complete. Summary:")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    crypto, router, risk, consensus, policy, safety, agencies, regions = initialize_system()

    for i in range(2):  # run two cycles for demo
        run_cycle(router, risk, consensus, agencies, regions)
        time.sleep(3)

    print("\n[MISSION] Global Autonomous Network stable and secure.")
