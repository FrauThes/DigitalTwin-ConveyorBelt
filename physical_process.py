"""
CB physical process

if motor is turned ON, motor temperature is increasing or decreasing dependent on desired velocity
if motor is turned OFF, motor temperature is decreasing

"""

from conveyorbelt import ConveyorBelt

from utils import STATE, MOTOR_TEMP_INIT
import time

# TAGS
MOTOR = ('MOTOR', 1)
SENSOR_TEMP = ('SENSOR-TEMPERATURE', 1)


class ConveyorBelt(ConveyorBelt):

    def pre_loop(self):
        self.set(MOTOR, 0.0)  # motor is OFF
        self.temperature = self.set(SENSOR_TEMP, MOTOR_TEMP_INIT)  # init temperature of belt when motor is OFF

    def main_loop(self):
        while True:
            motor = float(self.get(MOTOR))
            temperature = float(self.get(SENSOR_TEMP))
            print "INFO phys-proc: motor velocity: %f  motor temperature: %f" % (motor, temperature)

            if motor == 0.0:  # if motor is OFF, temperature is decreasing until init/room temp
                print "DEBUG phys-proc: motor is OFF"
                while temperature > MOTOR_TEMP_INIT and motor == float(self.get(MOTOR)):  # while motor vel not altered
                    time.sleep(0.1)
                    new_temperature = temperature - 0.1
                    if new_temperature < MOTOR_TEMP_INIT:
                        self.set(SENSOR_TEMP, MOTOR_TEMP_INIT)
                        temperature = MOTOR_TEMP_INIT
                    else:
                        self.set(SENSOR_TEMP, new_temperature)
                        temperature = new_temperature
                    print "INFO phys-proc: motor is turned off -- temperature decreasing: ", new_temperature

            elif motor > 0.0:  # if motor is ON, temperature is either increasing or decreasing dep. on vel
                print "DEBUG phys-proc: motor is ON"
                final_temperature = MOTOR_TEMP_INIT + (0.5 * motor)
                while motor == float(self.get(MOTOR)):
                    print "DEBUG phys-proc: motor is ON -- velocity remains"
                    time.sleep(0.1)
                    if float(self.get(SENSOR_TEMP)) <= final_temperature:
                        increasing_temperature = float(self.get(SENSOR_TEMP)) + 0.1
                        self.set(SENSOR_TEMP, increasing_temperature)
                        print "INFO phys-proc: motor is turned on -- temperature increasing: ", increasing_temperature
                    else:
                        decreasing_temperature = float(self.get(SENSOR_TEMP)) - 0.1
                        self.set(SENSOR_TEMP, decreasing_temperature)
                        print "INFO phys-proc: motor is turned on -- temperature decreasing: ", decreasing_temperature

            time.sleep(0.25)


if __name__ == '__main__':
    cb = ConveyorBelt(
        name='cb',
        state=STATE,
        protocol=None,
        temperature=MOTOR_TEMP_INIT
    )
