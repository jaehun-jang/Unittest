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

def checkLldpNeighborTlvC(host,state): 
    readcount = 0                
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvC.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh lldp neighbor')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvC.txt', 'rt') as fr:
        passCnt = 0
        readResult = fr.readlines()
        readcount = len(readResult)
#        print(readResult)
        print ('PRINT: ' + str(readcount))      
        os.remove('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvC.txt')
        if 'default' in state:
            if readcount == 55: 
                return 'Ok' 
            else:
                return 'Nok'
        if 'enable' in state:
            if readcount == 55: 
                return 'Ok' 
            else:
                return 'Nok'
        elif 'disable' in state:
            if readcount == 4: 
                return 'Ok' 
            else:
                return 'Nok'       
        else:
            return 'Nok'   

def checkLldpNeighborTlvCF(host,count): 
    countList = [ 54,53,52,48,45,42,40,32,28,23,23,19,19,19,20,21,22,26,29,32,34,42,46,51,51,55,55,55]
    readcount = 0                
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvCF.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh lldp neighbor')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvCF.txt', 'rt') as fr:
        passCnt = 0
        readResult = fr.readlines()
        readcount = len(readResult)
        print ('PRINT CC: ' + str(countList[count]))      
        os.remove('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvCF.txt')
        if readcount == countList[count]: 
            return 'Ok' 
        else:
            return 'Nok'
 
def checkLldpNeighborTlvD(host,state):                 
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvD.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh lldp neighbor')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvD.txt', 'rt') as fr:
        if 'mgmt-subtype' in state:
            readResult = fr.readlines()[21]
            spResult = str(readResult).split()
            if spResult[5] == '802': 
                return 'Ok'
            else:
                return 'Nok'
        elif 'lldp-timer'in state:
            readResult = fr.readlines()[9]
            spResult = str(readResult).split()
            if spResult[4] == '40': 
                    return 'Ok'
            else:
                return 'Nok'
        elif 'sys-mgmt'in state:
            readResult = fr.readlines()[23]
            spResult = str(readResult).split()
            if spResult[3] == '25001': 
                return 'Ok'
            else:
                return 'Nok'


