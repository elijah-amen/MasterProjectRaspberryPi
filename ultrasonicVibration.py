#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG = 11       # GPIO pin for Trig of Ultrasonic Sensor
ECHO = 12       # GPIO pin for Echo of Ultrasonic Sensor
VIBRATION_MOTOR = 16  # GPIO pin for Vibration Motor

def setup():
    """ Setup the GPIO pins for the ultrasonic sensor and vibration motor """
    GPIO.setmode(GPIO.BOARD)

    # Setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # Setup for vibration motor
    GPIO.setup(VIBRATION_MOTOR, GPIO.OUT)
    GPIO.output(VIBRATION_MOTOR, GPIO.LOW)  # Turn off the vibration motor initially

def distance():
    """ Measure the distance using the ultrasonic sensor """
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

def vibrate_for_seconds(seconds=0.5):
    """ Activate the vibration motor for a specified number of seconds """
    GPIO.output(VIBRATION_MOTOR, GPIO.HIGH)  # Turn on the vibration motor
    time.sleep(seconds)  # Keep it on for the specified duration
    GPIO.output(VIBRATION_MOTOR, GPIO.LOW)  # Turn off the vibration motor

def loop():
    """ Main loop that checks the distance and controls the vibration motor """
    while True:
        dis = distance()
        print(f"Object detected at: {dis} cm")

        if dis < 20:  # If the distance is less than 20 cm
            vibrate_for_seconds(0.5)  # Vibrate for 0.5 seconds
        
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
