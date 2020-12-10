"""
CB plc.py
"""

from minicps.devices import PLC
from utils import PLC_DATA, STATE, PLC_PROTOCOL, PLC_ADDR, HMI_ADDR
from utils import MOTOR_VEL_THRES, MOTOR_VEL_INIT_ON, MOTOR_VEL_INIT_OFF
from utils import MOTOR_TEMP_THRES

import time
import logging

# tag addresses
SENSOR_TEMP = ('SENSOR-TEMPERATURE', 1)
MOTOR = ('MOTOR', 1)
MOTOR_HMI = ('MOTOR-HMI', 1)


class CBPLC(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: CB PLC enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc main loop.
             - reads value from sensor
             - drives actuator according to the control strategy
             - updates its enip server
             - logs the control strategy events (info, exceptions)
        """

        print 'DEBUG: CB PLC enters main_loop'
        print
        # close to BSD-syslog format (RFC 3164)
        # e.g. <133> Feb 25 14:09:07 webserver syslogd: restart PRI <Facility*8+Severity>, HEADER (timestamp host), MSG
        logging.basicConfig(filename='logs/plc.log',
                            format='%(levelname)s %(asctime)s ' + PLC_ADDR + ' %(funcName)s %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)

        while True:
            current_velocity = float(self.get(MOTOR))
            new_velocity = float(self.receive(MOTOR_HMI, PLC_ADDR))  # check if HMI send new vel to PLC
            if current_velocity != new_velocity:  # if HMI wants to change velocity (HMI enip tag)
                print 'DEBUG HMI wants to change velocity to ', new_velocity
                logging.info(
                    'Received new velocity from HMI (%s) in own (%s) internal enip tag.' % (HMI_ADDR, PLC_ADDR))
                current_velocity = new_velocity

            current_temperature = float(self.get(SENSOR_TEMP))
            self.send(SENSOR_TEMP, current_temperature, PLC_ADDR)

            if current_temperature <= float(MOTOR_TEMP_THRES['MAX']):
                if current_velocity <= float(MOTOR_VEL_THRES['MIN']) and current_velocity != 0.0:
                    print 'DEBUG PLC - velocity of belt (MOTOR) under threshold: %f <= %f --> turn on motor: %f' % (
                        current_velocity, MOTOR_VEL_THRES['MIN'], MOTOR_VEL_INIT_ON)
                    logging.info('Velocity of belt (MOTOR) under threshold: %f <= %f --> turn on motor: %f' % (
                    current_velocity, MOTOR_VEL_THRES['MIN'], MOTOR_VEL_INIT_ON))
                    self.set(MOTOR, MOTOR_VEL_INIT_ON)
                    self.send(MOTOR, MOTOR_VEL_INIT_ON, PLC_ADDR)

                elif current_velocity > MOTOR_VEL_THRES['MAX']:  # stop if velocity greater than max. velocity
                    print 'DEBUG PLC - velocity of belt (MOTOR) greater than threshold: %f > %f --> turn off motor' % (
                        current_velocity, MOTOR_VEL_THRES['MAX'])
                    logging.info('Velocity of belt (MOTOR) greater than threshold: %f > %f --> turn off motor' % (
                    current_velocity, MOTOR_VEL_THRES['MAX']))
                    self.set(MOTOR, MOTOR_VEL_INIT_OFF)
                    self.send(MOTOR, current_velocity, PLC_ADDR)

                else:
                    logging.info('Set motor to velocity: %f.' % current_velocity)
                    self.set(MOTOR, current_velocity)
                    self.send(MOTOR, current_velocity, PLC_ADDR)
            else:
                print 'DEBUG PLC - temperature of belt motor greater than threshold: %f > %f --> turn off motor' % (
                    current_temperature, MOTOR_TEMP_THRES['MAX'])
                logging.info('Temperature of belt motor greater than threshold: %f > %f --> turn off motor' % (
                current_temperature, MOTOR_TEMP_THRES['MAX']))
                self.set(MOTOR, MOTOR_VEL_INIT_OFF)
                self.send(MOTOR, current_velocity, PLC_ADDR)


if __name__ == "__main__":
    plc = CBPLC(
        name='plc',
        state=STATE,
        protocol=PLC_PROTOCOL,
        memory=PLC_DATA,
        disk=PLC_DATA)
