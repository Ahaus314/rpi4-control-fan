#!/usr/bin/python

import RPi.GPIO as GPIO
import time, datetime
import os
import traceback

DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
INTERVAL = 10
MINIMAL_TEMPERATURE = float(30.0)
MAXIMAL_TEMPERATURE = float(80.0)

MAXIMAL_SPEED = 100
MINIMAL_SPEED = 1

previousSpeed = 0
currentSpeed = 0

def getCpuTemperature():
	temperature = os.popen('vcgencmd measure_temp').readline()
	#return float(70.0)
	return float(temperature.replace("temp=","").replace("'C\n",""))

def setFanSpeed(temperature, speed):
	if int(speed) == 0:
		pwm.stop()
	else:
		pwm.start(speed)
	
	printMessage("current cpu temperature: %.1f'C with speed: %.3f" % (cpuTemperature, speed))

def calculateFanSpeed(cpuTemperature, previousSpeed):
	temperatureCoeficient = MAXIMAL_TEMPERATURE /MINIMAL_TEMPERATURE
	speedCoeficient = MINIMAL_TEMPERATURE /MAXIMAL_TEMPERATURE
	
	currentSpeed = (cpuTemperature *temperatureCoeficient) - (speedCoeficient *(MAXIMAL_SPEED -previousSpeed)) -(MAXIMAL_TEMPERATURE/2 - MINIMAL_TEMPERATURE/2)
	#printMessage("previous speed: %.0f; current speed: %.0f; temperatureCoeficient: %f; speedCoeficient: %f" % (previousSpeed, currentSpeed, temperatureCoeficient *1.0, speedCoeficient *1.0))
	
	if currentSpeed > MAXIMAL_SPEED:
		currentSpeed = MAXIMAL_SPEED
	elif currentSpeed < MINIMAL_SPEED:
		currentSpeed = MINIMAL_SPEED
	
	return currentSpeed
        
def printMessage(message):
	print(datetime.datetime.now().strftime(DATE_FORMAT) + " %s" % message)

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setwarnings(False)
pwm = GPIO.PWM(2, MAXIMAL_SPEED)

try:
    printMessage("starting monitoring cpu temperature...")
    
    while True:

        cpuTemperature = getCpuTemperature()
        currentSpeed = calculateFanSpeed(cpuTemperature, previousSpeed)
        
        if cpuTemperature > 70.0:
            setFanSpeed(cpuTemperature, MAXIMAL_SPEED)
            
        elif cpuTemperature > 30.0:
            setFanSpeed(cpuTemperature, currentSpeed)

        else:
            setFanSpeed(cpuTemperature, MINIMAL_SPEED)
            printMessage("fan goes off")
             
        time.sleep(INTERVAL)
        previousSpeed = currentSpeed
        
except KeyboardInterrupt:
    printMessage("exiting...")
        
except:
    printMessage("unknown error occured...\n%s" % traceback.print_exc())
        
finally:
    GPIO.cleanup()
