"""
CB hmi.py
"""

from minicps.devices import HMI
from utils import STATE, PLC_ADDR
from utils import HMI_PROTOCOL, HMI_DATA, HMI_ADDR

import time
import logging

# interlocks to plc
MOTOR = ('MOTOR', 1)  # to be received from PLC
SENSOR_TEMP = ('SENSOR-TEMPERATURE', 1)  # to be received from PLC
MOTOR_HMI = ('MOTOR-HMI', 1)  # to be sent to PLC


class CBHMI(HMI):

    def main_loop(self, sleep=20):
        """hmi main loop:
            - read data of CB motor from PLC (temperature, velocity)
            - alter velocity
        """
        print 'DEBUG: CB HMI enters main_loop.'
        print
        # close to BSD-syslog format (RFC 3164)
        # e.g. <133> Feb 25 14:09:07 webserver syslogd: restart PRI <Facility*8+Severity>, HEADER (timestamp host), MSG
        logging.basicConfig(filename='logs/hmi.log',
                            format='%(levelname)s %(asctime)s ' + HMI_ADDR + ' %(funcName)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)

        while True:
            velocity = float(self.receive(MOTOR, PLC_ADDR))
            temperature = float(self.receive(SENSOR_TEMP, PLC_ADDR))
            try:
                user_input = int(raw_input(
                    "\n Please choose from the following options: \n Read temperature: Press 1 \n Read velocity: Press 2 \n Change velocity or stop motor: Press 3 \n Shutdown HMI program: Press 99 \n"))
                print 'DEBUG: input = ', user_input

                if user_input == 1:  # read temperature
                    logging.info('Read temperature: %f.' % temperature)
                    print "DEBUG pressed 1 (read temperature)"
                    print "Current temperature of motor: ", temperature, " degree celsius"

                elif user_input == 2:  # read velocity
                    logging.info('Read velocity: %f.' % velocity)
                    print "DEBUG pressed 2 (read velocity)"
                    print "Current velocity of motor: ", velocity, " m/s"

                elif user_input == 3:  # change velocity or stop motor
                    print "DEBUG pressed 3 (change velocity or stop motor) \n Current velocity of motor: ", velocity, " m/s"
                    change = raw_input("Do you wish to change the motor's velocity or stop the motor? Y/N \n")
                    print "DEBUG typed ", change

                    if change == "Y" or change == "y":
                        new_velocity = float(raw_input("Please enter the desired velocity of the motor (0 for stop): "))
                        print "DEBUG typed ", new_velocity
                    try:
                        logging.info('Sent new velocity to PLC (%s): %f.' % (PLC_ADDR, new_velocity))
                        self.send(MOTOR_HMI, new_velocity, PLC_ADDR)
                        print 'Changed velocity from %f to %f' % (velocity, new_velocity)
                    except (RuntimeError, TypeError, NameError):
                        logging.warning('New velocity (%f) could not be sent to PLC (%s).' % (new_velocity, PLC_ADDR))

                elif change == "N" or change == "n":
                    print "Current velocity of motor remains: ", velocity, " m/s"
                    continue

                elif user_input == 99:
                    logging.info('Shutdown HMI program.')
                    print "DEBUG pressed 3 (shutdown HMI program)"
                    print 'DEBUG: HMI Shutdown'
                    break
            except ValueError:
                print("Oops! That was no valid number. Please try again...")

        time.sleep(sleep)


if __name__ == "__main__":
    hmi = CBHMI(
        name='hmi',
        state=STATE,
        protocol=HMI_PROTOCOL,
        memory=HMI_DATA,
        disk=HMI_DATA)
