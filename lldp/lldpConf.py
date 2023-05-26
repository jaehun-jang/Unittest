# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
import pexpect
import sys
import time
import os

sys.path.append("./basic")
sys.path.append("./mef")
import basic.basicConf as bc
import mef.mefConf as mc
import lldp.lldpVef as llv

def enable(child):
    child.sendline("en")
    child.expect("#")

def confT(child):
    child.sendline("config terminal")
    child.expect("#")

def exit(child):
    child.sendline("exit")
    child.expect("#")
           
def end(child):
    child.sendline ('\n')
    child.expect("#")
    child.sendline("end")
    child.expect("#")

def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

###################################################################################

def disblldp(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('lldp disable') 
    child.expect("#")
    end(child)

def enblldp(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('lldp enable txrx') 
    child.expect("#")
    end(child)

def changLldpTlv(child,stateI,tlvI):
    state = ['','no']
    tlv = ['8021-org-spec','8023-org-spec','basic']
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline(state[stateI] + ' lldp tlv-select ' + tlv[tlvI] + ' all') 
    child.expect("#")
    end(child)

def changLldpTlvall(child,dut2):
    result = []
    sucCount = 0
    state = ['no','']
    org = ['8021-org-spec',
    '8023-org-spec',
    'basic'
    ]
    tlv =  [
    'port-protocol-vid',
    'port-vid',
    'protocol-identity',
    'vlan-name',
    'link-aggregation',
    'mac-phy-cfg',
    'max-frame-size',
    'power',
    'preemption-capability',
    'management-address',
    'port-description',
    'system-capabilities',
    'system-description ',
    'system-name'
    ] 
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    time.sleep(1)
    for stateI in state:
        for orgI in org:
            if orgI == '8021-org-spec':
                for tlvI in tlv[0:4]:
                    child.sendline(stateI+' lldp tlv-select '+orgI+' '+ tlvI) 
                    child.expect("#")
                    time.sleep(2)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1)
                    sucCount += 1
            elif orgI == '8023-org-spec':
                for tlvI in tlv[4:9]:
                    child.sendline(stateI+' lldp tlv-select '+orgI+' '+ tlvI) 
                    child.expect("#")
                    time.sleep(2)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1)
                    sucCount += 1
            elif orgI == 'basic':
                for tlvI in tlv[9::]:
                    child.sendline(stateI+' lldp tlv-select '+orgI+' '+ tlvI) 
                    child.expect("#")
                    time.sleep(2)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1)
                    sucCount += 1 
    print(result)   
    end(child)
    if result.count('Ok')  == 28:
        return ['Ok']
    else:
        return ['Nok']

def setMgmtTlv(child):
    confT(child)
    child.sendline('lldp tlv-set management-address-tlv mac-address')
    child.expect("#")
    end(child)

def setLldpTimer(child):
    confT(child)
    child.sendline('lldp holdtime-multiplier 4')
    child.expect("#")
    child.sendline('lldp tx-interval 10') 
    child.expect("#")
    end(child)

def chgMgmtTlv(child):
    confT(child)
    child.sendline('system management-address vlan 1 v6')
    child.expect("#")
    end(child)
    
###################################################################################

### Static Link Aggregation ###	  
def confEthService(child):
    svc = 2
    uni = 1
    mc.crtServi(child,svc,uni)
    time.sleep(1)

### Pure Static Link Aggregation ###	  
def removeEthService(child):
    svc = 2
    uni = 1  
    mc.dltServi(child,svc,uni)
    time.sleep(1)

def confBasicLldp(child,dut2): 
    result = []
    confEthService(child)
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvC(dut2,'default'))
    time.sleep(1)               
    disblldp(child)
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvC(dut2,'disable'))
    time.sleep(1)
    enblldp(child)
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvC(dut2,'enable'))
    time.sleep(5)
    result.extend(changLldpTlvall(child,dut2))
    time.sleep(5)
    setMgmtTlv(child)
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvD(dut2,'mgmt-subtype'))
    time.sleep(1)
    setLldpTimer(child)
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvD(dut2,'lldp-timer'))
    time.sleep(1)
    chgMgmtTlv(child) 
    time.sleep(5)
    result.append(llv.checkLldpNeighborTlvD(dut2,'sys-mgmt'))
    time.sleep(1)
    print(result)
    removeEthService(child) 
    os.remove('/home/jhjang/auto/utest_suite/log/checkLldpNeighborTlvD.txt') 
    return result.count('Ok')

