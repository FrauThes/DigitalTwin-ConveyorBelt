"""
CB topology
"""

from mininet.topo import Topo

from utils import NETMASK
from utils import PLC_ADDR, PLC_MAC, HMI_ADDR, HMI_MAC, ATTACKER_ADDR, ATTACKER_MAC


class CBTopo(Topo):

    """Conveyor belt (CB): plc + hmi + attacker"""

    def build(self):

        switch = self.addSwitch('s1')

        plc = self.addHost(
            'plc',
            ip=PLC_ADDR + NETMASK,
            mac=PLC_MAC)
        self.addLink(plc, switch)

        hmi = self.addHost(
            'hmi',
            ip=HMI_ADDR + NETMASK,
            mac=HMI_MAC)
        self.addLink(hmi, switch)

        attacker = self.addHost(
            'attacker',
            ip=ATTACKER_ADDR + NETMASK,
            mac=ATTACKER_MAC)
        self.addLink(attacker, switch)