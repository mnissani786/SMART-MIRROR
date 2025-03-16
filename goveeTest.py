# References: 
# https://govee.readme.io/reference/controllightdevice
# https://developer.govee.com/reference/control-you-devices#on_off
# https://govee-public.s3.amazonaws.com/developer-docs/GoveeDeveloperAPIReference.pdf

import requests
import uuid

#Formula to convert to acceptable color values (From Govee API documentation)
def colorConversion(red, green, blue):
    value = ((red & 0xFF) << 16) | ((green & 0xFF) << 8) | ((blue & 0xFF) << 0)
    print('Color value ' + str(value)) #debugging
    return value 

#This returns the header values for sending the HTTP message
#Possible Feature: The user could input their API key in the settings option of the app
def returnHeaders():
    headers = {
        "Content-Type": "application/json",
        "Govee-API-Key": "2013b345-7f27-43c9-bc48-dfe042868126"
    }
    return headers

#This returns the request body parameters
#Possible feature: the user can select which device and the "sku" and "device" variables would change
def returnData(type, instance, value):    
    data = {
        "requestId": str(uuid.uuid4()), #Generates a random uuid
        "payload": {
            "sku": "H6052",
            "device": "26:5F:13:E8:CB:BF:68:3A",
            "capability": {
                "type": type,
                "instance": instance,
                "value": value
            }
        }
    }
    return data

#This sends the complete HTTP message to control the light
def changeLight(type, instance, value):
    url = "https://openapi.api.govee.com/router/api/v1/device/control"
    data = returnData(type, instance, value)    
    headers = returnHeaders()
    response = requests.post(url, json=data, headers=headers) #Sends the request
    print(response.text) #Debugging


# def main():
    ### Turns light on and off
    ### 0 = off, 1 = on
    # changeLight("devices.capabilities.on_off", "powerSwitch", 0)    #Off
    # changeLight("devices.capabilities.on_off", "powerSwitch", 1)    #On

    ### changes the color of the light
    ### set r, g, b values 0-255 in colorConversion(r, g, b)
    # changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 0, 0)))    #Red
    # changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 255, 0)))    #Green
    # changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 0, 255)))    #Blue

    ### Changes the white temperature of the light
    ### My lamp uses temps between 2000k - 9000k, different models vary with their color temperature
    # changeLight("devices.capabilities.color_setting", "colorTemperatureK", 2000)    #2000k - Warm white
    # changeLight("devices.capabilities.color_setting", "colorTemperatureK", 5500)    #5500k - Pure white
    # changeLight("devices.capabilities.color_setting", "colorTemperatureK", 9000)    #9000K - Cool white

    ### Changes the brightness
    ### percentage ranges from 0-100% brightness
    # changeLight("devices.capabilities.range", "brightness", 10)    #10% brightness
    # changeLight("devices.capabilities.range", "brightness", 50)    #50% brightness
    # changeLight("devices.capabilities.range", "brightness", 100)   #100% brightness

#if __name__ == "__main__":
    #main()

