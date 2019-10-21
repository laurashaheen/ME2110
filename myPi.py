# Other RPi Libraries
import RPi.GPIO as GPIO
import time
import threading
from threading import Timer, Thread, Event
import atexit

# MCP Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Motor Library
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

#Stop Flag
stopFlag = False

# Inputs and outputs
LED1 = 19
LED2 = 16
pot = 7
IR = 0
encA = 22
encB = 23
solenoid1 = 12
solenoid2 = 13
valve1 = 5
valve2 = 6

# Buttons are digital inputs
button1 = 4
button1State = False
button2 = 18
button2State = False
button3 = 17
button3State = False
button4 = 27
button4State = False
resetBut = 20

# ADC
SPI_PORT   = 0
SPI_DEVICE = 0
global mcp

# Encoder
counter = 0
global dir

# Motors
mh = Adafruit_MotorHAT(addr=0x60)
global motor1, motor2, motor3, motor4

# Time Related
initTime = 0

# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
# --------------------CORE--------------------
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------

# --------------------------------------------
# Setup
def setup():
    # General setup
    print("Setting up...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # Program start time
    global initTime
    initTime = time.time()
    
    # Reset Button
    GPIO.setup(resetBut, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #pull down resistor for proper readings
    GPIO.add_event_detect(resetBut, GPIO.BOTH, callback = reset, bouncetime=5)
    
    # LED setup
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    
    # Solenoid & Valve setup
    GPIO.setup(solenoid1, GPIO.OUT)
    GPIO.setup(solenoid2, GPIO.OUT)
    GPIO.setup(valve1, GPIO.OUT)
    GPIO.setup(valve2, GPIO.OUT)

    # Set all outputs to low/off
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(solenoid1, False)
    GPIO.output(solenoid2, False)
    GPIO.output(valve1, False)
    GPIO.output(valve2, False)

    # Generic Buttons and Switches
    GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down resistor for proper readings
    GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down resistor for proper readings
    GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down resistor for proper readings
    GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # pull down resistor for proper readings
    
    GPIO.add_event_detect(button1, GPIO.BOTH, callback=button1Actuated, bouncetime=5)  # interrupt for button 1
    GPIO.add_event_detect(button2, GPIO.BOTH, callback=button2Actuated, bouncetime=5)  # interrupt for button 2
    GPIO.add_event_detect(button3, GPIO.BOTH, callback=button3Actuated, bouncetime=5)  # interrupt for button 3
    GPIO.add_event_detect(button4, GPIO.BOTH, callback=button4Actuated, bouncetime=5)  # interrupt for button 4
 
    # ADC
    global mcp
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    
    # Encoder setup
    GPIO.setup(encA, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pull up resistor for proper readings
    GPIO.setup(encB, GPIO.IN, pull_up_down = GPIO.PUD_UP) #pull up resistor for proper readings
    GPIO.add_event_detect(encA, GPIO.BOTH, callback = chA, bouncetime=5) #add interrupt for channel A
    GPIO.add_event_detect(encB, GPIO.BOTH, callback = chB, bouncetime=5) #add interrupt for channel B

    # Motor setup
    global motor1, motor2, motor3, motor4
    motor1 = mh.getMotor(1)
    motor2 = mh.getMotor(2)
    motor3 = mh.getMotor(3)
    motor4 = mh.getMotor(4)

# --------------------------------------------
# Cleanup functionality. Turns off pins to protect them and cleans up variables.
def cleanup():
    GPIO.cleanup()

# --------------------------------------------
# Reset functionality. Called if reset button has been pressed.
def reset(self):
    global stopFlag
    stopFlag = True
    cleanup()
    
def getStopFlag():
    global stopFlag
    stopFlag = GPIO.input(resetBut)
    return stopFlag

# --------------------------------------------
# System "clock." Returns how long the current program has been running
def elapsedTime():
    global initTime
    currTime = time.time()
    return currTime - initTime

# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
# -------------------INPUTS-------------------
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------

# --------------------------------------------
# Buttons
def button1Actuated(self):
    global button1, button1State
    state = GPIO.input(button1)
    if state == 1:
        button1State = True
    else:
        button1State = False
        
def button2Actuated(self):
    global button2, button2State
    state = GPIO.input(button2)
    if state == 1:
        button2State = True
    else:
        button2State = False
    
def button3Actuated(self):
    global button3, button3State
    state = GPIO.input(button3)
    if state == 1:
        button3State = True
    else:
        button3State = False
    
def button4Actuated(self):
    global button4, button4State
    state = GPIO.input(button4)
    if state == 1:
        button4State = True
    else:
        button4State = False
        
def getButtonState(buttonNum):
    global button1State, button2State, button3State, button4State
    global button1, button2, button3, button4
    if buttonNum == 1:
        buttonState = GPIO.input(button1)
    elif buttonNum == 2:
        buttonState = GPIO.input(button2)
    elif buttonNum == 3:
        buttonState = GPIO.input(button3)
    elif buttonNum == 4:
        buttonState = GPIO.input(button4)
    else:
        buttonState = GPIO.input(button1)
    return buttonState

# --------------------------------------------
# Reading analog signals using ADC    
def readADC():
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Return the ADC values.
    return values

# Returns current IR Sensor Value (0-1023)
def readIR():
    global IR
    return mcp.read_adc(IR)

# Returns current Potentiometer Value (0-1023)
def readPOT():
    global pot
    return mcp.read_adc(pot)

# --------------------------------------------
# Encoder Code
# Channel A interrupt
# This will interrupt the main program whenever it detects a rising or falling edge.
# Based on what it detects, it will determine if the encoder is being turned clockwise or anticlockwise.
# This is a separate function that does not immediately run on the main thread.
def chA(channel):
    global counter, dir
    
    # grab current readings
    currA = GPIO.input(encA)
    currB = GPIO.input(encB)
   
    # Scenario 1: Channel A has gone from 0 to 1
    if (currA == 1):
        # Check Channel B's state to determine which way the encoder turned.
        if (currB == 1):
            counter = counter - 1
            dir = "AntiClockwise"
        else:
            counter = counter + 1
            dir = "Clockwise"
            
    # Scenario 2: Channel A has gone from 1 to 0
    else:
        # Check Channel B's state to determine which way the encoder turned.
        if (currB == 1):
            counter = counter + 1
            dir = "Clockwise"
        else:
            counter = counter - 1
            dir = "AntiClockwise"
    
# Channel B interrupt
# This will interrupt the main program whenever it detects a rising or falling edge.
# Based on what it detects, it will determine if the encoder is being turned clockwise or anticlockwise.
# This is a separate function that does not immediately run on the main thread.    
def chB(channel):
    global counter,dir
    
    # grab current readings
    currA = GPIO.input(encA)
    currB = GPIO.input(encB)
    
    # Scenario 1: Channel B has gone from 0 to 1
    if (currB == 1):
        # Check Channel A's state to determine which way the encoder turned.
        if (currA == 1):
            counter = counter + 1
            dir = "Clockwise"
        else:
            counter = counter - 1
            dir = "AntiClockwise"
            
    # Scenario 2: Channel B has gone from 1 to 0
    else:
        # Check Channel A's state to determine which way the encoder turned.
        if (currA == 1):
            counter = counter - 1
            dir = "AntiClockwise"
        else:
            counter = counter + 1
            dir = "Clockwise"
    
# Returns encoder direction
def encDir():
    global dir
    return dir
# Returns encoder count
def encCount():
    global counter
    return counter
    
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
# ------------------OUTPUTS-------------------
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------

# --------------------------------------------
# LED Control
def ledON(ledNUM):
    if ledNUM == 1:
        LED = LED1
    elif ledNUM == 2:
        LED = LED2
    else:
        LED = LED1
    GPIO.output(LED, True)
    
def ledOFF(ledNUM):
    if ledNUM == 1:
        LED = LED1
    elif ledNUM == 2:
        LED = LED2
    else:
        LED = LED1
    GPIO.output(LED, False)   

# --------------------------------------------
def digitalON(portNum):
    global solenoid1, solenoid2, valve1, valve2
    if portNum == 1:
        output = solenoid1
    elif portNum == 2:
        output = solenoid2
    elif portNum == 3:
        output = valve2
    elif portNum == 4:
        output = valve1
    else:
        output = solenoid1
    GPIO.output(output,True)
    
def digitalOFF(portNum):
    global solenoid1, solenoid2, valve1, valve2
    if portNum == 1:
        output = solenoid1
    elif portNum == 2:
        output = solenoid2
    elif portNum == 3:
        output = valve2
    elif portNum == 4:
        output = valve1
    else:
        output = solenoid1
    GPIO.output(output,False)

# --------------------------------------------
# Motor Control
def motorForward(motorNum, speed):
    global motor1, motor2, motor3, motor4
    if speed < 0:
        speed = 0
    elif speed > 255:
        speed = 255
        
    if motorNum == 1:
        myMotor = motor1
    elif motorNum == 2:
        myMotor = motor2
    elif motorNum == 3:
        myMotor = motor3
    elif motorNum == 4:
        myMotor = motor4
    else:
        myMotor = motor1
    
    myMotor.setSpeed(speed)
    myMotor.run(Adafruit_MotorHAT.FORWARD)

def motorBackward(motorNum, speed):
    global motor1, motor2, motor3, motor4
    if speed < 0:
        speed = 0
    elif speed > 255:
        speed = 255
        
    if motorNum == 1:
        myMotor = motor1
    elif motorNum == 2:
        myMotor = motor2
    elif motorNum == 3:
        myMotor = motor3
    elif motorNum == 4:
        myMotor = motor4
    else:
        myMotor = motor1
        
    myMotor.setSpeed(speed)
    myMotor.run(Adafruit_MotorHAT.BACKWARD)

def turnOffMotors():
    global mh
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Program Exit Functionality
atexit.register(turnOffMotors)
atexit.register(cleanup)
