# funBaVef.py

# $language = "python"
# $interface = "1.0"

import pexpect
import sys
import time
import os
import basic.basicConf as bc

### Check VLAN Number ###

def checkVlanNum(host):                 
    sub_child = bc.connect(host)  
    Command = "show vlan summary"

    with open('/home/jhjang/auto/utest_suite/log/vlan_num.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline(Command)
        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/vlan_num.txt', 'rt') as fr:
        readResult = fr.readlines()[4]
        result = readResult.split()
        os.remove('/home/jhjang/auto/utest_suite/log/vlan_num.txt')
        return result[5]

### Check MAX VTY SESSION ###
def checkVtySsion(host):
    user = 'root'
    pwd = 'admin'
    index = 0
    cont = 1 
    x = []
    while index == 0:
        conStr = 'ssh '+ user + '@'+ host
        sub_child = pexpect.spawn(conStr,encoding='utf-8')
        sub_child.expect('assword')
        sub_child.sendline(pwd)
        index = sub_child.expect([
            '>',
            'Try again later',
            pexpect.TIMEOUT,
        ])
        if index == 0:        
            cont = cont + 1
            x.append(sub_child)
            print('number of session: '+ str(cont))
            time.sleep(0.5)
            continue
        elif index == 1:
            print ('reached to max session')
            return cont
        elif index == 2:
            print ('[-] Error Connecting')
            break

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
            os.remove('/home/jhjang/auto/utest_suite/log/'+ testName +'_plog.txt')
            return 'OK'
        else:
            print ('#' *10 + 'occur proecee log' + '#' * 10)
            return 'Nok'

### Exception log ###
def ExceptionLog(testName):                 
    with open('/home/jhjang/auto/utest_suite/log/Exception_log.txt', 'at') as fw:
        fw.writelines('Exception occurs while performing ' + testName + ' ' )
        return('exception')

     

             
