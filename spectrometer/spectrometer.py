#!/usr/bin/env python3
"""
Advanced Raspberry Pi Spectrometer
----------------------------------
Features:
 - Diffraction grating film (1000 lines/mm)
 - Controlled slit width (0.1 mm)
 - Polynomial wavelength calibration (using reference lamp lines)
 - Dark and white frame normalization
 - Spectral response correction → relative radiance
 - Optional near-UV extension (requires UV-sensitive optics)
 - GPS tagging and pollutant sensor integration
 - Data push to Flask/Plotly dashboard
"""

import cv2
import numpy as np
import time, json, requests, os, threading
from datetime import datetime
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from pathlib import Path
from gpsd import gps

# --------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------
SERVER_URL = "http://YOUR_SERVER_IP:5000/ingest"
CAL_FILE = Path("calibration.json")
RESPONSE_FILE = Path("spectral_response.json")
ROI_Y = [220, 260]
POLY_ORDER = 3
CAP_INDEX = 0
WIDTH, HEIGHT = 1280, 720
POST_INTERVAL = 15
SAVE_DIR = Path("captures")
SAVE_DIR.mkdir(exist_ok=True)

# --------------------------------------------------------------------
# GPS HANDLER
# --------------------------------------------------------------------
def get_gps_fix():
    try:
        g = gps()
        g.connect()
        data = g.get_current()
        return {"lat": data["lat"], "lon": data["lon"]}
    except Exception:
        return {"lat": None, "lon": None}

# --------------------------------------------------------------------
# CALIBRATION UTILITIES
# --------------------------------------------------------------------
def save_calibration(pixels, wavelengths):
    coeffs = np.polyfit(pixels, wavelengths, POLY_ORDER)
    json.dump({"coeffs": coeffs.tolist()}, open(CAL_FILE, "w"))
    print("Calibration saved:", coeffs)

def load_calibration():
    if CAL_FILE.exists():
        d = json.load(open(CAL_FILE))
        return np.array(d["coeffs"])
    # Fallback rough calibration
    return np.polyfit([100, 300], [430, 550], POLY_ORDER)

coeffs = load_calibration()
def pix_to_nm(p): return np.polyval(coeffs, p)

# --------------------------------------------------------------------
# DARK/WHITE FRAME NORMALIZATION
# --------------------------------------------------------------------
dark_frame = None
white_frame = None

def capture_reference_frames(cap):
    global dark_frame, white_frame
    print("Capturing dark frame (cover slit)...")
    time.sleep(3)
    _, dark_frame = cap.read()
    print("Now capture white frame (uniform lamp or white LED)...")
    time.sleep(3)
    _, white_frame = cap.read()
    np.save("dark.npy", dark_frame)
    np.save("white.npy", white_frame)
    print("Reference frames saved.")

def load_reference_frames():
    global dark_frame, white_frame
    if os.path.exists("dark.npy") and os.path.exists("white.npy"):
        dark_frame = np.load("dark.npy")
        white_frame = np.load("white.npy")

load_reference_frames()

def normalize_frame(frame):
    if dark_frame is None or white_frame is None:
        return frame
    corrected = (frame.astype(np.float32) - dark_frame.astype(np.float32))
    white_corr = (white_frame.astype(np.float32) - dark_frame.astype(np.float32))
    white_corr[white_corr <= 0] = 1
    norm = np.clip(corrected / white_corr, 0, 1)
    return (norm * 255).astype(np.uint8)

# --------------------------------------------------------------------
# SPECTRAL RESPONSE CORRECTION
# --------------------------------------------------------------------
def load_response_curve():
    if RESPONSE_FILE.exists():
        d = json.load(open(RESPONSE_FILE))
        return np.array(d["wavelength_nm"]), np.array(d["response"])
    return None, None

def save_response_curve(wavelengths, response):
    json.dump({"wavelength_nm": wavelengths.tolist(), "response": response.tolist()}, open(RESPONSE_FILE, "w"))
    print("Spectral response curve saved.")

response_wl, response_val = load_response_curve()

def apply_response_correction(wavelengths, intensity):
    if response_wl is None:
        return intensity
    interp = np.interp(wavelengths, response_wl, response_val)
    interp[interp <= 0] = 1
    corrected = intensity / interp
    return corrected

# --------------------------------------------------------------------
# FRAME → SPECTRUM PIPELINE
# --------------------------------------------------------------------
def extract_spectrum(frame, roi):
    frame = normalize_frame(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    band = gray[roi[0]:roi[1], :]
    intensity = np.mean(band, axis=0)
    intensity = gaussian_filter1d(intensity, 2)
    return intensity

# --------------------------------------------------------------------
# MAIN CAPTURE LOOP
# --------------------------------------------------------------------
def capture_loop():
    cap = cv2.VideoCapture(CAP_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # Optional reference capture
    if dark_frame is None or white_frame is None:
        capture_reference_frames(cap)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        spectrum = extract_spectrum(frame, ROI_Y)
        pixels = np.arange(len(spectrum))
        wavelengths = pix_to_nm(pixels)
        spectrum = apply_response_correction(wavelengths, spectrum)
        spectrum /= np.max(spectrum)

        peaks, props = find_peaks(spectrum, height=np.max(spectrum) * 0.05, distance=5)
        gpsfix = get_gps_fix()

        payload = {
            "timestamp": time.time(),
            "gps": gpsfix,
            "wavelength_nm": wavelengths.tolist(),
            "intensity": spectrum.tolist(),
            "peaks_nm": pix_to_nm(peaks).tolist(),
            "roi_y": ROI_Y,
            "coeffs": coeffs.tolist()
        }

        try:
            requests.post(SERVER_URL, json=payload, timeout=2)
        except Exception as e:
            print("Post failed:", e)

        # Save snapshot for validation
        fname = SAVE_DIR / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(str(fname), frame)
        print("Frame saved:", fname)

        time.sleep(POST_INTERVAL)

# --------------------------------------------------------------------
# REFERENCE CALIBRATION ROUTINE
# --------------------------------------------------------------------
def calibrate_with_reference(cap):
    print("Use reference lamp (mercury/neon/CFL). Capturing frame...")
    _, frame = cap.read()
    spectrum = extract_spectrum(frame, ROI_Y)
    pixels = np.arange(len(spectrum))

    # Identify emission peaks
    peaks, props = find_peaks(spectrum, height=np.max(spectrum)*0.1, distance=5)
    print("Detected peaks at pixels:", peaks)

    # Known reference wavelengths for mercury lamp (nm)
    known_lines = [404.7, 435.8, 546.1, 577.0]
    user_map = []
    for i, wl in enumerate(known_lines):
        if i < len(peaks):
            user_map.append((peaks[i], wl))
    pix, wls = zip(*user_map)
    save_calibration(pix, wls)

# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
if __name__ == "__main__":
    cap = cv2.VideoCapture(CAP_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    ans = input("Calibrate with reference lamp? [y/N]: ").strip().lower()
    if ans == "y":
        calibrate_with_reference(cap)

    capture_loop()
