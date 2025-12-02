#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Define GPIO pins for ultrasonic sensors
TRIG1 = 11      # GPIO pin for Trig of Ultrasonic Sensor 1
ECHO1 = 12      # GPIO pin for Echo of Ultrasonic Sensor 1
TRIG2 = 15                                                                      # GPIO pin for Trig of Ultrasonic Sensor 2
ECHO2 = 16      # GPIO pin for Echo of Ultrasonic Sensor 2
TRIG3 = 38
ECHO3 = 40

# Define GPIO pin for Buzzer
BuzzerPin = 13
BuzzerPin2 = 18

beepDistance = 20
buzzDistance = 20

vibrate = 36
vibrate2 = 36

#beep_interval = 2

def setup():
    """ Setup the GPIO pins for the ultrasonic sensors and buzzer """
    GPIO.setmode(GPIO.BOARD)
    
    # Setup for ultrasonic sensors
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)
    GPIO.setup(TRIG3, GPIO.OUT)
    GPIO.setup(ECHO3, GPIO.IN)

    # Setup for buzzer
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
    # Setup for buzzer
    GPIO.setup(BuzzerPin2, GPIO.OUT)
    GPIO.output(BuzzerPin2, GPIO.HIGH)
    
    GPIO.setup(vibrate, GPIO.OUT)
    GPIO.output(vibrate, GPIO.LOW)
    
    GPIO.setup(vibrate2, GPIO.OUT)
    GPIO.output(vibrate2, GPIO.LOW)

def distance(TRIG, ECHO):
    """ Measure the distance using an ultrasonic sensor """
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    time1 = time.time()
    
    while GPIO.input(ECHO) == 1:                                                                                
        pass
    time2 = time.time()

    duration = time2 - time1
    return (duration * 340 / 2) * 100  # Convert to centimeters

def buzzer_on():
    """ Turn the buzzer on """
    GPIO.output(BuzzerPin, GPIO.LOW)

def buzzer_off():
    """ Turn the buzzer off """
    GPIO.output(BuzzerPin, GPIO.HIGH)

def beep(duration):
    """ Make the buzzer beep for a specified duration """
    buzzer_on()
    time.sleep(duration)
    buzzer_off()
    time.sleep(duration)
    
def buzzer_on2():
    """ Turn the buzzer on """
    GPIO.output(BuzzerPin2, GPIO.LOW)

def buzzer_off2():
    """ Turn the buzzer off """
    GPIO.output(BuzzerPin2, GPIO.HIGH)

def beep2(duration):
    """ Make the buzzer beep for a specified duration """
    buzzer_on2() 
    time.sleep(duration)
    buzzer_off2()
    time.sleep(duration)
    
def buzzer_on3():
    """ Turn the buzzer on """
    GPIO.output(BuzzerPin, GPIO.LOW)
    GPIO.output(BuzzerPin2, GPIO.LOW)

def buzzer_off3():
    """ Turn the buzzer off """
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.output(BuzzerPin2, GPIO.HIGH)

def beep3(duration):
    """ Make the buzzer beep for a specified duration """
    buzzer_on() 
    #time.sleep(0.1)
    buzzer_on2()
    time.sleep(duration)
    buzzer_off3()
    time.sleep(duration)
    
def vibrate_on():
    GPIO.output(vibrate, GPIO.HIGH)
    
def vibrate_off():
    GPIO.output(vibrate, GPIO.LOW)
    
def vibrate_on2():
    GPIO.output(vibrate2, GPIO.HIGH)
    
def vibrate_off2():
    GPIO.output(vibrate2, GPIO.LOW)

def loop():
    """ Main loop that checks the distances from both sensors and controls the buzzer """
    while True:
        dis1 = distance(TRIG1, ECHO1)
        dis2 = distance(TRIG2, ECHO2)
        dis3 = distance(TRIG3, ECHO3)

        # Select the smallest distance from the two sensors
        # min_distance = min(dis1, dis2)
        # print(f"Closest object detected at: {min_distance} cm")
        
        if dis3 < buzzDistance:  # If the object is within 5 cm, buzz continuously
            beep3(1)
        elif dis3 < beepDistance:  # If within 30 cm, beep with decreasing interval
            beep_interval = (dis3 - 5) / 50.0  # Adjust beep interval
            #beep3(beep_interval)
            vibrate_on()
            vibrate_on2()
        
         #time.sleep(0.3)

        elif dis1 < buzzDistance:  # If the object is within 5 cm, buzz continuously
            buzzer_on()
        elif dis1 < beepDistance:  # If within 30 cm, beep with decreasing interval
            beep_interval = (dis1 - 5) / 50.0  # Adjust beep interval
            #beep(beep_interval)
            vibrate_on()
            # time.sleep(0.3)
        elif dis2 < buzzDistance:  # If the object is within 5 cm, buzz continuously
            buzzer_on2()
        elif dis2 < beepDistance:  # If within 30 cm, beep with decreasing interval
            beep_interval = (dis2 - 5) / 50.0  # Adjust beep interval
            #beep2(beep_interval)
            vibrate_on2()
            # time.sleep(0.3)
        else:
            # Turn off buzzer if object is far
            buzzer_off3()
            vibrate_off()
            vibrate_off2()

        
        
        

def destroy():
    """ Cleanup function to reset GPIO settings """
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
