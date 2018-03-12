#!/usr/bin/env python
'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define GPIO pins for relay
tv = 17
dvd = 18
set_top_box = 22
projector = 23
ac = 24
fan = 27


# initialize GPIO status variables
tv_Sts = 0
dvd_Sts = 0
set_top_box = 0
projector = 0
ac = 0
fan = 0

# Define relay pins as output
GPIO.setup(tv, GPIO.OUT)
GPIO.setup(dvd, GPIO.OUT)
GPIO.setup(set_top_box, GPIO.OUT)
GPIO.setup(projector, GPIO.OUT)
GPIO.setup(ac, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)


# turn relay OFF at start
GPIO.output(tv, GPIO.LOW)
GPIO.output(dvd, GPIO.LOW)
GPIO.output(set_top_box, GPIO.LOW)
GPIO.output(projector, GPIO.LOW)
GPIO.output(ac, GPIO.LOW)
GPIO.output(fan, GPIO.LOW)


@app.route("/")
def index():
    # Read Realay Status
    tv_Sts = GPIO.input(tv)
    dvd_Sts = GPIO.input(dvd)
    set_top_box_Sts = GPIO.input(set_top_box)
    projector_Sts = GPIO.input(projector)
    ac_Sts = GPIO.input(ac)
    fan_Sts = GPIO.input(fan)

    templateData = {
        'tv': tv_Sts,
        'dvd': dvd_Sts,
        'set_top_box': set_top_box_Sts,
        'projector': projector_Sts,
        'ac': ac_Sts,
        'fan': fan_Sts,
    }
    return render_template('index.html', **templateData)


# The function below is executed when someone requests
# a URL with the actuator name and action in it:
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'tv':
        actuator = tv

    if deviceName == 'dvd':
        actuator = dvd

    if deviceName == 'set_top_box':
        actuator = set_top_box

    if deviceName == 'projector':
        actuator = projector

    if deviceName == 'ac':
        actuator = ac

    if deviceName == 'fan':
        actuator = fan

    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)

    if action == "off":
        GPIO.output(actuator, GPIO.LOW)

    tv_Sts = GPIO.input(tv)
    dvd_Sts = GPIO.input(dvd)
    set_top_box_Sts = GPIO.input(set_top_box)
    projector_Sts = GPIO.input(projector)
    ac_Sts = GPIO.input(ac)
    fan_Sts = GPIO.input(fan)

    templateData = {
        'tv': tv_Sts,
        'dvd': dvd_Sts,
        'set_top_box': set_top_box_Sts,
        'projector': projector_Sts,
        'ac': ac_Sts,
        'fan': fan_Sts,
    }
    return render_template('index.html', **templateData)


if __name__ == "__main__":
    try:
        exit(app.run(host='0.0.0.0', port=8080, debug=True))
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
