"""
CB utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores values as strings.
sqlite uses float keyword and cpppo use REAL keyword.

"""
from minicps.utils import build_debug_logger

cb_logger = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

# thresholds velocity
MOTOR_VEL_THRES = {
    'MIN': 1.0,
    'MAX': 50.0
}
MOTOR_VEL_INIT_OFF = 0.0
MOTOR_VEL_INIT_ON = 1.0
# thresholds temperature
MOTOR_TEMP_INIT = 15.0
MOTOR_TEMP_THRES = {
    'MIN': 8.0,
    'MAX': 100.0
}

NETMASK = '/24'

# PLC
PLC_MAC = '00:00:00:00:00:01'
PLC_ADDR = '10.0.0.1'
PLC_DATA = {
    'SENSOR-TEMPERATURE': '0.0',  # temperature of CB motor
    'MOTOR': '0.0',   # 0 means OFF and >0 means ON (velocity of CB motor)
    'MOTOR-HMI': '0.0'
}
PLC_TAGS = (
    ('SENSOR-TEMPERATURE', 1, 'REAL'),
    ('MOTOR', 1, 'REAL'),
    ('MOTOR-HMI', 1, 'REAL')
)
PLC_SERVER = {
    'address': PLC_ADDR,
    'tags': PLC_TAGS
}
PLC_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': PLC_SERVER
}

# HMI
HMI_MAC = '00:00:00:00:00:02'
HMI_ADDR = '10.0.0.2'
HMI_DATA = {
    'MOTOR': '0.0',
    'MOTOR-HMI': '0.0'
}
HMI_TAGS = (
    ('MOTOR', 1, 'REAL'),
    ('MOTOR-HMI', 1, 'REAL')
)
HMI_SERVER = {
    'address': HMI_ADDR,
    'tags': HMI_TAGS
}
HMI_PROTOCOL = {
    'name': 'enip',
    'mode': 0,    # client only
    'server': HMI_SERVER
}

ATTACKER_MAC = '00:00:00:00:00:03'
ATTACKER_ADDR = '10.0.0.3'


# physical state
PATH = 'cb_db.sqlite'
NAME = 'cb_table'

STATE = {
    'name': NAME,
    'path': PATH
}


# pid is device id (e.g. plc number)
SCHEMA = """
CREATE TABLE cb_table (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO cb_table VALUES ('SENSOR-TEMPERATURE',   1, '15.0');
    INSERT INTO cb_table VALUES ('MOTOR',    1, '0.0');
    INSERT INTO cb_table VALUES ('MOTOR-HMI',    1, '0.0');
"""