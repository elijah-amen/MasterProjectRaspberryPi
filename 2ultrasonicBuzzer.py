#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Define GPIO pins for ultrasonic sensors
TRIG1 = 11      # GPIO pin for Trig of Ultrasonic Sensor 1
ECHO1 = 12      # GPIO pin for Echo of Ultrasonic Sensor 1
TRIG2 = 15      # GPIO pin for Trig of Ultrasonic Sensor 2
ECHO2 = 16      # GPIO pin for Echo of Ultrasonic Sensor 2

# Define GPIO pin for Buzzer
BuzzerPin = 13

def setup():
    """ Setup the GPIO pins for the ultrasonic sensors and buzzer """
    GPIO.setmode(GPIO.BOARD)
    
    # Setup for ultrasonic sensors
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)

    # Setup for buzzer
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

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

def loop():
    """ Main loop that checks the distances from both sensors and controls the buzzer """
    while True:
        dis1 = distance(TRIG1, ECHO1)
        dis2 = distance(TRIG2, ECHO2)

        # Select the smallest distance from the two sensors
        min_distance = min(dis1, dis2)
        print(f"Closest object detected at: {min_distance} cm")

        if min_distance < 5:  # If the object is within 5 cm, buzz continuously
            buzzer_on()
        elif min_distance < 30:  # If within 30 cm, beep with decreasing interval
            beep_interval = (min_distance - 5) / 50.0  # Adjust beep interval
            beep(beep_interval)
        else:
            buzzer_off()  # Turn off buzzer if object is far
        
        time.sleep(0.3)

def destroy():
    """ Cleanup function to reset GPIO settings """
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
