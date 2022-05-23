import usb_cdc
import time
import microcontroller
from temperatures import Thermistor
from crc8 import _crc8

Argus_Command_Undefined = b'\x00'
Argus_Command_ProbeDevice = b'\x01'
Argus_Command_GetTemp = b'\x20'
Argus_Command_GetFanRpm = b'\x30'
Argus_Command_GetFanPwm = b'\x31'
Argus_Command_SetFanPwm = b'\x32'
Argus_Command_EEReadByte = b'\x40'
Argus_Command_EEWriteByte = b'\x41'
Argus_Command_Error = b'\xFF'

class ArgusController:
  """handles serial communication with the Argus Monitor"""

  def __init__(self, device_id: int, thermistors: list):
    self.device_id = device_id
    self.sensor_count = len(thermistors) + 1 # first sensor will be internal temperature
    self.receive_state = 0
    self.recieve_buffer = bytearray()
    self.receive_command = Argus_Command_Undefined
    self.thermistors = thermistors
    self.receive()

  def receive(self):
    while(True):
      # read serial data from the Argus Monitor
      data = usb_cdc.data.read()

      if self.receive_state == 0:
        if (data == b'\xAA'):
          self.receive_state = 1
          self.recieve_buffer = bytearray()
          self.recieve_buffer.extend(data)

      elif self.receive_state == 1:
        if data == b'\x02' or data == b'\x03' or data == b'\x04' or data == b'\x05':
          self.receive_state = 2
          self.recieve_buffer.extend(data)
        else:
          self.receive_state = 0

      elif self.receive_state == 2:
        # Check if data is one of the Argus_Command_*
        self.receive_command = data
        self.recieve_buffer.extend(data)
        self.receive_state = 3
  
      elif self.receive_state == 3:
        crc8 = _crc8(self.recieve_buffer)
        self.recieve_buffer.extend(data)

        if crc8 == data:
          if self.receive_command == Argus_Command_ProbeDevice:
            self.answer_ProbeDevice()
          elif self.receive_command == Argus_Command_GetTemp:
            self.answer_GetTemp()
  
          self.receive_state = 0
          self.receive_command = Argus_Command_Undefined
      time.sleep(0.01)

  def send(self, message: bytearray):
    msg = bytearray()
    msg.extend(b'\xC5')
    msg.append(len(message) + 1)
    msg.extend(message)
    msg.extend(_crc8(msg))

    usb_cdc.data.write(msg)

  def answer_ProbeDevice(self):
    msg = bytearray()
    msg.extend(Argus_Command_ProbeDevice)
    msg.append(self.device_id)
    msg.append(self.sensor_count)
    msg.append(0)

    self.send(msg)

  def answer_GetTemp(self):
    thermistors = self.thermistors
    msg = bytearray()
    msg.extend(Argus_Command_GetTemp)
    msg.append(len(thermistors) + 1)

    # Send pico internal temp as first value
    internal_value = int(round(microcontroller.cpu.temperature, 1) * 10)
    msg.append(internal_value >> 8)
    msg.append(internal_value & 0xFF)
    
    for thermistor in thermistors:
      val = int(thermistor.temperature * 10)
      msg.append(val >> 8)
      msg.append(val & 0xFF)
      
    self.send(msg)
