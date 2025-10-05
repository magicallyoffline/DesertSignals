"""
policy.py
NASA Space Apps 2025 – Policy & Human-In-The-Loop Control System

Purpose:
Implements simulation-level control gates for autonomous decision-making,
rate limiting, and human-in-the-loop oversight. Inspired by NASA/JPL’s
Autonomy and Safety Assurance Framework (ASAF) for Earth observation missions.

Real-world analogs:
 - NASA ASAF / SAFER: policy constraints on autonomous spacecraft actions
 - FAA/NOAA joint protocols for airspace and weather safety
 - USGS review layers for critical environmental warnings
"""

import time
import random
from datetime import datetime
from typing import Dict, Any


class PolicyManager:
    """
    Simulates human-in-the-loop and safety policy control for automated operations.
    """

    def __init__(self):
        self.last_action_timestamp = 0.0
        self.rate_limit_seconds = 3.0  # throttle between major automated actions
        self.hitl_required = {
            "drought_alert": True,
            "flood_warning": True,
            "routine_update": False,
        }

    def _rate_limit(self) -> bool:
        """
        Enforce a time-based throttle between major automated actions.
        """
        now = time.time()
        if now - self.last_action_timestamp < self.rate_limit_seconds:
            return False
        self.last_action_timestamp = now
        return True

    def _human_in_loop(self, action: str) -> bool:
        """
        Simulate human review for critical actions.
        """
        required = self.hitl_required.get(action, False)
        if not required:
            return True
        # simulate a random approval delay
        approved = random.choice([True, True, False])  # 2/3 chance of approval
        decision_time = random.uniform(0.5, 2.5)
        time.sleep(decision_time)
        return approved

    def enforce_policy(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gate the flow of automated decisions through safety, rate-limit, and HITL checks.
        """
        if not self._rate_limit():
            return {"status": "rate_limited", "timestamp": datetime.utcnow().isoformat()}

        approved = self._human_in_loop(action)
        if not approved:
            return {"status": "denied", "reason": "HITL rejection", "action": action}

        # If passed both gates, simulate logged approval
        record = {
            "status": "approved",
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "verified_data": data,
        }
        return record


# Example usage
if __name__ == "__main__":
    pm = PolicyManager()

    test_action = "flood_warning"
    test_data = {"city": "Las Vegas", "risk_level": 0.82}

    result = pm.enforce_policy(test_action, test_data)
    print(result)
