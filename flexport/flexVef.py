# $language = "python"
# $interface = "1.0"

import pexpect
import sys
import time
import os

sys.path.append("./basic")
sys.path.append("./mef")
sys.path.append("./flexport")

import basic.basicConf as bc


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

# Flex-Port check Function 
def checkFlexP(status,host):               
    sub_child = bc.connect(host) 
    bc.enable(sub_child)

    with open('/home/jhjang/auto/utest_suite/log/flexPort_check.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh flexport')
        sub_child.expect('#')
        sub_child.sendline('show int status')
        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/flexPort_check.txt', 'rt') as fr:

        if "Detach" in status:   
            redResult = fr.readlines() 
            sRedResult = str(redResult).split()
            result = sRedResult.count('disable')
            if result == 16: 
                return 'Ok' 
            else:
                return 'Nok'
        elif "Attach" in status:  ## check enabled port unmbers
            redResult = fr.readlines() 
            sRedResult = str(redResult).split()
            result = sRedResult.count('enable')
            if result == 12: # enabled port unmbers
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('cpri')
            if result == 12:
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI10" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('60(Gb)')
            if result == 12:
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI8" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('50(Gb)')
            if result == 12:
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI7" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('20(Gb)') 
            if result == 12:
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI5" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('4915') 
            if result == 8:
                return 'Ok' 
            else:
                return 'Nok'
        elif "CPRI3" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('2457') 
            if result == 8:
                return 'Ok' 
            else:
                return 'Nok'
        elif "ETH" in status:
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('ethernet') 
            if result == 16:
                return 'Ok' 
            else:
                return 'Nok'
        elif "25G" in status: ## Check 26G port numbers
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('50(Gb)') 
            if result == 12:
                return 'Ok' 
            else:
                return 'Nok'

        elif "10G" in status: ## Check 26G port numbers
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('20(Gb)') 
            if result == 8:
                return 'Ok' 
            else:
                return 'Nok'
        elif "1G" in status: ## Check 26G port numbers
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('(ge)') 
            if result == 8:
                return 'Ok' 
            else:
                return 'Nok'

# Flex-Port check Function 
def checkFlexPExam(status,host):               
    sub_child = bc.connect(host) 
    bc.enable(sub_child)

    with open('/home/jhjang/auto/utest_suite/log/flexPortExam_check.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh flexport')
        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/flexPortExam_check.txt', 'rt') as fr:
        if "Exampl1" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('60(Gb)')
            if result == 2:
                return 'Ok' 
            else:
                return 'Nok'
        elif "Exampl2" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('60(Gb)')
            if result == 4:
                return 'Ok' 
            else:
                return 'Nok'
        elif "Exampl3" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('60(Gb)')
            if result == 6:
                return 'Ok' 
            else:
                return 'Nok'
        elif "Exampl4" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('50(Gb)')
            if result == 2:
                return 'Ok' 
            else:
                return 'Nok'
        elif "Exampl5" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('50(Gb)')
            if result == 4:
                return 'Ok' 
            else:
                return 'Nok'

# Flex-Port Breakout check Function 
def checkBreakout(status,host):               
    sub_child = bc.connect(host) 
    bc.enable(sub_child)

    with open('/home/jhjang/auto/utest_suite/log/flexPort_breakout_check.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh flexport')
        sub_child.expect('#')
#        sub_child.sendline('show int status')
#        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/flexPort_breakout_check.txt', 'rt') as fr:

        if "100Gto25G" in status:   
            redResult = fr.readlines() 
            sRedResult = str(redResult).split()
#            print(sRedResult)
            result1 = sRedResult.count('25(GbE)')
            result2 = sRedResult.count('breakout')
            result3 = sRedResult.count("1/25/1,1/25/2,1/25/3,1/25/4\\n',")
#            print ('1: ',result1,':',result2,':',result3)
            if result1 == 1 and result2 == 1 and result3 == 1: 
                return 'Ok' 
            else:
                return 'Nok'
        elif "100Gto10G" in status:  
            redResult = fr.readlines() 
            sRedResult = str(redResult).split()
            result1 = sRedResult.count('40(Gb)')
            result2 = sRedResult.count('breakout')
            result3 = sRedResult.count("1/26/1,1/26/2,1/26/3,1/26/4\\n',")
#            print ('2: ',result1,':',result2,':',result3)
            if result1 == 1 and result2 == 2 and result3 == 1: 
                return 'Ok' 
            else:
                return 'Nok'
        elif "detach" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('breakout')
            if result == 2:
                return 'Ok' 
            else:
                return 'Nok'
        elif "attach" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('enable')
            if result == 16:
                return 'Ok' 
            else:
                return 'Nok'
        elif "noBreakout" in status: ## Check a flexport type is CPRI
            redResult = fr.readlines()
            sRedResult = str(redResult).split()
            result = sRedResult.count('breakout')
            if result == 0:
                return 'Ok' 
            else:
                return 'Nok'
        

### Show Flex Port ###	  
def ShowInFlex(child):
    child.sendline ('\n')
    child.expect("#")
    child.sendline("show flexport")
    child.expect("#")
    
### Show Interface ###	  
def ShowInt(child):
    child.sendline ('\n')
    child.expect("#")
    child.sendline("show interface status")
    child.expect("#")