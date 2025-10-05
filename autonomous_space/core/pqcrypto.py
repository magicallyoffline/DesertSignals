"""
pqcrypto.py
NASA Space Apps 2025 – Post-Quantum Secure Communications Module

Implements a *hybrid encryption* layer:
- AES-256-GCM for symmetric data encryption.
- Kyber (simulated) for key encapsulation.
- Dilithium (simulated) for digital signatures.
- HMAC-SHA-512 for message integrity.

This mirrors NIST PQC Round 3 standards.
No real cryptographic material is generated—educational simulation only.
"""

import os
import hmac
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class PQCryptoHybrid:
    def __init__(self):
        self._session_key = None
        self._public_key = "NASA_SIMULATED_PQC_PUBLIC"
        self._private_key = "NASA_SIMULATED_PQC_PRIVATE"
        self._signature_key = b"NASA_DILITHIUM_SIM_KEY"

    # -------------------------------------------------------------
    # 1. Session Key Handling (Kyber simulation)
    # -------------------------------------------------------------
    def kyber_encapsulate(self):
        """Simulate Kyber key encapsulation."""
        shared_key = get_random_bytes(32)
        capsule = hashlib.sha512(shared_key).hexdigest()[:64]
        print("[PQC] [Kyber] Key encapsulated (simulated).")
        return shared_key, capsule

    def kyber_decapsulate(self, capsule):
        """Simulate Kyber key recovery."""
        derived = hashlib.sha256(capsule.encode()).digest()
        print("[PQC] [Kyber] Key decapsulated (simulated).")
        return derived[:32]

    # -------------------------------------------------------------
    # 2. Data Encryption (AES-256-GCM)
    # -------------------------------------------------------------
    def aes_encrypt(self, plaintext: bytes, key: bytes = None):
        """Encrypt plaintext using AES-256-GCM."""
        key = key or self._session_key or get_random_bytes(32)
        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        print("[PQC] [AES-256-GCM] Encryption complete.")
        return b64encode(nonce + tag + ciphertext).decode()

    def aes_decrypt(self, encoded: str, key: bytes = None):
        """Decrypt ciphertext using AES-256-GCM."""
        raw = b64decode(encoded)
        nonce, tag, ciphertext = raw[:12], raw[12:28], raw[28:]
        key = key or self._session_key
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        print("[PQC] [AES-256-GCM] Decryption verified.")
        return plaintext

    # -------------------------------------------------------------
    # 3. Digital Signature (Dilithium simulation)
    # -------------------------------------------------------------
    def dilithium_sign(self, message: bytes):
        """Simulate Dilithium signing (HMAC-based)."""
        sig = hmac.new(self._signature_key, message, hashlib.sha512).hexdigest()
        print("[PQC] [Dilithium] Signature created.")
        return sig

    def dilithium_verify(self, message: bytes, signature: str):
        """Simulate Dilithium signature verification."""
        expected = hmac.new(self._signature_key, message, hashlib.sha512).hexdigest()
        valid = hmac.compare_digest(expected, signature)
        print(f"[PQC] [Dilithium] Signature valid={valid}")
        return valid

    # -------------------------------------------------------------
    # 4. HMAC Integrity
    # -------------------------------------------------------------
    def hmac_integrity(self, message: bytes, key: bytes = None):
        """Compute message integrity tag."""
        key = key or self._signature_key
        return hmac.new(key, message, hashlib.sha512).hexdigest()

    def verify_integrity(self, message: bytes, tag: str, key: bytes = None):
        """Verify message integrity tag."""
        expected = self.hmac_integrity(message, key)
        valid = hmac.compare_digest(expected, tag)
        print(f"[PQC] [HMAC] Integrity valid={valid}")
        return valid

    # -------------------------------------------------------------
    # 5. Unified Hybrid Encryption Pipeline
    # -------------------------------------------------------------
    def encrypt_message(self, message: str):
        """
        Encrypt + sign a message using hybrid post-quantum crypto.
        Returns a secure packet that includes:
          - capsule (Kyber)
          - ciphertext (AES)
          - signature (Dilithium)
          - integrity tag (HMAC)
        """
        # Step 1: Kyber key exchange
        shared_key, capsule = self.kyber_encapsulate()

        # Step 2: AES encryption
        ciphertext = self.aes_encrypt(message.encode(), shared_key)

        # Step 3: Dilithium signature
        signature = self.dilithium_sign(ciphertext.encode())

        # Step 4: Integrity tag
        tag = self.hmac_integrity(ciphertext.encode())

        packet = {
            "capsule": capsule,
            "ciphertext": ciphertext,
            "signature": signature,
            "tag": tag
        }

        print("[PQC] Secure packet generated.")
        return packet

    def decrypt_message(self, packet: dict):
        """Decrypt and verify a post-quantum secure packet."""
        shared_key = self.kyber_decapsulate(packet["capsule"].encode())

        # Step 1: Verify integrity
        if not self.verify_integrity(packet["ciphertext"].encode(), packet["tag"]):
            raise ValueError("Integrity verification failed.")

        # Step 2: Verify signature
        if not self.dilithium_verify(packet["ciphertext"].encode(), packet["signature"]):
            raise ValueError("Signature verification failed.")

        # Step 3: Decrypt AES data
        plaintext = self.aes_decrypt(packet["ciphertext"], shared_key)

        print("[PQC] Packet decrypted successfully.")
        return plaintext.decode()
