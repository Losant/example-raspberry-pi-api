import json
from gpiozero import LED # Import GPIO library: https://gpiozero.readthedocs.io/en/stable/
from time import sleep
from losantmqtt import Device # Import Losant library: https://github.com/Losant/losant-mqtt-python

# We need to describe what GPIO is available to control.
# This key is the GPIO number and the value is the peripheral to control.
availableGPIO = {"6": LED(6), "13": LED(13), "19": LED(19), "26": LED(26)}

# Construct Losant device
device = Device("my-device-id", "my-app-access-key", "my-app-access-secret")

def on_command(device, command):
    print(command["name"] + " command received.")

    # Listen for the gpioControl. This name configured in Losant
    if command["name"] == "gpioControl":
        # The gpio that's passed in from the path parameter
        currentGpio = int(command["payload"]["gpio"])
        currentGpioText = str(currentGpio)

        # Get the LED at that physical GPIO number
        # from our availableGPIO
        led = availableGPIO.get(currentGpioText)

        # If found, toggle the LED
        # If not, display a message
        if led:
            print("Toggling LED " + str(currentGpioText))
            led.toggle()
        else:
            print("GPIO not configured " + str(currentGpioText))



# Listen for commands.
device.add_event_observer("command", on_command)

print("Listening for device commands")

# Connect to Losant and leave the connection open
device.connect(blocking=True)
