# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
import pexpect
import sys
import time
import os


def login(testName):
    child = connect() 
    fout = open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' )
    child.logfile = fout
    child.logfile_read = sys.stdout
    return child

def keygen(host):
    conStr = 'ssh-keygen -R' + host
    child = pexpect.spawn(conStr, encoding='utf-8')
    return child

def connect(host):
    index = 0
    user = 'root'
    pwd = 'admin'
    conStr = 'ssh '+ user + '@'+ host
    while index <= 4:
        child = pexpect.spawn(conStr, encoding='utf-8')
        child.setwinsize(1500, 1500)
        index = child.expect([
            pexpect.TIMEOUT,
            'Are you sure',
            'assword',
            'Host key verification failed'
        ],timeout=3)
        if index == 0:
            print ('[-] Error Connecting')
            child.kill
            break
        elif index == 1:
            child.sendline('yes')
            child.expect('assword:')       
            child.sendline(pwd)
            child.expect(">")
            child.sendline("en")
            child.expect("#")
            return child 
        elif index == 2:
            child.sendline(pwd)
            child.expect(">")
            child.sendline("en")
            child.expect("#")
            return child
        elif index == 3:
            os.system('ssh-keygen -f "/home/jhjang/.ssh/known_hosts" -R "%s"' % (host))
            continue

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

### default SetUp  ###	  
def defaultSetup(child,host):
    confT(child)
    child.sendline ('\n')
    child.sendline('logging console')
    child.expect("#")
    time.sleep(1)  
    if host =='192.168.0.201':
        child.sendline('hostname LAB1')
        child.expect("#")
    if host =='192.168.0.202':
        child.sendline('hostname LAB2')
        child.expect("#")
    time.sleep(1) 
    child.sendline('aaa auth attempts login 0')
    child.expect("#")
    time.sleep(1)       
    end(child)

### Create maximum numberof VLAN  ###	  
def crtVlan(child,vlans):
    confT(child)
    if vlans == 1:
        return
    else: 
        child.sendline ('\n')
        child.expect("#")
        child.sendline("vlan 2-%s" % str(vlans))
        time.sleep(60)
        child.expect("#")
    end(child)

### Delet maximum numberof VLAN  ###	  
def dltVlan(child,vlans):
    confT(child)
    if vlans == 1:
        return
    else: 
        child.sendline ('\n')
        child.expect("#")
        child.sendline("no vlan 2-%s" % str(vlans))
        time.sleep(60)
        child.expect("#")
    end(child)

def defVlan(child):
    confT(child)
    child.sendline ('\n')
    child.expect("#")
    child.sendline("no vlan 2-4095" )
    time.sleep(3)
    child.expect("#")
    end(child)

### Config maximum numberof vty session  ###	  
def confVty(child,vty):
    confT(child)
    child.sendline ('\n')
    child.expect("#")
    child.sendline("no line vty %s 39" % vty)
    time.sleep(15)
    child.expect("#")
    end(child)

### Restore maximum numberof vty session  ###	  
def deftVty(child):
    confT(child)
    child.sendline ('\n')
    child.expect("#")
    child.sendline("line vty 1 39")
    time.sleep(15)
    child.expect("#")
    end(child)
        
### Restore maximum numberof vty session  ###	  
def deftSystem(child):
    child.sendline ('write default')
    child.expect("erased!")
    child.sendline("y")
    child.expect("#")
    child.sendline("reload")
    child.expect("(y/n)")
    child.sendline("n")
    child.expect("(y/n)")
    child.sendline("y")
    time.sleep(180) 
    child.expect(None)

