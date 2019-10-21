# Competition code
from threading import Timer
import myPi
import time

myPi.setup()

# ready sign
myPi.ledON(1)

# waits for banana plugs to actuate
while ~ myPi.getButtonState(1):
	myPi.getButtonState(1)

# actuates pneumatics, deploys slides
myPi.digitalON(1)

# actuates slapper arm 
time.sleep(3)
myPi.digitalOFF(1)
myPi.motorForward(1,255)

# limit switch polling block 
while ~ myPi.getButtonState(2)
	myPi.getButtonState(2)

# actuates solenoid, places ray 
myPi.digitalON(2)

# turns all actuators off 
for i in range(1,4)
	myPi.digitalOFF(i)

myPi.motorForward(1,0)
myPi.motorForward(2,0)

myPi.cleanup()