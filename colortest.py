import time
from rpi_ws281x import *
import argparse

class ColorWorker:
    def __init__(self):
        LED_COUNT      = 100      # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        
        
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def setColor(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
# LED strip configuration:



def setColor(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    colorWorker = ColorWorker()
    strip = colorWorker.strip

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            red = input("Enter red value (0-255): ")
            green = input("Enter green value (0-255): ")
            blue = input("Enter blue value (0-255): ")
            red = int(red)
            green = int(green)
            blue = int(blue)
            if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
                print("Invalid input. Please enter values between 0 and 255.")
                continue
            setColor(strip, Color(red, green, blue))

    except KeyboardInterrupt:
        if args.clear:
            setColor(strip, Color(0,0,0), 10)