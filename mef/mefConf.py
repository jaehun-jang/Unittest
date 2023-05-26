# funMefVef.py
# $language = "python"
# $interface = "1.0"

from re import I
import pexpect
import sys
import time
import os


###### Element Function  ######
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

def decoration(func):
    def wrapper():
        confT()
        func()
        end()
    return wrapper

### Create maximum numberof VLAN  ###	  
def crtVlan(child,vlans):
    if vlans == 1:
        return
    else: 
        child.sendline ('\n')
        child.expect("#")
        child.sendline("vlan 2-%s" % str(vlans))
        child.expect("#")

### Delet maximum numberof VLAN  ###	   
def dltVlan(child,vlans):
    if vlans == 1:
        return
    else: 
        child.sendline ('\n')
        child.expect("#")
        child.sendline("no vlan 2-%s" % str(vlans))
        time.sleep(2)
        child.sendline ('\n')    
        child.expect("#",timeout=60)

### Create EVC and Add SVLAN ###	   
def crtSvc(child,svc):
    for i in range (1,svc+1,1):
        child.sendline("ethernet service add evc" + str(i))
        child.expect("#")
        child.sendline("svlan " + str(i))
        child.expect("#")
        child.sendline("service type evpl")
        child.expect("#")
        time.sleep(0.2)

### Create NNI and add Service ###  
def crtNni(child,svc):
    child.sendline("ethernet nni add nni1")
    child.expect("#")
    child.sendline("map interface 1/25")
    child.sendline()
    for i in range (1,svc+1,1):
        child.sendline("add service evc" + str(i))
        child.expect("#")
        time.sleep(0.2)

### Create UNI ###  
def crtUni(child,uni):
        for i in range (1, uni+1, 1):
            child.sendline("ethernet uni add uni" + str(i))
            child.expect("#")
            child.sendline("map interface 1/" + str(i))
            child.expect("#")
            child.sendline("all-to-one-bundling disable")
            child.expect("#")
            child.sendline("multiplex enable")
            child.expect("#")
            child.sendline("bundling enable")
            child.expect("#")
            child.sendline("max-svc 256")
            child.expect("#")
            time.sleep(0.2)
   
### Add Service to UNI###  
def addSvc(child,svc,uni): 
    sep = divmod (svc, uni)  # Return value of divmod is tuple.
    sepTu0 = int(sep[0])     # Extract the value of a tuple through an index
    sepTu1 = int(sep[1])     # Extract the value of a tuple through an index (reminder)
    for uniCnt in range (1, uni+1, 1): # Number of UNI 
        child.sendline("ethernet uni uni" + str(uniCnt))
        child.expect("#")
        if sepTu1 == 0: # There is no remainder SVCs to be added to UNI
            for i in range (1, sepTu0+1, 1): 
                svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0   
                child.sendline("add service evc" + str(svcCnt)) 
                child.expect("#")
        elif sepTu1 != 0: # There is remainder SVCs to be added to UNI, therefor remainder SVCs should be add to th last UNI.
            if uni != uniCnt:
                for i in range (1, sepTu0+1, 1):  
                    svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0
                    child.sendline("add service evc" + str(svcCnt))
                    child.expect("#")
                    time.sleep(0.2)
            elif uni == uniCnt:  # for to add remained SEPs to the last UNI
                for i in range (1, sepTu0+sepTu1+1, 1):  
                    svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0 # add remainder
                    child.sendline("add service evc" + str(svcCnt))
                    child.expect("#")
                    time.sleep(0.2)

### Add CE-VLAN into SEP###  
def addCvlan(child,svc,uni):
    sep = divmod (svc, uni)
    sepTu0 = int(sep[0])
    sepTu1 = int(sep[1]) 
    cVlan = divmod (4095, svc)
    cVlanTu0 = int(cVlan[0])
    cVlanTu1 = int(cVlan[1]) 
    for uniCnt in range (1, uni+1): # Number of UNI 
        if sepTu1 == 0: # There is no remainder SVCs to be added to UNI
            for i in range (1, sepTu0 + 1, 1):  
                if uniCnt == uni and i == sepTu0: # for to add remained CE-VLANs to the last SEP 
                    svcCnt = (uniCnt - 1 ) * sepTu0 + i 
                    child.sendline("ethernet sep uni" + str(uniCnt) +"-evc"+ str(svcCnt))
                    child.expect("#")
                    cVlanCnt = (svcCnt - 1) * cVlanTu0 + 1 
                    child.sendline("add vlan " + str(cVlanCnt) +"-"+ str(svcCnt*cVlanTu0+cVlanTu1)) ###  add remained CE-VLAN
                    child.expect("#")
                else: # for Not last SEP
                    svcCnt = (uniCnt - 1 ) * sepTu0 + i 
                    child.sendline("ethernet sep uni" + str(uniCnt) +"-evc"+ str(svcCnt))
                    child.expect("#")
                    cVlanCnt = (svcCnt - 1) * cVlanTu0 + 1 
                    child.sendline("add vlan " + str(cVlanCnt) +"-"+ str(svcCnt*cVlanTu0))
                    child.expect("#")

        elif sepTu1 != 0: # There is remainder SVCs to be added to UNI, therefor remainder SVCs should be add to th last UNI.  
            if uniCnt != uni : # for Not the last SEP
                for i in range (1, sepTu0 + 1, 1): 
                    svcCnt = (uniCnt - 1 ) * sepTu0 + i 
                    child.sendline("ethernet sep uni" + str(uniCnt) +"-evc"+ str(svcCnt))
                    child.expect("#")
                    cVlanCnt = (svcCnt - 1) * cVlanTu0 + 1 
                    child.sendline("add vlan " + str(cVlanCnt) +"-"+ str(svcCnt*cVlanTu0))
                    child.expect("#")
            elif uniCnt == uni: # for the last SEP
                for i in range (1, sepTu0 + sepTu1 + 1, 1): 
#                    print(uni,i,cVlanTu0,cVlanTu1)
                    if uniCnt == uni and i == sepTu0 + sepTu1: # for to add remained CE-VLANs to the last SEP 
                        svcCnt = (uniCnt - 1 ) * sepTu0 + i 
                        child.sendline("ethernet sep uni" + str(uniCnt) +"-evc"+ str(svcCnt))
                        child.expect("#")
                        cVlanCnt = (svcCnt - 1) * cVlanTu0 + 1 
                        child.sendline("add vlan " + str(cVlanCnt) +"-"+ str(svcCnt*cVlanTu0+cVlanTu1)) ###  add remained Service
                        child.expect("#")
                    else:
                        svcCnt = (uniCnt - 1 ) * sepTu0 + i 
                        child.sendline("ethernet sep uni" + str(uniCnt) +"-evc"+ str(svcCnt))
                        child.expect("#")
                        cVlanCnt = (svcCnt - 1) * cVlanTu0 + 1 
                        child.sendline("add vlan " + str(cVlanCnt) +"-"+ str(svcCnt*cVlanTu0))
                        child.expect("#")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

### Delete UNI and del Service ###  
def dltSvcUni(child,svc,uni):
    sep = divmod (svc, uni)
    sepTu0 = int(sep[0])
    sepTu1 = int(sep[1])   
    for uniCnt in range (1, uni+1, 1): # Number of UNI 
        child.sendline("ethernet uni uni" + str(uniCnt))
        child.expect("#")
        if sepTu1 == 0: # There is no remainder SVCs to be added to UNI
            for i in range (1, sepTu0+1, 1): 
                svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0   
                child.sendline("del service evc" + str(svcCnt)) 
                child.expect("#")
        elif sepTu1 != 0: # There is remainder SVCs to be added to UNI, therefor remainder SVCs should be add to th last UNI.
            if uni != uniCnt:
                for i in range (1, sepTu0+1, 1):  
                    svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0
                    child.sendline("del service evc" + str(svcCnt))
                    child.expect("#")
                    time.sleep(0.2)
            elif uni == uniCnt:  # for to add remained SEPs to the last UNI
                for i in range (1, sepTu0+sepTu1+1, 1):  
                    svcCnt = (uniCnt) * sepTu0 + (i) - sepTu0 # add remainder
                    child.sendline("del service evc" + str(svcCnt))
                    child.expect("#")
                    time.sleep(0.2)
        child.sendline("no map interface")
        child.expect("#")
        child.sendline("ethernet uni del uni" + str(uniCnt))
        child.expect("#")

### Delete Service and NNI ###   
def dltNni(child,svc):  	
    child.sendline("ethernet nni nni1")
    child.expect("#")
    for Devc in range (1, svc+1, 1):
        child.sendline("del service evc" + str(Devc))
        child.expect("#")
        time.sleep(0.2) 
    child.sendline("ethernet nni del nni1")
    child.expect("#")

### Delete Service	### 
def dltSvc(child,svc):	
    for Dsvc in range (1, svc+1, 1):
        child.sendline("ethernet service del evc" + str(Dsvc))
        child.expect("#")
        time.sleep(0.2)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++!

def crtServi(child,svc,uni): 
    confT(child)
    #Create SVLAN
    crtVlan(child,svc)
    end(child)
    time.sleep(1)
    #Create EVC and Add SVLAN
    confT(child)
    crtSvc(child,svc)
    end(child)
    time.sleep(1)
    #Create NNI and add Service
    confT(child)
    crtNni(child,svc)
    end(child)
    time.sleep(1)
    #Create UNI and add Service
    confT(child)
    crtUni(child,uni)
    end(child)
    time.sleep(1)
    #Add Service into UNI### 
    confT(child)
    addSvc(child,svc,uni)
    end(child)    
    time.sleep(1)
    #Add CE-VLAN into SEP### 
    confT(child)
    addCvlan(child,svc,uni)
    end(child)  


### Delete Service ### 
def dltServi(child,svc,uni): 
    confT(child)
    #Delete UNI and del Service
    dltSvcUni(child,svc,uni)
    end(child)
    time.sleep(1)
    #Delete Service and NNI 
    confT(child)
    dltNni(child,svc)
    end(child)
    time.sleep(1)
    #Delete Service
    confT(child)
    dltSvc(child,svc)
    end(child)
    time.sleep(1)
    #Delete SVLAN
    confT(child)
    dltVlan(child,svc)
    end(child)

