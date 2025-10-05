"""
NASA Space Apps 2025 – Trust Authority (Post-Quantum Simulation)
----------------------------------------------------------------
Simulated post-quantum public key infrastructure (PQ-PKI) for agencies.

Implements mock key management inspired by Kyber (encryption) and
Dilithium (signatures). Actual math is replaced by deterministic hashing
to keep this simulation safe and local.
"""

import hashlib
import json
import secrets


class TrustAuthority:
    def __init__(self):
        self.agency_keys = {}

    def register_agency(self, agency_name: str):
        """
        Simulate issuing a Kyber/Dilithium-style key pair.
        """
        public_key = hashlib.sha3_512(agency_name.encode()).hexdigest()
        private_key = hashlib.sha3_256(secrets.token_bytes(32)).hexdigest()
        self.agency_keys[agency_name] = {"public": public_key, "private": private_key}
        print(f"[TrustAuthority] Registered {agency_name} with simulated PQ keys.")
        return public_key

    def sign_message(self, agency_name: str, message: dict):
        """
        Simulate Dilithium digital signature using a hash of the private key and message.
        """
        if agency_name not in self.agency_keys:
            raise ValueError("Agency not registered.")
        private_key = self.agency_keys[agency_name]["private"]
        message_str = json.dumps(message, sort_keys=True)
        signature = hashlib.sha3_512((private_key + message_str).encode()).hexdigest()
        return signature

    def validate_signature(self, agency_name: str, message: dict):
        """
        Verify message authenticity using stored public key (simulated hash check).
        """
        if agency_name not in self.agency_keys:
            return False
        public_key = self.agency_keys[agency_name]["public"]
        msg_str = json.dumps(message, sort_keys=True)
        check_hash = hashlib.sha3_256(msg_str.encode()).hexdigest()[:32]
        return check_hash in public_key


# Example usage
if __name__ == "__main__":
    trust = TrustAuthority()
    trust.register_agency("NOAA")

    msg = {"temperature": 37.2, "risk": "heat"}
    sig = trust.sign_message("NOAA", msg)
    print("Simulated signature:", sig)
    valid = trust.validate_signature("NOAA", msg)
    print("Signature validation result:", valid)
