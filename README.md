# Desert Signals is web-based tool that visualizes real-time air quality and weather data using NASA and open-source APIs.

- Combine NASA TEMPO, OpenAQ, and Open-Meteo data sources

- Show near-real-time pollutant concentrations (NO₂, PM₂.₅, O₃, CH₂O, Aerosols, CO)

- Connect these to their environmental causes and public health impacts

- Help users explore the planet interactively and understand how pollution affects life.

- This project is in development — future versions will include richer NASA overlays, historical trends, and automated health alerts. This challenge only has one team member.

  # Video Demo
  Enjoy our 30 second video demo here: 🌕 https://youtu.be/8nuQSTnmLU8 🌕

# Raspberry Pi Spectrometer — NASA Hackathon Build

This Spectrometer implements a compact, low-cost optical spectrometer for environmental monitoring.
It uses a diffraction grating (1000 lines/mm) and a 0.1 mm slit to disperse light onto a Pi or USB camera.
Python software performs real-time wavelength calibration, normalization, and streaming of spectra and sensor data. It is a blueprint due to other api's being unavailable. The decision to make our own was based on data science.

Features:

- Polynomial wavelength calibration using reference lamp (Hg/Ne/CFL)

- Dark and white frame correction for accurate relative intensity

- Spectral-response compensation → relative radiance output

- Optional near-UV capture for NO₂ / HCHO absorption features

- GPS-tagged data packets for satellite co-location (TEMPO, TROPOMI)

- Optional PM₂.₅, NO₂, HCHO sensors for ground truth

- Flask + Plotly dashboard for live visualization

- Data Flow

- Light enters slit → dispersed by grating → recorded by camera.

- Python extracts and calibrates the spectrum.

- Device metadata (GPS, sensors, timestamp) attached.

- JSON payload sent to server via HTTP POST.

- Dashboard displays live spectra and pollutant readings.

## Hardware

- Raspberry Pi 4 (or 3B+)

-Pi Camera Module or USB Webcam (visible + near-UV sensitive)

- Diffraction grating film 1000 lines/mm

- Precision slit 0.1 mm

- Optional sensors: PMS5003 (PM₂.₅), NO₂ electrochemical, HCHO sensor, GPS HAT

- Matte black enclosure (light-tight)

- Software Stack

- Python 3 / OpenCV / NumPy / SciPy / Flask / Plotly 

- Optional: requests (for HTTP), gpsd-py3 (for GPS)

- Calibration Procedure

- Capture dark frame (cover slit).

- Capture white frame (uniform light).

- Capture reference lamp spectrum and assign known wavelengths.

- Save polynomial coefficients to calibration.json.

- Output

- wavelength_nm[] — Calibrated wavelength axis

- intensity[] — Normalized radiance spectrum

- peaks_nm[] — Detected emission lines

- pps.lat/lon, sensor readings, timestamp

## Dashboard

Run server_dashboard.py to start a local Flask server.
Access via http://localhost:5000 to view live data and location.

  # Disclaimer:
  We are not NASA but enjoy outer space, real life and challenges.

  # Buy me a coffee
  If you enjoy my work, specially this 1 person challenge, you may donate crypto here:
  Btc: bc1q6k4hw8e7p7ap6dga02nll444dfcxklvd0qwnkg
  
  Eth: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Sol: 2FwHfCfAeqfAN4X3mS4ts3hm4uXfg6uYsWcSmp1pwTnZ
  
  XRP: rDPbCNMAKGbD3bVeQxq9AKAmRnbSfCzPNn
  
  BNB:0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  USDC (ETH Stablecoin): 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  USDT (ETH Stablecoin):0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Dogecoin: DKvXuFT9nC8fc1TuVsoX5NdXhHe1pmqioN
  
  SEI: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  ApeCoin: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Pepe: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  PudgyPenguins: 2FwHfCfAeqfAN4X3mS4ts3hm4uXfg6uYsWcSmp1pwTnZ
  
  Bonk: 2FwHfCfAeqfAN4X3mS4ts3hm4uXfg6uYsWcSmp1pwTnZ
  
  Trump: 2FwHfCfAeqfAN4X3mS4ts3hm4uXfg6uYsWcSmp1pwTnZ
  
  AVAX: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Cardano: addr1qxpceal2fxtr7cc2gqfcqvll5dzm2ywyza9zugvrn8aul95r3nm75jvk8a3s5sqnsqellg69k5gug9629csc8x0me7tqwvdhtp
