import digitalio
import board
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led.value = True
time.sleep(1)

# while True:
#     led.value = True
    # time.sleep(0.5)
    # led.value = False
    # time.sleep(0.5)
