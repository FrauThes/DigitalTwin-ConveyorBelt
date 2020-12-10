"""
``conveyorbelt`` provides an additional device for MiniCPS

"""

from minicps.devices import Device
import time


class ConveyorBelt(Device):
    """ConveyorBelt class.

    ConveyorBelt provides:
        - state APIs: e.g., set the temperature of the motor
    """

    def __init__(self, name, protocol, state, temperature):
        """
        :param str name: device name
        :param dict protocol: used to set up the network layer API
        :param dict state: used to set up the physical layer API
        :param float temperature: current temperature in Celsius
        """

        self.temperature = temperature
        super(ConveyorBelt, self).__init__(name, protocol, state)

    def _start(self):
        self.pre_loop()
        self.main_loop()

    def pre_loop(self, sleep=0.5):
        """ConveyorBelt pre_loop.

        :param float sleep: second[s] to sleep before returning
        """

        print "TODO ConveyorBelt pre_loop: please override me"

    def main_loop(self, sleep=0.5):
        """ConveyorBelt main loop.

        :param float sleep: second[s] to sleep after each iteration
        """

        sec = 0
        while sec < 1:
            print "TODO ConveyorBelt main_loop: please override me"
            time.sleep(sleep)

            sec += 1
