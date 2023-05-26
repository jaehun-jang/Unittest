# funBaVef.py

# $language = "python"
# $interface = "1.0"

import pexpect
import sys
import time
import os

sys.path.append("./basic")
import basic.basicConf as bc

### Check VLAN Number ###

def checkPortChannel(host,state):                 
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkPortChannel.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('show port-channel summary')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkPortChannel.txt', 'rt') as fr:
        passCnt = 0
        chickList1 = ['po1','(SU)','NONE','1/23(P)*','1/24(P)']
        chickList2 = ['(SU)','LACP','8','1/23(P)','1/24(P)'] 
        chickList3 = ['(SU)','LACP','1','1/23(P)','1/24(D)'] 
        readResult = fr.readlines()[11]
        spResult = str(readResult).split()
        del spResult[0]
        print(spResult)
        if state == 'static':
            for i in chickList1:
                print(i)
                passCnt += spResult.count(i)
            print(passCnt)
        elif state == 'lacp':
            for i in chickList2:
                print(i)
                passCnt += spResult.count(i)
        elif state == 'hotstandby':
            for i in chickList3:
                print(i)
                passCnt += spResult.count(i)                
        os.remove('/home/jhjang/auto/utest_suite/log/checkPortChannel.txt')
        if passCnt == 5: 
            return 'Ok' 
        else:
            return 'Nok'

def checkLacpInternal(host,state):                 
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/checkLacpInternal.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('sh lacp 1 internal ')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/checkLacpInternal.txt', 'rt') as fr:
        passCnt = 0
        chickList1 = ['FA','bndl'] 
        chickList2 = ['FP','bndl'] 
        chickList3 = ['FP','standby'] 
        readResult = fr.readlines()[11:13]
        spResult = str(readResult).split()
        print(readResult)        
        print(spResult)
        if state == 'active':
            for i in chickList1:
                print(i)
                passCnt += spResult.count(i)
            print(passCnt)
        elif state == 'passive':
            for i in chickList2:
                print(i)                
                passCnt += spResult.count(i)
            print(passCnt)
        elif state == 'hotstandby':
            for i in chickList3:
                print(i)
                passCnt += spResult.count(i)
            print(passCnt)  

        os.remove('/home/jhjang/auto/utest_suite/log/checkLacpInternal.txt')
        if passCnt == 2: 
            return 'Ok' 
        else:
            return 'Nok'
        # if state == 'hotstandby':
        #         return 'Ok' if pass_count == 3 else 'Nok'
        #     else:
        #         return 'Ok' if pass_count == 2 else 'Nok'


def checkBcmPort(host,state):                 
    sub_child = bc.connect(host)  
    with open('/home/jhjang/auto/utest_suite/log/bcmPortStat.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('debug no-auth')
        sub_child.expect('#')
        sub_child.sendline('bcm-shell')
        sub_child.expect('> ')
        sub_child.sendline('ps')
        sub_child.expect('>')
        sub_child.sendline('exit')
        sub_child.expect('#')
    with open('/home/jhjang/auto/utest_suite/log/bcmPortStat.txt', 'rt') as fr:
        readResult = fr.readlines()[34]
        spResult = str(readResult).split()
        print(spResult)
        os.remove('/home/jhjang/auto/utest_suite/log/bcmPortStat.txt')
        if state == 'hotstandby' and spResult[7] == 'Block': 
            return 'Ok' 
        elif state == 'normal' and spResult[7] == 'Forward': 
            return 'Ok' 
        else:
            return 'Nok'

### Check Process plog ###
def checkPlog(testName,host):                  
    sub_child = bc.connect(host) 
    bc.enable(sub_child)
    Command = "show process plog"

    with open('/home/jhjang/auto/utest_suite/log/'+ testName +'_plog.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline(Command)
        sub_child.expect("ls:")

    with open('/home/jhjang/auto/utest_suite/log/'+ testName +'_plog.txt', 'rt') as fr:
        readResult = fr.readlines()
        if len(readResult) == 4:
#            os.remove('/home/jhjang/auto/utest_suite/log/'+ testName +'_plog.txt')
            return 'ok'
        else:
            print ('#' *10 + 'occur proecee log' + '#' * 10)
            return 'nok'

     

             
