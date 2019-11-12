# unwrap.py
from threading import Timer
import myPi
import time

myPi.setup()

while True: 
	
	if myPi.getButtonState(1):
		myPi.motorForward(2,255)
	
	if myPi.getButtonState(2):
		myPi.motorBackward(2,255)

myPi.cleanup()