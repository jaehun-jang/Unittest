# funBaVef.py

# $language = "python"
# $interface = "1.0"

import pexpect
import sys
import time
import os

sys.path.append("./basic")
import basic.basicConf as bc


### Check LLDP Neighbor ###

def checkEoamNeighborDisc(host,state):              
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkEoamNeighborDisc.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh ethernet oam discovery interface 1/25')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkEoamNeighborDisc.txt', 'rt') as fr:
        if 'passive' in state:
            readResult = fr.readlines()[31]
            spResult = str(readResult).split()
            print(spResult)
            if spResult[1] == 'passive': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'active' in state:
            readResult = fr.readlines()[31]
            spResult = str(readResult).split()
            print(spResult)
            if spResult[1] == 'active': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'startLBTest' in state:
            readResult = fr.readlines()[16]
            spResult = str(readResult).split()
            print(spResult)
            if spResult[2] == 'local': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'stopLBTest' in state:
            readResult = fr.readlines()[16]
            spResult = str(readResult).split()
            print(spResult)
            if spResult[2] == 'no': 
                return 'Ok'
            else:
                return 'Nok'
        else:
            return 'Nok'  
def checkEoamStatus(host,state):               
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkEoamStatus.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh ethernet oam status interface 1/25 ')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkEoamStatus.txt', 'rt') as fr:      
        if 'dying-gasp' in state:
#            print (len(a))
            readResult = fr.readlines()[50]
            spResult = str(readResult).split()
            print (spResult)  
            if spResult[1] == 'disable': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'link-fault' in state:
            readResult = fr.readlines()[49]
            spResult = str(readResult).split()
            print (spResult) 
            if spResult[1] == 'disable': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'link-monitor' in state:
            readResult = fr.readlines()[21]
            spResult = str(readResult).split()
            print (spResult) 
            if spResult[1] == 'supported(on)': 
                return 'Ok' 
            else:
                return 'Nok' 
        else:
            return 'Nok'   


def RLBTestResult(host): 
    readcount = 0                
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/RLBTestResult.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh ethernet oam remote-loopback test result ')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/RLBTestResult.txt', 'rt') as fr:      
            readResult = fr.readlines()[9]
            spResult = str(readResult).split()
            print (spResult)  
            if spResult[6] == '15': 
                return 'Ok'
            else:
                return 'Nok'





