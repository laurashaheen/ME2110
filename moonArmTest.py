from threading import Timer
import myPi
import time

myPi.setup()

print("running for 5 seconds")

start = myPi.elapsedTime()

while (myPi.elapsedTime() - start < 5) :
	myPi.motorForward(2,255)

while (myPi.elapsedTime() - start < 10) :
	myPi.motorBackward(2,255)

myPi.cleanup()