import statusled
from argus_controller import ArgusController
from temperatures import Thermistor
import board

"""
Based on the Argus Controller for Open Hardware:
https://github.com/openfancontrol/arguscontroller
"""

ArgusController(1, [Thermistor(board.A1)])
