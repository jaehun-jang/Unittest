# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
import pexpect
import sys
import time
import os

sys.path.append("./mef")
sys.path.append("./lag")
import mef.mefConf as mc
import lag.lagVef as lav

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

def staticLag(child):
    confT(child)
    child.sendline('interface 1/23')
    child.expect("#")
    child.sendline('channel-group 1 mode on working')
    child.expect("#")
    child.sendline('interface 1/24')
    child.expect("#")
    child.sendline('channel-group 1 mode on protection')
    child.expect("#")
    end(child)

def activeLacp(child):
    confT(child)
    child.sendline('interface 1/23')
    child.expect("#")
    child.sendline('channel-group 1 mode active')
    child.expect("#")
    child.sendline('lacp timeout short')
    child.expect("#")
    child.sendline('interface 1/24')
    child.expect("#")
    child.sendline('channel-group 1 mode active')
    child.expect("#")
    child.sendline('lacp timeout short')
    child.expect("#")
    end(child)

def passiveLacp(child):
    confT(child)
    child.sendline('interface 1/23')
    child.expect("#")
    child.sendline('channel-group 1 mode passive')
    child.expect("#")
    child.sendline('lacp timeout short')
    child.expect("#")
    child.sendline('interface 1/24')
    child.expect("#")
    child.sendline('channel-group 1 mode passive')
    child.expect("#")
    child.sendline('lacp timeout short')
    child.expect("#")
    end(child)

def changeMaxMember(child,maxmember):
    confT(child)
    child.sendline('port-channel 1 max-member ' + str(maxmember))
    child.expect("#")
    end(child)

def delNniInt(child):    
    confT(child)
    child.sendline('ethernet nni nni1')
    child.expect("#")
    child.sendline('no map interface')
    child.expect("#")  
    end(child)

def addNniInt(child):    
    confT(child)
    child.sendline('ethernet nni nni1')
    child.expect("#")
    child.sendline('map interface po1')
    child.expect("#")    
    end(child)

def delPortCh(child):    
    confT(child)
    child.sendline('interface range 1/23-1/24')
    child.expect("#")
    child.sendline('no channel-group')
    child.expect("#")
    end(child)

def deflacpTime(child):    
    confT(child)
    child.sendline('interface range 1/23-1/24')
    child.expect("#")
    child.sendline('lacp timeout long')
    child.expect("#")
    end(child)

###################################################################################

### Static Link Aggregation ###	  
def confLag(child):
    svc = 1
    uni = 1
    mc.crtServi(child,svc,uni)
    time.sleep(1)
    delNniInt(child)
    time.sleep(1)
    staticLag(child)
    time.sleep(1)
    addNniInt(child)
    time.sleep(1)

### Static Link Aggregation ###	  
def confLacp(child):
    svc = 1
    uni = 1
    mc.crtServi(child,svc,uni)
    time.sleep(1)
    delNniInt(child)
    time.sleep(1)
    activeLacp(child)
    time.sleep(1)
    addNniInt(child)
    time.sleep(1)


### Pure Static Link Aggregation ###	  
def removeLag(child):
    svc = 1
    uni = 1
    delNniInt(child)
    time.sleep(1)
    delPortCh(child)
    time.sleep(1)   
    mc.dltServi(child,svc,uni)
    time.sleep(1)


### Pure Static Link Aggregation ###	  
def removeLacp(child):
    svc = 1
    uni = 1
    delNniInt(child)
    time.sleep(1)
    deflacpTime(child)
    time.sleep(1)
    delPortCh(child)
    time.sleep(1)   
    mc.dltServi(child,svc,uni)
    time.sleep(1)

### Redundant Static Link Aggregation ###	  

def confStaticLag(child,dut): 
    result = []
    confLag (child)
    result.append(lav.checkPortChannel(dut,'static')) ##['static','lacp','hotstandby']
    time.sleep(1)
    result.append(lav.checkBcmPort(dut,'hotstandby')) ##['normal','hotstandby']
    time.sleep(1)
    removeLag(child)
    print(result)  
    return result.count('Ok')

def confBasicLacp(child,dut): 
    result = []
    confLacp(child)
    time.sleep(10)
    result.append(lav.checkPortChannel(dut,'lacp'))
    result.append(lav.checkLacpInternal(dut,'active')) ##['active','passive','hotstandby']
    time.sleep(1)
    delNniInt(child)
    time.sleep(1)
    passiveLacp(child)
    time.sleep(1)    
    addNniInt(child)
    time.sleep(5)    
    result.append(lav.checkPortChannel(dut,'lacp'))
    result.append(lav.checkLacpInternal(dut,'passive'))
    time.sleep(1)
    changeMaxMember(child,1)
    time.sleep(5)
    result.append(lav.checkPortChannel(dut,'hotstandby'))
    result.append(lav.checkLacpInternal(dut,'hotstandby'))
    time.sleep(1)    
    result.append(lav.checkBcmPort(dut,'hotstandby'))
    changeMaxMember(child,8)
    time.sleep(5)
    result.append(lav.checkPortChannel(dut,'lacp'))
    result.append(lav.checkLacpInternal(dut,'passive'))
    time.sleep(1)  
    result.append(lav.checkBcmPort(dut,'normal'))
    time.sleep(1)
    removeLacp(child)  
    print(result)  
    return result.count('Ok')

