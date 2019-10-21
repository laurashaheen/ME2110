# Competition code
from threading import Timer
import myPi
import time
myPi.setup()

# defined methods ###########################################################################################
# Ray placement timing algo #################################################################################
def Timing(colorC, pos):
    timing = -1*(1 - colorC)*(5/2) 
    timing += pos*(5/4)

    condition = (round(myPi.elapsedTime()) - timing)%10 == 0
    return condition

# Quadrant color ############################################################################################
def getQuadColor():
    print("Please input quadrant color:")
    colorQ = str(raw_input())

    if colorQ.lower() == 'r' or colorQ.lower() == 'red' or colorQ.lower() == 'black':
            order = ['r','b','w','y']
            return order;
    elif colorQ.lower() == 'b' or colorQ.lower() == 'blue':
            order = ['b','w','y','r']
            return order;
    elif colorQ.lower() == 'w' or colorQ.lower() == 'white':
            order = ['w','y','r','b']
            return order;
    elif colorQ.lower() == 'y' or colorQ.lower() == 'yellow':
            order = ['y','r','b','w']
            return order;
    else :
            print("Invalid Input: {}.\n Please try again.".format(colorQ))
            getQuadColor()

# center color ###############################################################################################
def getCenterColor(order):
    print("Please input center color:")
    colorC = str(raw_input())
    i = 0
    
    if colorC.lower() == 'r' or colorC.lower() == 'red' or colorC.lower() == 'black':
            while order[i] != 'r':
                    i += 1
            return i+1
    elif colorC.lower() == 'b' or colorC.lower() == 'blue':
            while order[i] != 'b':
                    i += 1
            return i+1
    elif colorC.lower() == 'w' or colorC.lower() == 'white':
            while order[i] != 'w':
                    i += 1
            return i+1
    elif colorC.lower() == 'y' or colorC.lower() == 'yellow':
            while order[i] != 'y':
                    i += 1
            return i+1
    else :
            print("Invalid Input: {}.\n Please try again.".format(colorC))
            getCenterColor(order)
# center alignment ############################################################################################
def getPos() :
	print("Please input center position: Enter/Exit/Center")
	pos = str(raw_input())
	if pos.lower() == 'ent' or pos.lower() == 'enter' :
		return 1
	elif pos.lower() == 'ex' or pos.lower() == 'exit' :
		return -1
	else : 
		return 0

# reset functionality #########################################################################################
def reset():
    for i in range(1,4):
            myPi.digitalOFF(i)
    myPi.motorForward(1,0)
    myPi.motorForward(2,0)

# global vars #################################################################################################
order = getQuadColor()
colorC = getCenterColor(order)
pos = getPos()

# ready message ###############################################################################################
if True: 
    print("System Ready")

print("Deploy? Y/N")
goNoGo = str(raw_input())

if goNoGo.lower() == "y":
    print("Nice B) \n Please connect banana plugs to actuate.")
    myPi.ledON(1)
    while myPi.getButtonState(1) == False: # for comp on wed
        myPi.getButtonState(1)

    start = myPi.elapsedTime()

	# deploy slides #########################################################################################
    myPi.digitalON(1)
    print("pneumatics deployed")

    # deploy sweeper ########################################################################################
    time.sleep(3)
    myPi.motorForward(2,255)
    
    print('motor running')

    # deploy moon ###########################################################################################
            #nothing for now

	# drive

    ## deploy ray ###########################################################################################
    ## limit switch
    # while myPi.getButtonState(2) and myPi.elapsedTime() - start < 40:
    #       myPi.getButtonState(2)
    ##  <code to place ray>

    ## OR
	## timer method
	
    while Timing(colorC, pos) == False and ((myPi.elapsedTime() - start) < 40):
		Timing(colorC, pos)
		
    if myPi.elapsedTime() - start > 40 :
		print("infinite loop")
    else :	
    	print('lo hicimos')
        myPi.motorBackward(1,255)
        time.sleep(.5)
        myPi.motorForward(1,255)
        time.sleep(.5)
	
else: Print("uhhhh okay then :/")

myPi.cleanup()