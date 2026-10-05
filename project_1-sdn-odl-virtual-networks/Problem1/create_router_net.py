from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    net = Mininet(
        controller=None,
        switch=OVSKernelSwitch,
        link=TCLink
    )
    h1 = net.addHost('h1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254', mac='00:00:00:00:01:01')
    h2 = net.addHost('h2', ip='10.0.2.1/24', defaultRoute='via 10.0.2.254', mac='00:00:00:00:02:01')
    s1 = net.addSwitch('s1', protocols="OpenFlow13")
    s2 = net.addSwitch('s2', protocols="OpenFlow13")
    r1 = net.addSwitch('r1', protocols="OpenFlow13") 

    net.addLink(h1, s1, port1=0, port2=1) 
    net.addLink(s1, r1, port1=2, port2=1) 
    net.addLink(r1, s2, port1=2, port2=1) 
    net.addLink(s2, h2, port1=2, port2=0) 

    net.build()
    net.start()
    h1.cmd('arp -s 10.0.1.254 00:00:00:00:01:FE')
    h2.cmd('arp -s 10.0.2.254 00:00:00:00:02:FE')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
