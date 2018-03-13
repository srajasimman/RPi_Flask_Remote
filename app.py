#!/usr/bin/env python
'''
	Raspberry Pi GPIO Status and Control
'''
from flask import Flask, render_template
from gpiozero.pins.mock import MockFactory
from gpiozero import OutputDevice, Device


app = Flask(__name__)
Device.pin_factory = MockFactory()

# define GPIO pins for relay
tv = OutputDevice(pin=17, initial_value=False)
dvd = OutputDevice(pin=18, initial_value=False)
set_top_box = OutputDevice(pin=22, initial_value=False)
projector = OutputDevice(pin=23, initial_value=False)
ac = OutputDevice(pin=24, initial_value=False)
fan = OutputDevice(pin=27, initial_value=False)

# initialize GPIO status variables
tv_Sts = 0
dvd_Sts = 0
set_top_box_Sts = 0
projector_Sts = 0
ac_Sts = 0
fan_Sts = 0

@app.route("/")
def index():
    # Read Realay Status
    tv_Sts = tv.value
    dvd_Sts = dvd.value
    set_top_box_Sts = set_top_box.value
    projector_Sts = projector.value
    ac_Sts = ac.value
    fan_Sts = fan.value

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
		actuator.on()

    if action == "off":
		actuator.off()

    tv_Sts = tv.value
    dvd_Sts = dvd.value
    set_top_box_Sts = set_top_box.value
    projector_Sts = projector.value
    ac_Sts = ac.value
    fan_Sts = fan.value

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
