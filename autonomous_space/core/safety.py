"""
safety.py
NASA Space Apps 2025 – Security, Integrity, and Replay Protection Layer

Purpose:
Ensures integrity, authenticity, and temporal safety of all autonomous communications
within the Desert Skies / Autonomous Space architecture.

Based on principles from:
 - NASA-STD-8739.8 (Software Assurance and Safety)
 - CCSDS 355.0-G-3 (Space Data Link Security)
 - NIST SP 800-57, SP 800-208 (Post-Quantum Crypto Guidelines)
"""

import time
import hmac
import hashlib
import secrets
from typing import Dict, Any


class SafetyManager:
    """
    Security and trust enforcement for cross-node communications.
    """

    def __init__(self, trusted_nodes=None, hmac_key=None):
        # Trusted entities: NASA, NOAA, FAA, USGS, USBR, CityGov
        self.trusted_nodes = trusted_nodes or [
            "NASA",
            "NOAA",
            "USGS",
            "FAA",
            "USBR",
            "CityGov",
        ]
        self.hmac_key = hmac_key or secrets.token_bytes(32)
        self.replay_window = 10.0  # seconds
        self.last_timestamps: Dict[str, float] = {}

    # ----------------------------- Integrity Layer -----------------------------

    def compute_hmac(self, message: str) -> str:
        """
        Compute an HMAC-SHA256 signature to ensure message integrity.
        """
        mac = hmac.new(self.hmac_key, message.encode(), hashlib.sha256)
        return mac.hexdigest()

    def verify_hmac(self, message: str, signature: str) -> bool:
        """
        Verify message integrity using constant-time comparison.
        """
        expected = self.compute_hmac(message)
        return hmac.compare_digest(expected, signature)

    # ----------------------------- Replay Protection -----------------------------

    def is_replay(self, node_id: str, timestamp: float) -> bool:
        """
        Check for replayed or out-of-order messages.
        """
        last_time = self.last_timestamps.get(node_id, 0)
        if timestamp <= last_time:
            return True
        if abs(time.time() - timestamp) > self.replay_window:
            return True
        self.last_timestamps[node_id] = timestamp
        return False

    # ----------------------------- Trust Validation -----------------------------

    def validate_sender(self, node_id: str) -> bool:
        """
        Ensure node belongs to a trusted organization or partner.
        """
        return node_id in self.trusted_nodes

    # ----------------------------- Secure Envelope -----------------------------

    def secure_wrap(self, node_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a signed message envelope with replay protection.
        """
        timestamp = time.time()
        data_str = f"{node_id}|{timestamp}|{payload}"
        signature = self.compute_hmac(data_str)
        return {
            "node_id": node_id,
            "timestamp": timestamp,
            "payload": payload,
            "signature": signature,
        }

    def secure_unwrap(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify sender trust, integrity, and replay protection.
        Returns verified payload if valid, or raises an exception.
        """
        node_id = envelope["node_id"]
        timestamp = envelope["timestamp"]
        payload = envelope["payload"]
        signature = envelope["signature"]

        data_str = f"{node_id}|{timestamp}|{payload}"

        if not self.validate_sender(node_id):
            raise PermissionError(f"Untrusted sender: {node_id}")

        if not self.verify_hmac(data_str, signature):
            raise ValueError("Integrity check failed (HMAC mismatch)")

        if self.is_replay(node_id, timestamp):
            raise TimeoutError("Replay or delayed message detected")

        return payload


# ----------------------------- Example Usage -----------------------------
if __name__ == "__main__":
    sm = SafetyManager()

    message = {"city": "Las Vegas", "signal": "ET anomaly"}
    envelope = sm.secure_wrap("NASA", message)
    print("\nSecured message:", envelope)

    verified = sm.secure_unwrap(envelope)
    print("\nVerified payload:", verified)
