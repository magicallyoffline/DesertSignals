"""
consensus.py
NASA Space Apps 2025 – Multi-Agency Consensus Engine (PQC + Safety Enhanced)

Purpose:
Simulates a verifiable cross-agency consensus framework for Earth observation data
using hybrid cryptography and trust verification layers.
Designed for integration with safety.py and pqcrypto.py.

Real Analogs:
 - NASA: ECOSTRESS, GRACE-FO, POWER satellite data
 - NOAA: Climate and atmospheric modeling
 - USGS: Hydrology and terrain validation
 - Local Agencies: Water authority + heat/flood mitigation

References:
 - NASA-STD-8719.13C (Software Safety)
 - CCSDS 355.0-G-3 (Space Data Link Security)
 - NIST PQC Final Round (Kyber / Dilithium)
"""

import random
import statistics
import json
import time
from typing import Dict, List

from core.safety import SafetyManager


class AgencyNode:
    """
    Represents a participating agency node (NASA, NOAA, etc.)
    Each performs independent verification and sends secure signed telemetry.
    """

    def __init__(self, name: str, reliability: float = 0.9, safety: SafetyManager = None):
        self.name = name
        self.reliability = reliability
        self.safety = safety or SafetyManager()

    def verify(self, risk_data: Dict[str, float]) -> Dict[str, float]:
        """
        Simulate agency-level verification with confidence-weighted bias.
        """
        verified = {}
        for key, value in risk_data.items():
            deviation = random.uniform(-0.03, 0.03) * (1.0 - self.reliability)
            verified[key] = max(0.0, min(1.0, value + deviation))
        confidence = self.reliability * random.uniform(0.9, 1.0)

        payload = {
            "agency": self.name,
            "verified_risk": verified,
            "confidence": confidence,
            "timestamp": time.time(),
        }
        return self.safety.secure_wrap(self.name, payload)


class ConsensusEngine:
    """
    Aggregates multiple agency verifications into a single trusted consensus.
    Hybrid cryptography via SafetyManager ensures authenticity of all participants.
    """

    def __init__(self):
        self.safety = SafetyManager()
        self.nodes = [
            AgencyNode("NASA", reliability=0.97, safety=self.safety),
            AgencyNode("NOAA", reliability=0.95, safety=self.safety),
            AgencyNode("USGS", reliability=0.93, safety=self.safety),
            AgencyNode("LocalAgency", reliability=0.85, safety=self.safety),
        ]

    def aggregate(self, risk_report: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Collects secure reports, verifies them, and computes weighted mean per metric.
        """
        verified_data = []
        for node in self.nodes:
            envelope = node.verify(risk_report["risk"])
            try:
                data = self.safety.secure_unwrap(envelope)
                verified_data.append(data)
            except Exception as e:
                print(f"Warning: Data rejected from {envelope['node_id']} — {str(e)}")

        combined = {}
        for metric in ["heat", "drought", "flood"]:
            weighted_sum = sum(d["verified_risk"][metric] * d["confidence"] for d in verified_data)
            total_weight = sum(d["confidence"] for d in verified_data)
            combined[metric] = round(weighted_sum / total_weight, 3)

        consensus = {
            "agencies_involved": [d["agency"] for d in verified_data],
            "consensus_risk": combined,
            "mean_confidence": round(statistics.mean(d["confidence"] for d in verified_data), 3),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        }
        return consensus

    def consensus_report(self, risk_report: Dict[str, Dict[str, float]]) -> str:
        """
        Return a JSON string of the consensus result (verified & timestamped).
        """
        result = self.aggregate(risk_report)
        return json.dumps(result, indent=2)


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    from core.risk import RiskEngine

    risk_engine = RiskEngine()
    risk_report = risk_engine.analyze()

    engine = ConsensusEngine()
    final_report = engine.consensus_report(risk_report)
    print(final_report)
