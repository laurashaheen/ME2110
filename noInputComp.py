# Competition code
from threading import Timer
import myPi
import time

def thisShitSlaps() :
	myPi.motorForward(1,255)

myPi.setup()

# ready sign
myPi.ledON(1)

# waits for banana plugs to actuate
while ~ myPi.getButtonState(1):
	myPi.getButtonState(1)

start = myPi.elapsedTime()
# actuates pneumatics, deploys slides
myPi.digitalON(1)

# actuates slapper arm 
slapper = Timer(3, thisShitSlaps())
myPi.digitalOFF(1)


# limit switch polling block 
while ~ myPi.getButtonState(2) and myPi.elapsedTime() - start < 40:
	myPi.getButtonState(2)

# actuates solenoid, places ray 
if myPi.elapsedTime() - start < 40 :
	time.sleep(1)
	myPi.digitalON(2)

# turns all actuators off 
for i in range(1,4):
	myPi.digitalOFF(i)

myPi.motorForward(1,0)
myPi.motorForward(2,0)

myPi.cleanup()