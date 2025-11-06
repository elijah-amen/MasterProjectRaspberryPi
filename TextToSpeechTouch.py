import subprocess
import base64
import sys
from openai import OpenAI
import RPi.GPIO as GPIO

client = OpenAI(api_key="xx")

MODEL = "gpt-5-nano-2025-08-07"      
IMAGE_PATH = "captured_image.jpg"
RESOLUTION = "640x480"             

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
    

def setup():
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

def loop():
	while True:
		Led(GPIO.input(TouchPin))


while True:
    setup()
    loop()
