"""
NASA Space Apps 2025 – Agency Coordination Layer
------------------------------------------------
This module defines how NASA, NOAA, USGS, and local agencies
interact within the autonomous_space network.

Purpose:
 - Simulate ingestion of encrypted telemetry from satellites, drones,
   aircraft, and ground nodes.
 - Verify integrity via agency trust authority.
 - Publish consolidated updates to the consensus layer.
"""

import time
from core.router import SecureRouter
from agency.trust import TrustAuthority


class Agency:
    def __init__(self, name: str, trust_authority: TrustAuthority, router: SecureRouter):
        self.name = name
        self.trust = trust_authority
        self.router = router
        self.received_packets = []

    def receive_packet(self, packet):
        """
        Receive encrypted telemetry → decrypt → validate signature.
        """
        decrypted = self.router.decrypt_message(packet)
        if not self.trust.validate_signature(self.name, decrypted):
            print(f"[{self.name}] Rejected packet – invalid signature.")
            return None

        print(f"[{self.name}] Accepted verified telemetry packet.")
        self.received_packets.append(decrypted)
        return decrypted

    def analyze_data(self):
        """
        Simulate each agency analyzing the received data.
        """
        if not self.received_packets:
            return {"agency": self.name, "status": "no_data"}

        # Mock analytics: aggregate temperature, risk flags, etc.
        avg_temp = sum(p.get("temperature_c", 0) for p in self.received_packets) / len(self.received_packets)
        risks = [p.get("risk_flag", "normal") for p in self.received_packets]
        alerts = [r for r in risks if r != "normal"]

        report = {
            "agency": self.name,
            "entries": len(self.received_packets),
            "avg_temp": round(avg_temp, 2),
            "active_alerts": alerts,
            "timestamp": time.time(),
        }

        print(f"[{self.name}] Analysis summary:", report)
        return report

    def publish_update(self, consensus_engine, report):
        """
        Simulate publishing results to the multi-agency consensus engine.
        """
        print(f"[{self.name}] Publishing verified data to consensus engine.")
        consensus_engine.aggregate({"risk": {"heat": 0.6, "drought": 0.4, "flood": 0.2}})
        return True


# Example usage
if __name__ == "__main__":
    from core.consensus import ConsensusEngine

    router = SecureRouter()
    trust = TrustAuthority()
    nasa = Agency("NASA", trust, router)
    consensus = ConsensusEngine()

    # Simulate packet reception
    packet = router.encrypt_message({"temperature_c": 38.7, "risk_flag": "heat_alert"})
    trust.register_agency("NASA")
    decrypted = nasa.receive_packet(packet)
    report = nasa.analyze_data()
    nasa.publish_update(consensus, report)
