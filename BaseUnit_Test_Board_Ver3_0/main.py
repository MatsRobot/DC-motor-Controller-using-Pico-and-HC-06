#-----------------------------------------------------------------------------------------------
# BaseUnit_Test_Board_Ver3_0
#
# Requires the following Libraries
# SSD1360.py with all capital letters
#-----------------------------------------------------------------------------------------------
#
# 5 Switches with pulled up 10K resistors to 3.3V create the following commands
# Right-GP11, Backward-GP12. Stop-GP13, Forward-GP14, Left-GP15
#
# UART communication at 9600 baud rate connected to GP8 and GP9
#
# SSD1360.py Library for OLED with all capital letters
# OLED is connected to I2C-1 GP18 and GP19
#
# Feedback LEDs on fr=GP16, fl=GP17, rr=GP20, rl=GP21
#
# 3 wire communication connection 
#   Ground-Pico1 to Ground-Pico2
#   RX-Pico1 to TX-Pico2
#   TX-Pico1 to RX-Pico2
#
# The fourth wire Power line is not connected but Schottky Diode 1N5819 is used 
# to protect the Picos if a positive line gets connected to a +5V supply
# 
#-----------------------------------------------------------------------------------------------
 
from machine import Pin, UART, I2C
import time
from SSD1306 import SSD1306_I2C     # SSD1360.py with all capital letters

# UART communication at 9600 baud rate connected to GP8 and GP9
uart = UART(1, 9600, tx=Pin(8), rx=Pin(9))

# OLED is connected to I2C-1 GP18 and GP19
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)

# Buttons (Active Low)
sw_right=Pin(11, Pin.IN)
sw_back=Pin(12, Pin.IN)
sw_stop=Pin(13, Pin.IN)
sw_fwd=Pin(14, Pin.IN)
sw_left=Pin(15, Pin.IN)

# Feedback LEDs
led_fr=Pin(16, Pin.OUT)
led_fl=Pin(17, Pin.OUT)
led_rr=Pin(20, Pin.OUT)
led_rl=Pin(21, Pin.OUT)

last_sent_stop = False
last_sensor = "CLEAR"

while True:
    # 1. RX from Base
    if uart.any():
            raw_rx = uart.readline()
            
            # Check if raw_rx is not None before decoding
            if raw_rx is not None:
                try:
                    # This removes the 'NoneType' error warning
                    if isinstance(raw_rx, bytes):
                        rx = raw_rx.decode('utf-8').strip()
                    
                    # Update LEDs (1 is ON, 0 is OFF)
                    led_fr.value(1 if rx == "FR" else 0)
                    led_fl.value(1 if rx == "FL" else 0)
                    led_rr.value(1 if rx == "RR" else 0)
                    led_rl.value(1 if rx == "RL" else 0)
                    
                    if rx in ["FR", "FL", "RR", "RL"]:
                        last_sensor = "STOP " + rx
                    else:
                        last_sensor = "CLEAR"
                except Exception:
                    # If it's partial data or a glitch, just skip this frame
                    pass

    # 2. TX to Base (Momentary)
    cmd = None
    if sw_fwd.value() == 0: cmd = "Forward"
    elif sw_back.value() == 0: cmd = "Backward"
    elif sw_left.value() == 0: cmd = "Left"
    elif sw_right.value() == 0: cmd = "Right"
    elif sw_stop.value() == 0: cmd = "Stop"

    if cmd:
        uart.write(cmd + "\n")
        last_sent_stop = False
    elif not last_sent_stop:
        uart.write("Stop\n")
        last_sent_stop = True

    # 3. Display
    oled.fill(0)
    oled.text("BRAIN CTRL", 0, 0)
    oled.text("SEND: " + (cmd if cmd else "IDLE"), 0, 20)
    oled.hline(0, 35, 128, 1)
    oled.text("SENSOR: " + last_sensor, 0, 45)
    oled.show()
    time.sleep(0.05)