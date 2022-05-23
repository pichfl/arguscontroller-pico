import analogio
import math

ZERO_K = 273.15

class Thermistor:
  def __init__(self, pin, beta: int = 3950, resistance_o: int = 10, resistance_series: int = 10, nominal_temp: int = 25):
    self.pin = analogio.AnalogIn(pin)
    self.beta = beta
    self.resistance_o = resistance_o
    self.resistance_series = resistance_series
    self.nominal_temp_k = nominal_temp + ZERO_K

  @property
  def reference_voltage(self) -> float:
    return self.pin.reference_voltage
  
  @property
  def pin_voltage(self) -> float:
    return (self.pin.value * self.reference_voltage) / 65536
  
  @property
  def resistance(self) -> float:
    return self.pin_voltage * self.resistance_series / (self.reference_voltage - self.pin_voltage)

  @property
  def temperature(self) -> float:
    temp_k = 1 / ((1 / self.nominal_temp_k) + (math.log(self.resistance / self.resistance_o)) / self.beta)
    return round(temp_k - ZERO_K, 1)

  def __del__(self):
    self.pin.deinit()

