"""
risk.py
NASA Space Apps 2025 – Environmental Risk Computation Engine

Simulates drought, evapotranspiration (ET), flood, and heat stress risk
based on data inputs from NASA & USGS observation layers:
 - ECOSTRESS (surface temperature)
 - GRACE-FO (groundwater anomalies)
 - Landsat/OpenET (irrigation demand)
 - NASA POWER (climate/weather)
 - GPM (precipitation)
"""

import random
import json


class RiskEngine:
    """
    RiskEngine estimates local environmental risk based on multi-source data.
    Each metric is normalized 0–1, then risk levels are computed per category.
    """

    def __init__(self):
        self.thresholds = {
            "heat": 0.75,
            "drought": 0.65,
            "flood": 0.70,
        }

    # ------------------------------------------------------------------
    # MOCK DATA INPUTS (replaceable with NASA APIs)
    # ------------------------------------------------------------------
    def _get_mock_temperature(self):
        """Simulate ECOSTRESS LST (°C)."""
        return random.uniform(25, 50)

    def _get_mock_precip(self):
        """Simulate GPM rainfall (mm/day)."""
        return random.uniform(0, 100)

    def _get_mock_evapotranspiration(self):
        """Simulate ET from OpenET / Landsat (mm/day)."""
        return random.uniform(0.5, 6.0)

    def _get_mock_groundwater(self):
        """Simulate GRACE-FO groundwater anomaly (cm)."""
        return random.uniform(-10, 10)

    # ------------------------------------------------------------------
    # METRIC CALCULATIONS
    # ------------------------------------------------------------------
    def normalize(self, value, min_val, max_val):
        """Scale to [0, 1]."""
        return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))

    def compute_heat_risk(self, temperature):
        """Heat risk grows exponentially with surface temperature."""
        t_norm = self.normalize(temperature, 20, 50)
        return round(min(1.0, t_norm ** 1.8), 3)

    def compute_drought_risk(self, et, precip, gw):
        """Combine evapotranspiration, precipitation, and groundwater."""
        dryness_index = et - (precip / 50) - (gw / 20)
        d_norm = self.normalize(dryness_index, -1, 5)
        return round(min(1.0, d_norm ** 1.5), 3)

    def compute_flood_risk(self, precip, gw):
        """Flood risk based on rainfall and soil saturation."""
        f_norm = self.normalize(precip + max(0, gw), 0, 120)
        return round(min(1.0, f_norm ** 2), 3)

    # ------------------------------------------------------------------
    # MAIN ANALYSIS LOOP
    # ------------------------------------------------------------------
    def analyze(self, data_sources=None):
        """
        Perform integrated environmental risk analysis.
        Inputs (optional): dict with sensor data, else generate mock.
        """
        temperature = data_sources.get("temperature") if data_sources else self._get_mock_temperature()
        precip = data_sources.get("precip") if data_sources else self._get_mock_precip()
        et = data_sources.get("et") if data_sources else self._get_mock_evapotranspiration()
        gw = data_sources.get("groundwater") if data_sources else self._get_mock_groundwater()

        heat_risk = self.compute_heat_risk(temperature)
        drought_risk = self.compute_drought_risk(et, precip, gw)
        flood_risk = self.compute_flood_risk(precip, gw)

        summary = {
            "temperature_C": round(temperature, 2),
            "precip_mm": round(precip, 2),
            "et_mm": round(et, 2),
            "groundwater_cm": round(gw, 2),
            "risk": {
                "heat": heat_risk,
                "drought": drought_risk,
                "flood": flood_risk,
            },
            "alerts": self._generate_alerts(heat_risk, drought_risk, flood_risk)
        }

        return summary

    # ------------------------------------------------------------------
    # ALERTS & REPORTS
    # ------------------------------------------------------------------
    def _generate_alerts(self, heat, drought, flood):
        alerts = []
        if heat >= self.thresholds["heat"]:
            alerts.append("Heatwave Risk")
        if drought >= self.thresholds["drought"]:
            alerts.append("Drought Conditions")
        if flood >= self.thresholds["flood"]:
            alerts.append("Flood Potential")
        return alerts or ["Normal Conditions"]

