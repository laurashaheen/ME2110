from threading import Timer
import myPi
import time

myPi.setup()

while myPi.getButtonState(2) == False:
	myPi.getButtonState(2)

# actuates solenoid, places ray 
myPi.digitalON(2)

myPi.cleanup()