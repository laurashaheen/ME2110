# Competition code
from threading import Timer
import myPi
import time

myPi.setup()

# method defined to start slapper arm after 3sec have elapsed
def thisBoySlaps() :
	myPi.motorForward(1,255)

# method defined to terminate moon arm extension
def retract() : 
	myPi.motorForward(2,0)

# ready sign
myPi.ledON(1)

# waits for banana plugs to actuate
while myPi.getButtonState(1) == False:
	myPi.getButtonState(1)

start = myPi.elapsedTime()
# actuates pneumatics, deploys slides
myPi.digitalON(1)

# actuates moon arm, turns off after 8 seconds 
myPi.motorForward(2,255)
moonArm = Timer(8, retract())

# actuates slapper arm 
slapper = Timer(3, thisBoySlaps())
myPi.digitalOFF(1)


# limit switch polling block 
while myPi.getButtonState(2) == False and myPi.elapsedTime() - start < 40:
	myPi.getButtonState(2)

# actuates solenoid, places ray 
if myPi.elapsedTime() - start < 40 :
	time.sleep(1)
	myPi.digitalON(2)

# turns all actuators off so none are under power after 40s elapse 
for i in range(1,4):
	myPi.digitalOFF(i)

myPi.motorForward(1,0)
myPi.motorForward(2,0)

myPi.cleanup()