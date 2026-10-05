from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def tree_topology():
    net = Mininet(
        controller=RemoteController,
        switch=OVSKernelSwitch,
        link=TCLink,
        autoSetMacs=True  
    )

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    s1 = net.addSwitch('s1', protocols="OpenFlow13") 
    
    s2 = net.addSwitch('s2', protocols="OpenFlow13") 
    s3 = net.addSwitch('s3', protocols="OpenFlow13")
    
    s4 = net.addSwitch('s4', protocols="OpenFlow13") 
    s5 = net.addSwitch('s5', protocols="OpenFlow13")
    s6 = net.addSwitch('s6', protocols="OpenFlow13")
    s7 = net.addSwitch('s7', protocols="OpenFlow13")

    h1, h2 = net.addHost('h1'), net.addHost('h2')
    h3, h4 = net.addHost('h3'), net.addHost('h4')
    h5, h6 = net.addHost('h5'), net.addHost('h6')
    h7, h8 = net.addHost('h7'), net.addHost('h8')

    net.addLink(s1, s2) 
    net.addLink(s1, s3)
    
    net.addLink(s2, s4) 
    net.addLink(s2, s5)
    net.addLink(s3, s6)
    net.addLink(s3, s7)
    
    net.addLink(h1, s4); net.addLink(h2, s4) 
    net.addLink(h3, s5); net.addLink(h4, s5)
    net.addLink(h5, s6); net.addLink(h6, s6)
    net.addLink(h7, s7); net.addLink(h8, s7)

    net.build()
    c0.start()
    for switch in [s1, s2, s3, s4, s5, s6, s7]:
        switch.start([c0])

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    tree_topology()
