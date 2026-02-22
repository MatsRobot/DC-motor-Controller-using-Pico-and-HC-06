# RobotBase Ver2.2
#
# HC06 pins
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
#          Front Right - FR GP8
#          Front Left  - FL GP9
#          Rear Right  - RR GP10
#          Rear Left   - RL GP11
#
#
# I2C OLED
#          SDA GP18
#          SCL GP19
#

from machine import Pin,I2C,PWM,UART #importing PIN and PWM
import time #importing time
from SSD1306 import SSD1306_I2C
from write import Write
from gfx import GFX
import ubuntu_20, ubuntu_15, ubuntu_12


#declare GP ports for IR sensors
IR_Sensor_FR = Pin(8, Pin.IN)
IR_Sensor_FL = Pin(9, Pin.IN)
IR_Sensor_RR = Pin(10, Pin.IN)
IR_Sensor_RL = Pin(11, Pin.IN)

#declare GP19 for LED and make it blink
LED_Y =  Pin(20, Pin.OUT)
LED_Y.on()
time.sleep_ms(100)
LED_Y.off()
time.sleep_ms(100)

#Defining UART channel and Baud Rate
uart= UART(0,9600)

# L298 Pins
EN_A=PWM(Pin(2))    #ENA
In1=Pin(3,Pin.OUT)  #IN1`
In2=Pin(4,Pin.OUT)  #IN2
In3=Pin(5,Pin.OUT)  #IN3
In4=Pin(6,Pin.OUT)  #IN4
EN_B=PWM(Pin(7))    #ENB

# Defining frequency for enable pins
EN_A.freq(500) #1500
EN_B.freq(500) #1500

# Setting initial duty cycle for maximum speed (0 to 65025)
EN_A.duty_u16(32512) # 65025
EN_B.duty_u16(32512) # 65025


# Define I2C data bus for the OLED and make it display version
i2c = I2C(1,scl = Pin(19),sda = Pin(18),freq = 200000)
SSD1306 = SSD1306_I2C (128,64,i2c)
write20 = Write(SSD1306, ubuntu_15)
write15 = Write(SSD1306, ubuntu_15)
write12 = Write(SSD1306, ubuntu_12)

write20.text("RobotBase Ver2.2", 0, 0)
SSD1306.show()


# Left
def turn_left():
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    
   
# Right
def turn_right():
    In1.high()
    In2.low()
    In3.low()
    In4.high()
    
# Backward
def move_backward():
    In1.high()
    In2.low()
    In3.high()
    In4.low()
    
# Forward
def move_forward():
    In1.low()
    In2.high()
    In3.low()
    In4.high()
    
# Stop
def stop():
    In1.low()
    In2.low()
    In3.low()
    In4.low()

    
while True:
    LED_Y.off()
        
    if uart.any(): #Checking if data available
        data=uart.read() #Getting data
        data=str(data) #Converting bytes to str type
        print(data)
        write12.text("Bluetooth Data:", 0, 15)
        write15.text(str(data) +"                            ", 0, 30)
        SSD1306.show()
        if('Forward' in data):
            move_forward() #Forward
        elif('Backward' in data):
            move_backward() #Backward
        elif('Right' in data):
            turn_right() #Turn Right
        elif('Left' in data):
            turn_left() #Turn Left
        elif('Stop' in data):
            stop() #Stop
        elif('V1' in data):
            speed=data.split("|")
            print(speed[1])
            set_speed = float(speed[1])/100 * 65025
            EN_A.duty_u16(int(set_speed)) #Setting Duty Cycle
            EN_B.duty_u16(int(set_speed)) #Setting Duty Cycle

        else:
            stop() #Stop
            
    if IR_Sensor_FR.value()==0:
        LED_Y.on() #LED on
        write12.text("Stop FR", 0, 50)
        SSD1306.show()
        stop() #Stop
    if IR_Sensor_FL.value()==0:
        LED_Y.on() #LED on
        write12.text("Stop FL", 0, 50)
        SSD1306.show()
        stop() #Stop
    if IR_Sensor_RR.value()==0:
        LED_Y.on() #LED on
        write12.text("Stop RR", 0, 50)
        SSD1306.show()
        stop() #Stop
    if IR_Sensor_RL.value()==0:
        LED_Y.on() #LED on
        write12.text("Stop RL", 0, 50)
        SSD1306.show()
        stop() #Stop
    