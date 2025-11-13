#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import subprocess
import base64
import sys
from openai import OpenAI

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

beepDistance = 31
buzzDistance = 20

vibrate = 36
vibrate2 = 32
client = OpenAI(api_key="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")

MODEL = "gpt-5-nano-2025-08-07"      
IMAGE_PATH = "captured_image.jpg"
RESOLUTION = "640x480"   

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
		Led(GPIO.input(TouchPin))
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
#client = OpenAI(api_key="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")

#MODEL = "gpt-5-nano-2025-08-07"      
#IMAGE_PATH = "captured_image.jpg"
#RESOLUTION = "640x480"             

def capture_image(path: str):
    # -S 2 skips a couple frames so exposure settles faster
    subprocess.run(["fswebcam", "-r", RESOLUTION, "-S", "2", "--no-banner", "--flip", "h", path], check=True)

def to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

def extract_text(resp):
    text = getattr(resp, "output_text", None)
    if text:
        return text.strip()
    try:
        for item in getattr(resp, "output", []):
            for part in getattr(item, "content", []):
                if getattr(part, "type", None) in ("output_text", "text") and getattr(part, "text", None):
                    return part.text.strip()
    except Exception:
        pass
    try:
        return resp.model_dump_json(indent=2)
    except Exception:
        return str(resp)
        
def speak_output(text):
    text = text.replace(" ", "_")
    subprocess.run(("espeak \"" + text + "\" 2>/dev/null").split(" "))

def main():
    try:
        capture_image(IMAGE_PATH)
        data_url = to_data_url(IMAGE_PATH)
        
        

        prompt = (
            "Reply with three to five words "
            "describing the main visible object UNLESS THERE IS TEXT IN THE IMAGE. If there is text, read the text and read the text as the output, with information about what the text is (short description ie. menu, instruction booklet, etc.). If the text is unreadable describe object then reply with \"unreadable text\"."
        )

        resp = client.responses.create(
            model=MODEL,
            reasoning={"effort": "low"},     # minimize hidden reasoning for speed
            max_output_tokens=1024,           # big headroom -> no practical cap
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url}
                ]
            }],
        )
        

        print(extract_text(resp))
        speak_output(extract_text(resp))

    except Exception as e:
        print("ERROR:", repr(e), file=sys.stderr)
        raise

""" if __name__ == "__main__":
    main()
"""

TouchPin = 37
Gpin   = 13
Rpin   = 12

tmp = 0
    

def setup1():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

def Led(x):
	if x == 1:
		main()
	
def Print(x):
	global tmp
	if x != tmp:
		if x == 0:
			print ('    **********')
			print ('    *     ON *')
			print ('    **********')
	
		if x == 1:
			print ('    **********')
			print ('    * OFF    *')
			print ('    **********')
		tmp = x

def loop1():
	while True:
		Led(GPIO.input(TouchPin))


if __name__ == "__main__":
    setup()
    setup1()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
