# Autonomous Car

A custom autonomous / semi-autonomous ground vehicle built around an **ESP32 main controller** and a **Raspberry Pi host**, using mecanum wheels for omnidirectional movement.

The platform integrates real-time sensor fusion, obstacle avoidance, and remote telemetry into a three-layer architecture: firmware → host software → debug tooling.

---

## Architecture overview

```
┌─────────────────────────────────────────────────────────┐
│                   Raspberry Pi (host)                   │
│  • Auto-detects ESP32/Arduino over USB                  │
│  • Bridges serial ↔ network                             │
│  • Runs ROS2                                            |
|  • Takes USB Camera Feed                                │
└────────────────────┬────────────────────────────────────┘
                     │ USB serial  ($MOVE / $OBSTACLE / …)
┌────────────────────▼────────────────────────────────────┐
│                   ESP32 (ESP_FIRMWARE)                  │
│  • FreeRTOS dual-core task architecture                 │
│  • PCA9685 PWM → 4× mecanum wheel motors                │
│  • 4× VL53L0X ToF (front/rear/left/right)               │
│  • MPU6050 IMU — tilt compensation via rotation matrix  │
│  • TCS34725 colour sensor                               │
│  • ADS1115 ADC                                          │
│  • Obstacle avoider + $MOVE/$ROTATE serial protocol     │
└─────────────────────────────────────────────────────────┘
```

---

## Repository structure

| Directory | Description |
|---|---|
| [`ESP_FIRMWARE/`](ESP_FIRMWARE/) | Arduino/PlatformIO firmware for the ESP32. FreeRTOS tasks, sensor drivers, serial command parser, obstacle avoidance logic. |
| [`rPi software/`](rPi%20software/) | Raspberry Pi host scripts. USB auto-detection, IP/serial bridging, PyQt5 telemetry dashboard (`serial_dashboard.py`). |
| [`Arduino Debug Console/`](Arduino%20Debug%20Console/) | Lightweight serial debug console for direct ESP32 interaction during development. |
| [`images/`](images/) | Photos and diagrams of the physical build. |

Each subdirectory has its own README with setup instructions specific to that layer.

---

## Hardware

| Component | Role |
|---|---|
| ESP32 (dual-core) | Main controller |
| Raspberry Pi | Host — USB bridge, dashboard, network relay |
| Mecanum wheels ×4 | Omnidirectional drive |
| PCA9685 | 16-channel PWM driver for motor ESCs/drivers |
| VL53L0X ×4 | Time-of-flight distance sensors (obstacle detection) |
| MPU6050 | 6-axis IMU (gyro + accelerometer, tilt compensation) |
| TCS34725 | RGB colour sensor |
| ADS1115 | 4-channel 16-bit ADC |

---

## Firmware (ESP_FIRMWARE)

- **FreeRTOS** dual-core operation — motion control and sensing run as separate tasks pinned to independent cores.
- **Serial protocol:** `$MOVE,x-speed,y-speed,rot-speed` for full omnidirectional control; `$ROTATE` for in-place turns; `$OBSTACLE` messages sent back to host when proximity thresholds trigger.
- **I2C bus management:** all sensors share the `Wire` bus with priority scheduling to prevent starvation; VL53L0X sensors use direct register access to avoid blocking library reads.
- **IMU tilt compensation:** rotation-matrix-based correction on live gyro/accel data.
- **Obstacle avoider:** configurable stop-threshold (`$STOPTHRES`) per direction.

See [`ESP_FIRMWARE/README.md`](ESP_FIRMWARE/README.md) for library dependencies and build instructions.

---

## Host software (rPi software)

- Auto-detects connected Arduino/ESP32 devices on USB at startup.
- Exposes serial data over the network and relays IP information back to the microcontroller.
- `serial_dashboard.py` — PyQt5 GUI with live telemetry.

See [`rPi software/README.md`](rPi%20software/README.md) for setup.

---

## Debug console (Arduino Debug Console)

A minimal serial console for interacting with the ESP32 directly without the full dashboard. Useful during firmware bring-up and sensor calibration.

See [`Arduino Debug Console/README.md`](Arduino%20Debug%20Console/README.md) for usage.

---

## Getting started

1. **Flash firmware** — open `ESP_FIRMWARE/` in PlatformIO or Arduino IDE, install bundled libraries from `ESP_FIRMWARE/libraries/`, and flash to the ESP32.
2. **Set up the Pi** — follow `rPi software/README.md` to configure the virtual environment and run `serial_dashboard.py`.
3. **Connect** — power the car, connect the Pi to the ESP32 via USB; the host script auto-detects the port.
4. **Control** — use the dashboard to send move commands and monitor sensor telemetry in real time.
