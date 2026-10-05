from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from spf import A 

def topology():
    n = len(A)
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    switches = {}
    for i in range(1, n+1):
        switches[i] = net.addSwitch(f's{i}', protocols="OpenFlow13", dpid=str(i).zfill(16))

    h1 = net.addHost('h1', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254', mac='00:00:00:00:01:01')
    h2 = net.addHost('h2', ip='10.0.2.1/24', defaultRoute='via 10.0.2.254', mac='00:00:00:00:02:01')

    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if A[i-1][j-1] > 0 or A[j-1][i-1] > 0:
                net.addLink(switches[i], switches[j], port1=j, port2=i)
                
    net.addLink(h1, switches[1], port1=0, port2=n+1)
    net.addLink(h2, switches[n], port1=0, port2=n+1)

    net.build()
    c0.start()
    for i in range(1, n+1):
        switches[i].start([c0])
    h1.cmd('arp -s 10.0.1.254 00:00:00:00:01:fe')
    h2.cmd('arp -s 10.0.2.254 00:00:00:00:02:fe')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
