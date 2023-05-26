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
sys.path.append("./eoam")
import basic.basicConf as bc
import mef.mefConf as mc
import eoam.eoamVef as eov

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

def disbEoam(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('ethernet oam disable') 
    child.expect("#")
    end(child)

def enbEoamAct(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('ethernet oam enable') 
    child.expect("#")
    child.sendline('ethernet oam mode active') 
    child.expect("#")    
    end(child)

def enbEoamPsv(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('ethernet oam enable') 
    child.expect("#")
    child.sendline('ethernet oam mode passive') 
    child.expect("#") 
    end(child)

def confDyingGasp(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('no ethernet oam link-event dying-gasp enable')
    child.expect("#")
    child.sendline('\n')
    child.expect("#")   
    end(child)

def confLinkFault(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('no ethernet oam link-event link-fault enable')
    child.expect("#")
    child.sendline('\n')
    child.expect("#")  
    end(child)

def confMonitor(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('ethernet oam link-monitor on ')
    child.expect("#")
    child.sendline('ethernet oam link-monitor supported')
    child.expect("#")
    end(child)

def confRemoteLB(child):
    confT(child)
    child.sendline('interface 1/25')
    child.expect("#")
    child.sendline('ethernet oam remote-loopback supported')
    child.expect("#")
    child.sendline('ethernet oam remote-loopback timeout 5 ') 
    child.expect("#")
    end(child)

def startRemoteLB(child):
    child.sendline('ethernet oam remote-loopback test packet-count 15')
    child.expect("#")
    child.sendline('ethernet oam remote-loopback test packet-size 1500 ')
    child.expect("#")
    child.sendline('ethernet oam remote-loopback start interface 1/25  ') 
    child.expect("#")
    child.sendline('ethernet oam remote-loopback test start   ') 
    child.expect("#")

def stopRemoteLB(child):
    child.sendline('ethernet oam remote-loopback stop interface 1/25 ') 
    child.expect("#")

###################################################################################

def confEoam(child):
    svc = 1
    uni = 1
    mc.crtServi(child,svc,uni)
    time.sleep(1)
    enbEoamAct(child)
    time.sleep(1)

def removeEoam(child):
    svc = 1
    uni = 1
    mc.dltServi(child,svc,uni)
    time.sleep(1)
    disbEoam(child)
    time.sleep(1)

def confBasicEoam(child,dut1,dut2): 
    result = []
    confEoam(child)
    time.sleep(2) 
    enbEoamPsv(child)
    time.sleep(2) 
    result.append(eov.checkEoamNeighborDisc(dut2,'passive'))
    time.sleep(2)
    enbEoamAct(child)
    time.sleep(2)                  
    result.append(eov.checkEoamNeighborDisc(dut2,'active'))
    time.sleep(2)
    confDyingGasp(child)
#    input("Enter!") 
    time.sleep(2)                   
    result.append(eov.checkEoamStatus(dut1,'dying-gasp'))
    time.sleep(2)
    confLinkFault(child)
#    input("Enter!") 
    time.sleep(2)                    
    result.append(eov.checkEoamStatus(dut1,'link-fault'))
    time.sleep(2)
    confMonitor(child)
#    input("Enter!") 
    time.sleep(2)               
    result.append(eov.checkEoamStatus(dut1,'link-monitor'))
    time.sleep(2) 
    startRemoteLB(child)
    time.sleep(2)
    result.append(eov.checkEoamNeighborDisc(dut2,'startLBTest'))  
    time.sleep(15) 
    stopRemoteLB(child)
    time.sleep(2)
    result.append(eov.checkEoamNeighborDisc(dut2,'stopLBTest'))  
    result.append(eov.RLBTestResult(dut1))  
    time.sleep(2)    
    print(result)
    removeEoam(child)
    time.sleep(5)
    os.remove('/home/jhjang/auto/utest_suite/log/checkEoamNeighborDisc.txt') 
    os.remove('/home/jhjang/auto/utest_suite/log/checkEoamStatus.txt') 
    os.remove('/home/jhjang/auto/utest_suite/log/RLBTestResult.txt') 
    return result.count('Ok')
