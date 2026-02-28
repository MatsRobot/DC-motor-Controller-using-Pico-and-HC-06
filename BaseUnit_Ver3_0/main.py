#-----------------------------------------------------------------------------------------------
# BaseUnit_Ver3.0 
#
# Requires the following Libraries
# SSD1360.py with all capital letters
#
#
# The Robot's base unit receives commands from the Bluetooth and the UART interface 
# in the form of plain text to move Right, Left, Forward, Backward and Stop
# in the event of getting too close to an object, the IR sensors overwite the command and
# send a message to the control processor via the same UART as this of the four sensors 
# triggered a stop to assist the mainprocessor move away from the obsticle
#-----------------------------------------------------------------------------------------------
#
# HC06 pins - UART-0
#          RX GP0
#          TX GP1
#
# L298 Pins
#          ENA GP2
#          IN1 GP3`
#          IN2 GP4
#          IN3 GP5
#          IN4 GP6
#          ENB GP7
#
# LED pins
#          Yellow GP20
#
# IR Stop Sensors pins
#          Front Right - FR GP12
#          Front Left  - FL GP13
#          Rear Right  - RR GP14
#          Rear Left   - RL GP15
#
#
# I2C OLED
#          SDA GP18
#          SCL GP19
#
# Main Controller Rapberry Pi, PC or another Pico on UART-1
#          TX GP8
#          RX GP9
#
# AUX Controller I2C-1
#          SDA GP16
#          SCL GP17
#
#
#-----------------------------------------------------------------------------------------------


from machine import Pin, I2C, PWM, UART
import time
from SSD1306 import SSD1306_I2C # Only requires ssd1306.py

# --- Pin Declarations ---
IR_Sensor_FR = Pin(12, Pin.IN)
IR_Sensor_FL = Pin(13, Pin.IN)
IR_Sensor_RR = Pin(14, Pin.IN)
IR_Sensor_RL = Pin(15, Pin.IN)
LED_Y = Pin(20, Pin.OUT)

# --- UART Setup ---
uart0 = UART(0, 9600, tx=Pin(0), rx=Pin(1)) # Bluetooth
uart1 = UART(1, 9600, tx=Pin(8), rx=Pin(9)) # Brain

# --- L298 Motor Driver Setup ---
EN_A = PWM(Pin(2))
In1 = Pin(3, Pin.OUT)
In2 = Pin(4, Pin.OUT)
In3 = Pin(5, Pin.OUT)
In4 = Pin(6, Pin.OUT)
EN_B = PWM(Pin(7))

EN_A.freq(500)
EN_B.freq(500)
EN_A.duty_u16(32512)
EN_B.duty_u16(32512)

# --- Standard OLED Setup ---
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=200000)
oled = SSD1306_I2C(128, 64, i2c)

def update_display(line1, line2, line3):
    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 20)
    oled.text(line3, 0, 45)
    oled.show()


# --- Movement Functions ---
def turn_left(): In1.low(); In2.high(); In3.high(); In4.low()
def turn_right(): In1.high(); In2.low(); In3.low(); In4.high()
def move_backward(): In1.high(); In2.low(); In3.high(); In4.low()
def move_forward(): In1.low(); In2.high(); In3.low(); In4.high()
def stop(): In1.low(); In2.low(); In3.low(); In4.low()

def process_command(raw_data, source):
    try:
        data = raw_data.decode('utf-8').strip()
    except:
        data = str(raw_data)

    if 'Forward' in data: move_forward()
    elif 'Backward' in data: move_backward()
    elif 'Right' in data: turn_right()
    elif 'Left' in data: turn_left()
    elif 'Stop' in data: stop()
    
    update_display(source, "CMD: " + data, "")

while True:
    LED_Y.off()
    if uart0.any(): process_command(uart0.read(), "BT INPUT")
    if uart1.any(): process_command(uart1.read(), "BRAIN INPUT")

    # IR Sensor Check & Feedback
    sensor_msg = "PATH CLEAR"
    if IR_Sensor_FR.value() == 0:
        stop(); uart1.write("FR\n"); LED_Y.on(); sensor_msg = "STOP FR"
    elif IR_Sensor_FL.value() == 0:
        stop(); uart1.write("FL\n"); LED_Y.on(); sensor_msg = "STOP FL"
    elif IR_Sensor_RR.value() == 0:
        stop(); uart1.write("RR\n"); LED_Y.on(); sensor_msg = "STOP RR"
    elif IR_Sensor_RL.value() == 0:
        stop(); uart1.write("RL\n"); LED_Y.on(); sensor_msg = "STOP RL"

    # Minimal refresh to avoid flickering
    oled.fill_rect(0, 45, 128, 20, 0)
    oled.text(sensor_msg, 0, 50)
    oled.show()
    time.sleep(0.05)