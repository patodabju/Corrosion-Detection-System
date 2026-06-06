# Corrosion Detection System

## Overview

This project implements an automated corrosion inspection system based on an ESP32 microcontroller and a TCS230 color sensor.

The system is designed to classify metallic specimens as either:

- Corroded
- Non-corroded

using optical measurements obtained under controlled lighting conditions.

A custom 3D-printed enclosure ensures repeatable measurements by maintaining a fixed sensor-to-sample distance and eliminating the influence of ambient light.

---

## System Architecture

```text
Metal Specimen
        ↓
TCS230 Color Sensor
        ↓
ESP32
        ↓
Classification Algorithm
        ↓
USB Serial Communication
        ↓
Python Data Acquisition Software
        ↓
CSV / Excel Database
        ↓
Live Dashboard and Historical Records
```

## Features

- Corrosion detection using reflected light measurements.
- Controlled optical chamber for repeatable readings.
- Push-button acquisition system.
- Automatic specimen classification.
- Timestamp generation from the host computer.
- Continuous data logging.
- Excel-compatible database generation.
- Real-time dashboard visualization.
- Historical inspection record storage.

## Hardware

### Main Components

- ESP32 Development Board
- TCS230 Color Sensor
- Push Button
- USB Connection
- Custom 3D Printed Enclosure

### Measurement Chamber

The enclosure is designed to:

- Block external light sources.
- Maintain a fixed sensor-to-sample distance.
- Ensure repeatable measurements.
- Provide quick specimen insertion and removal.

## Software Components

### ESP32 Firmware

Responsible for:

- Reading TCS230 sensor values.
- Capturing measurements on button press.
- Processing sensor readings.
- Determining corrosion state.
- Sending classification results through serial communication.

### Python Acquisition Software

Responsible for:

- Monitoring the serial port.
- Receiving inspection results.
- Generating timestamps.
- Storing inspection records.
- Updating the inspection database.

### Excel Dashboard

Responsible for:

- Visualizing inspection history.
- Displaying corrosion statistics.
- Tracking inspection timestamps.
- Providing a user-friendly interface for data analysis.

## Data Structure

Each inspection record contains:

| Timestamp | State |
|------------|---------|
| YYYY-MM-DD HH:MM:SS | Corroded / Non-corroded |

Example:

| Timestamp | State |
|------------|---------|
| 2026-06-05 16:32:10 | Corroded |
| 2026-06-05 16:35:42 | Non-corroded |

## Future Improvements

- Multi-level corrosion classification.
- Corrosion severity estimation.
- Wi-Fi connectivity.
- Cloud database integration.
- Machine learning based classification.
- Statistical process monitoring.
- Automated report generation.

## Author

Developed as an engineering instrumentation and automation project using ESP32 and optical sensing technologies.