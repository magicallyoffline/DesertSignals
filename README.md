# Desert Signals is web-based tool that visualizes real-time air quality and weather data using NASA and open-source APIs. It also uses robotics to monitor the sky and has its own spectrogram.

- Combine NASA OpenAQ, and Open-Meteo data sources. Earthdata.html uses a different API for safety purposes (I am not sure if too many people are using it during the space challenge), so data science and decision making were used to not use other API's for now. This keeps the triad + cybersecurity awareness month in check and not expose anything sensitive (specially those api keys).

- Show near-real-time pollutant concentrations (NO₂, PM₂.₅, O₃, CH₂O, Aerosols, CO)

- Connect these to their environmental causes and public health impacts

- Help users explore the planet interactively and understand how pollution affects life.

- This project is in development — future versions will include richer NASA overlays, historical trends, and automated health alerts. This challenge only has one team member.

  # Video Demo
  Enjoy our 30 second video demo here: 🌕 https://youtu.be/8nuQSTnmLU8 🌕
  - Audio is a custom track produced by me with freshly synthesized and original sounds. Some free NASA sounds were morphed and edited a bit. Those sampled sounds are directly from NASA.gov. Video is more symbolic due to some technical difficulties recording my screen for the front end demo, but the mission remains the same.

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

# Autonomous Space – Post-Quantum Environmental Monitoring Framework

Autonomous Space is a simulated research framework exploring how autonomous robotics, satellites, drones, and ground systems could coordinate environmental monitoring in a secure and ethical way.

The project demonstrates:

- Multi-layer communication between satellites, drones, aircraft, and ground sensors.

- Post-quantum hybrid encryption (Kyber + Dilithium + AES-256 + HMAC).

- Robotics perception (YOLOv8 simulation).

- Secure routing and policy enforcement between simulated agencies (NASA, NOAA, USGS).

- Risk modeling for heat, drought, evapotranspiration, and flood indicators.

- An educational showcase for Earth observation, AI, and cybersecurity integration.

- This is an educational prototype only. No live satellite or aircraft systems are accessed or controlled.

# Autonomous Simulation Workflow

Data Gathering
  - Simulated satellite and drone feeds produce temperature, evapotranspiration, and precipitation data.

Risk Analysis
  - The core/risk.py module evaluates drought and heat conditions.

Consensus Validation
 - NASA, NOAA, and USGS nodes validate the results via the core/consensus.py module.

Secure Communication
 - All routing is performed through hybrid post-quantum crypto routines in core/pqcrypto.py and core/router.py

## Clean Air, Clear Choices – Education & Safety Portal

Purpose:
These pages are designed as a public education resource to help people understand air quality, health protection, and related STEM career pathways. It complements the Autonomous Space project by connecting environmental data science with real-world learning opportunities.

The portal includes:

- Air Pollution Basics: Learn about NO₂, PM₂.₅, O₃, CO, and aerosols.

- Health & Safety Tips: Practical guidance from NASA, WHO, and EPA resources.

- Community Action: Steps to reduce pollution and improve local air quality.

- Training & Careers: Educational programs and verified U.S. job links in NASA, NOAA, and related agencies.

- STEM Roadmap: A simple path for students to begin careers in environmental science, aerospace, or public health.

Educational Intent

All content is based on open data and verified public resources.
No private systems, APIs, or sensitive information are used.
This page exists to promote awareness, sustainability, and accessible education.

# Acknowledgments

- NASA Open Data and Earth Science Programs. NASA Space Apps are funded by NASA's Earth Science Division through a contract with Booz Allen Hamilton, Mindgrub, and SecondMuse.

- NOAA Climate Data Records

- USGS Water Data for the Nation

- Ultralytics YOLOv8 Framework

- NIST Post-Quantum Cryptography Project

- AI for letting me speedrun this project solo — proving caffeine and code can, in fact, orbit together.

- Everyone working toward a cleaner, safer planet (you know who you are).

  # Buy me a coffee
  If you enjoy my work, specially with this 1 person challenge, you may donate crypto here:
  Btc: bc1q6k4hw8e7p7ap6dga02nll444dfcxklvd0qwnkg
  
  Eth: 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Sol: 2FwHfCfAeqfAN4X3mS4ts3hm4uXfg6uYsWcSmp1pwTnZ
  
  XRP: rDPbCNMAKGbD3bVeQxq9AKAmRnbSfCzPNn
  
  BNB:0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  USDC (ETH Stablecoin): 0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  USDT (ETH Stablecoin):0x48CBE58828c11feA3e013E4037Ce0042D6A2182C
  
  Dogecoin: DKvXuFT9nC8fc1TuVsoX5NdXhHe1pmqioN

