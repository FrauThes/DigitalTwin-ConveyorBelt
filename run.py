"""
CB run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS
from topo import CBTopo

import sys


class CBCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc, s1, hmi = self.net.get('plc', 's1', 'hmi')

        # s1.cmd(sys.executable + ' physical_process.py &')
        # plc.cmd(sys.executable + ' plc.py &')
        # hmi.cmd(sys.executable + ' hmi.py &')

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = CBTopo()
    net = Mininet(topo=topo)

    cbcps = CBCPS(
        name='CBCPS',
        net=net)