from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

A = [
    [0, 2, 3, 4],
    [2, 0, 0, 1],
    [3, 0, 0, 0],
    [1, 1, 0, 0]
]

def topology():
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
    c1 = net.addController('c1', ip='127.0.0.1', port=6633)

    n = len(A)
    switches = []
   
    for i in range(n):
        dpid = "%016x" % (i+1)
        switches.append(net.addSwitch('s%d' % (i+1), protocols='OpenFlow13', dpid=dpid))

    h1 = net.addHost('h1', ip='10.0.1.10/24', mac='00:00:00:00:00:01', defaultRoute='via 10.0.1.1')
    hn = net.addHost('h%d' % n, ip='10.0.2.10/24', mac='00:00:00:00:00:02', defaultRoute='via 10.0.2.1')

    net.addLink(h1, switches[0])
    net.addLink(hn, switches[-1])

    for i in range(n):
        for j in range(i+1, n):
            if A[i][j] > 0 or A[j][i] > 0:
                net.addLink(switches[i], switches[j])

    net.build()
    net.start()
   
    time.sleep(2)
   
    h1.cmd('arp -s 10.0.1.1 00:00:00:00:00:02')
    hn.cmd('arp -s 10.0.2.1 00:00:00:00:00:01')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
