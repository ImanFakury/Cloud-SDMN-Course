from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def topology():
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    h1 = net.addHost('h1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254', mac='00:00:00:00:01:01')
    h2 = net.addHost('h2', ip='10.0.2.1/24', defaultRoute='via 10.0.2.254', mac='00:00:00:00:02:01')
    s1 = net.addSwitch('s1', protocols="OpenFlow13", dpid="0000000000000001") # openflow:1
    s2 = net.addSwitch('s2', protocols="OpenFlow13", dpid="0000000000000002") # openflow:2
    r1 = net.addSwitch('r1', protocols="OpenFlow13", dpid="0000000000000003") # openflow:3

    net.addLink(h1, s1, port1=0, port2=1)
    net.addLink(s1, r1, port1=2, port2=1)
    net.addLink(r1, s2, port1=2, port2=1)
    net.addLink(s2, h2, port1=2, port2=0)

    net.build()
    c0.start()
    s1.start([c0]); s2.start([c0]); r1.start([c0])

    h1.cmd('arp -s 10.0.1.254 00:00:00:00:01:fe')
    h2.cmd('arp -s 10.0.2.254 00:00:00:00:02:fe')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
