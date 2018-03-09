'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define actuators GPIOs
relay1 = 23
relay2 = 24

#initialize GPIO status variables
relay1_Sts = 0
relay2_Sts = 0

# Define button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)
GPIO.setup(senPIR, GPIO.IN)

# Define led pins as output
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

# turn leds OFF
GPIO.output(relay1, GPIO.LOW)
GPIO.output(relay2, GPIO.LOW)

@app.route("/")
def index():
	# Read GPIO Status
	relay1_Sts = GPIO.input(relay1)
	relay2_Sts = GPIO.input(relay2)

	templateData = {
      'relay1'  : relay1_Sts,
      'relay2'  : relay2_Sts,
      }
	return render_template('index.html', **templateData)

# The function below is executed when someone requests a URL with the actuator name and action in it:
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'relay1':
		actuator = relay1
	if deviceName == 'relay2':
		actuator = relay2

	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)

	relay1_Sts = GPIO.input(relay1)
	relay2_Sts = GPIO.input(relay2)

	templateData = {
      'relay1'  : relay1_Sts,
      'relay2'  : relay2_Sts,
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
