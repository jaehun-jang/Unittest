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

### Breakout to 25G*4 ###	 	  
def breakoutTo25G(child):
    child.sendline("flexport-group " + str(13))
    child.expect("#")
    child.sendline("breakout 25g-4x")
    child.expect("#")
    time.sleep(1) 

### Breakout to 10G*4  ###	   
def breakoutTo10G(child):
    child.sendline("flexport-group " + str(14))
    child.expect("#")
    child.sendline("breakout 10g-4x")
    child.expect("#")
    time.sleep(1) 

### Detach 100G ### 	   
def detachBreakout(child):
    child.sendline("flexport-group " + str(14))
    child.expect("#")
    child.sendline("detach member all ")
    child.expect("#")
    time.sleep(1)

### Attach 100G ### 	   
def attachBreakout(child):
    child.sendline("flexport-group " + str(14))
    child.expect("#")
    child.sendline("attach member all ")
    child.expect("#")
    time.sleep(1)

### No Breakout###	   
def noBreakout(child):
    for intCon in range (13, 15, 1):
        child.sendline("flexport-group " + str(intCon))
        child.expect("#")
        child.sendline("no breakout")
        child.expect("#")
        time.sleep(1)

############################################################################
 
    
#+++++++++++++++++++++++ Flex-Port Main Function ++++++++++++++++++++++++++!

def flexPortBreakout(child,host):
    result = []
    confT(child)

    ### Breakout to 25G*4 ###
    title = "### Breakout to 25G*4 ###"
    action = '100Gto25G'
    disTitle(child,title)
    breakoutTo25G(child)
    time.sleep(5)
    result.append(ffv.checkBreakout(action,host))
    time.sleep(1)
    print(result)

    ### Breakout to 10G*4 ###       
    title = "### Breakout to 10G*4 ###"
    action = '100Gto10G'
    disTitle(child,title)
    breakoutTo10G(child)
    time.sleep(5)
    result.append(ffv.checkBreakout(action,host))
    time.sleep(1)
    print(result)

    ### breakoutIntDetach ###       
    title = "### breakoutIntDetach ###"
    action = 'detach'
    disTitle(child,title)
    detachBreakout(child)
    time.sleep(5)
    result.append(ffv.checkBreakout(action,host))
    time.sleep(1)
    print(result)

    ### breakoutIntAttach ###       
    title = "### breakoutIntAttach ###"
    action = 'attach'
    disTitle(child,title)
    attachBreakout(child)
    time.sleep(5)
    result.append(ffv.checkBreakout(action,host))
    time.sleep(1)
    print(result)

    ### release Breakout  ###       
    title = "### release Breakout ###"
    action = 'noBreakout'
    disTitle(child,title)
    noBreakout(child)
    time.sleep(5)
    end(child)
    result.append(ffv.checkBreakout(action,host))
    time.sleep(1)
    print(result)
    os.remove('/home/jhjang/auto/utest_suite/log/flexPort_breakout_check.txt')
    return result.count('Ok')

## ++++++++++++++++++++++++++++++++++++++ ##

