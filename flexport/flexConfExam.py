# $language = "python"
# $interface = "1.0"


import pexpect
import sys
import time
import os

sys.path.append("./basic")
sys.path.append("./mef")

import flexport.flexVef as ffv


###### Element of Main Function  ######

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

###### Element of Flexport Function  ######


### Detach 100G ### 	   
def detach100g(child):
    for intCon in range (13, 17, 1):
            child.sendline("flexport-group " + str(intCon))
            child.expect("#")
            child.sendline("detach member all ")
            child.expect("#")
            time.sleep(1)

### Attach 100G ### 	   
def attach100g(child):
    for intCon in range (13, 17, 1):
            child.sendline("flexport-group " + str(intCon))
            child.expect("#")
            child.sendline("attach member all ")
            child.expect("#")
            time.sleep(1)

### Change ETH to CPRI ###	 	  
def chgEthToCpri(child):
    for intCon in range (1, 13, 1):
        child.sendline("flexport-group " + str(intCon))
        child.expect("#")
        child.sendline("port-type cpri max-speed cpri7")
        child.expect("#")
        time.sleep(1) 

### Change CPRI to ETH ###	   
def chgCpriToEth(child):
    for intCon in range (1, 13, 1):
        child.sendline("flexport-group " + str(intCon))
        child.expect("#")
        child.sendline("port-type ethernet max-speed 10")
        child.expect("#")
        time.sleep(1) 

### ### Restore Speed  CPRI7###	   
def restCpriSpeed7(child):
    for intCon in range (1, 13, 1):
            child.sendline("flexport-group " + str(intCon))
            child.expect("#")
            child.sendline(" max-speed cpri7 ")
            child.expect("#")
            time.sleep(1)

### Exanple 1  ###  
def example1(child):
    child.sendline('flexport-group 1')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 2')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect("#")
    time.sleep(1)

### Exanple 2  ###  
def example2(child):
    child.sendline('flexport-group 4')
    child.expect("#")
    child.sendline('max-speed cpri8')
    time.sleep(5)
    child.sendline('flexport-group 4')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 3')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect("#")    
    time.sleep(1)

### Exanple 3  ###  
def example3(child):
    child.sendline('flexport-group 5')
    child.expect("#")
    child.sendline('max-speed cpri8')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 6')
    child.expect("#")
    child.sendline('max-speed cpri8')
    time.sleep(5)
    child.sendline('flexport-group 5')
    child.expect("#")
    child.sendline('max-speed cpri7')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 6')
    child.expect("#")
    child.sendline('max-speed cpri10')
    time.sleep(5)
    child.sendline('flexport-group 5')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect('#')
    time.sleep(1)

### Exanple 4  ###  
def example4(child):
    child.sendline('flexport-group 7')
    child.expect("#")
    child.sendline('max-speed cpri10')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 8')
    child.expect("#")
    child.sendline('max-speed cpri10')
    time.sleep(5)
    child.sendline('flexport-group 7')
    child.expect("#")
    child.sendline('max-speed cpri7')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 8')
    child.expect("#")
    child.sendline('max-speed cpri8')
    time.sleep(5)
    child.sendline('flexport-group 7')
    child.expect("#")
    child.sendline('max-speed cpri8')
    child.expect("#")
    time.sleep(1)

### Exanple 5  ###  
def example5(child):
    child.sendline('flexport-group 9')
    child.expect("#")
    child.sendline('port-type ethernet max-speed 25')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 10')
    child.expect("#")
    child.sendline('port-type ethernet max-speed 25')
    child.expect("#")    
    time.sleep(1)
    child.sendline('flexport-group 9')
    child.expect("#")
    child.sendline('max-speed 10')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 10')
    child.expect("#")
    child.sendline('port-type cpri max-speed cpri7')
    child.expect("#")  
    time.sleep(1)
    child.sendline('flexport-group 9')
    child.expect("#")
    child.sendline('port-type cpri max-speed cpri8')
    child.expect("#")
    time.sleep(1)
    child.sendline('flexport-group 10')
    child.expect("#")
    child.sendline('port-type cpri max-speed cpri8')
    child.expect("#") 
############################################################################
 
    
#+++++++++++++++++++++++ Flex-Port Main Function ++++++++++++++++++++++++++!

''' Previous Test Item
[1]Example1 (CPRI7 to CPRI10)
[2]Example2 (CPRI7/8 to CPRI10)
[3]Example3 (CPRI8 to CPRI10)
[4]Example4 (CPRI10 to CPRI8)
[5]Example5 (Ethernet to CPRI8)
'''
def confFlexPortExam(child,host):
    result = []
    confT(child)

     ### Change Flex Port To CPRI ###
    title = "### Change Flex Port To CPRI ###"
    action = 'CPRI'
    disTitle(child,title)
    detach100g(child)
    time.sleep(5)
    chgEthToCpri(child)
    time.sleep(10)
    result.append(ffv.checkFlexP(action,host))
    time.sleep(1)
    print(result)
#    a = input('Wait')

    ### Flex Port 'Exampl1 ###       
    title = "### Flex Port 'Exampl1' ###"
    action = 'Exampl1'
    disTitle(child,title)
    example1(child)
    time.sleep(5)
    result.append(ffv.checkFlexPExam(action,host))
    time.sleep(1)
#    a = input('Wait')

    ### Flex Port 'Exampl2 ###       
    title = "### Flex Port 'Exampl2' ###"
    action = 'Exampl2'
    disTitle(child,title)
    example2(child)
    time.sleep(5)
    result.append(ffv.checkFlexPExam(action,host))
    time.sleep(1)
#    a = input('Wait')

    ### Flex Port 'Exampl3 ###       
    title = "### Flex Port 'Exampl3' ###"
    action = 'Exampl3'
    disTitle(child,title)
    example3(child)
    time.sleep(5)
    result.append(ffv.checkFlexPExam(action,host))
    time.sleep(1)
#    a = input('Wait')

    ### Flex Port 'Exampl4 ###       
    title = "### Flex Port 'Exampl4' ###"
    action = 'Exampl4'
    disTitle(child,title)
    example4(child)
    time.sleep(5)
    result.append(ffv.checkFlexPExam(action,host))
    time.sleep(1)
#    a = input('Wait')

    ### Flex Port 'Exampl5 ###       
    title = "### Flex Port 'Exampl5' ###"
    action = 'Exampl5'
    disTitle(child,title)
    example5(child)
    time.sleep(5)
    result.append(ffv.checkFlexPExam(action,host))
    time.sleep(1)
#    a = input('Wait')

    ### Restore Cpri Speed CPRI7 ###
    restCpriSpeed7(child)
    time.sleep(10)

    ### Change Flex Port To ETH ###
    title = "### Change Flex Port To ETH ###"
    action = 'ETH'
    disTitle(child,title)
    attach100g(child)
    time.sleep(5)   
    chgCpriToEth(child)
    time.sleep(10)
    result.append(ffv.checkFlexP(action,host))
    time.sleep(1)
    print(result)
    end(child)
    os.remove('/home/jhjang/auto/utest_suite/log/flexPort_check.txt')
    os.remove('/home/jhjang/auto/utest_suite/log/flexPortExam_check.txt')
    return result.count('Ok')
## ++++++++++++++++++++++++++++++++++++++ ##

