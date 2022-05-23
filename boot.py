import usb_cdc
import storage
import analogio
import board

usb_cdc.enable(console=True, data=True)

# Enable USB drive if no temperature sensor is connected
pin = analogio.AnalogIn(board.A1)

if pin.value < 60000:
  storage.disable_usb_drive()
  print("USB drive disabled: To enable USB drive, disconnect sensors and reboot device")
else:
  print("USB drive enabled")

pin.deinit()
