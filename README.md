# 🏎️ Heavy-Duty Drive: Pico & HC-06 DC Motor Controller

A high-current motor control architecture engineered for high-torque **Inductive Loads** (Automotive Wiper Motors). This system bridges a custom Android UI with the **RP2040 PWM engine** for robust wireless mobile robotics.

<p align="center">
  <img width="300" src="https://github.com/user-attachments/assets/2beb45cb-d587-44a7-9c6e-a3a469dc8359" alt="MIT App Inventor Bluetooth Interface" />
</p>

---

## 🚀 Engineering Backstory: Torque vs. Control

Standard hobby-grade motor drivers are insufficient for the current inrush required by 12V automotive wiper motors. This project focuses on managing the **Power Electronics** required for heavy-duty chassis, using the Raspberry Pi Pico to provide the precision timing needed for smooth acceleration curves.

By utilizing the **HC-06 Bluetooth Transceiver** as a transparent UART bridge, the system achieves a 10-meter wireless control radius without the overhead of Wi-Fi or complex network stacks.

## ✨ Key Technical Features

* **Hardware-Timed PWM:** Utilizes the RP2040’s dedicated PWM slices to ensure jitter-free motor speed control independent of CPU load.
* **Transparent UART Bridge:** Low-latency 3.3V TTL communication between the Pico and the HC-06 Bluetooth module.
* **Non-Blocking Parsing:** Firmware architecture allows for real-time command processing (Forward, Reverse, Pivot) without stalling the control loop.
* **Inductive Load Protection:** Designed for use with heavy-duty H-Bridges capable of handling high back-EMF and stall currents.
* **Control Theory Ready:** Includes a modular framework for **PID ($K_p, K_i, K_d$)** implementation, ready for encoder or IMU feedback.

## 🛠️ Hardware Stack

* **MCU:** Raspberry Pi Pico (RP2040).
* **Communication:** HC-06 Bluetooth (Serial Port Profile).
* **Power Stage:** 43A BTS7960 (or similar) High-Current H-Bridge.
* **Actuators:** 2x 12V DC Brushed Wiper Motors.
* **Control Layer:** MIT App Inventor (Android) & MicroPython.

---

## 📐 Logic & Signal Flow

### UART-to-PWM Conversion
The system operates on an **Interrupt-Driven Command Logic**:
1. **Packet Capture:** The HC-06 receives RF signals and pushes ASCII characters to the Pico's UART0 RX buffer.
2. **Logic Branching:** The MicroPython script evaluates the character (e.g., `'F'` = $1111_2$, `'S'` = $0000_2$) to determine the H-Bridge pin states.
3. **Duty Cycle Modulation:** The Pico updates the `PWM.duty_u16()` registers to translate user input into physical velocity.

### Closed-Loop Potential
While this version operates in **Open-Loop**, the internal architecture is built for **Proportional-Integral-Derivative** control. Placeholders for $K_p, K_i,$ and $K_d$ constants are integrated into the global scope to support future quadrature encoder feedback for synchronized wheel velocity.

---

## 📱 The Controller App (MIT App Inventor)

The interface is a dedicated control node:
1. **Directional Matrix:** Maps touch-events to specific UART characters.
2. **Link Monitoring:** Real-time visual feedback on the Bluetooth SPP status.
3. **Parameter Injection:** UI infrastructure designed to pass dynamic PID constants to the Pico's volatile memory for live tuning.

---

<small>© 2026 MatsRobot | Licensed under the [MIT License](https://github.com/MatsRobot/matsrobot.github.io/blob/main/LICENSE)</small>
