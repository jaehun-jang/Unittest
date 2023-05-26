# funMefVef.py
# $language = "python"

import pexpect
import sys
import time
import os

sys.path.append("./basic")
import basic.basicConf as fbc

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

### Check Number of Service ###
def checkNmbrSvc(host):                 
    sub_child = fbc.connect(host) 
    fbc.enable(sub_child)
    Command = "show ethernet nni"

    with open('/home/jhjang/auto/utest_suite/log/svc_num.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline(Command)
        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/svc_num.txt', 'rt') as fr:
        readResult = fr.readlines()[9]
        result = readResult.split()
        os.remove('/home/jhjang/auto/utest_suite/log/svc_num.txt')
        return int(result[4]) # 'Number of EVC in NNI#

### Check Number of UNI ###
def checkNmbrUni(host):                 
    sub_child = fbc.connect(host)
    fbc.enable(sub_child)
    Command = 'show ethernet uni brief'

    with open('/home/jhjang/auto/utest_suite/log/uni_num.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline(Command)
        sub_child.expect('#')

    with open('/home/jhjang/auto/utest_suite/log/uni_num.txt', 'rt') as fr:
        readResult = fr.readlines()[6:30]
        readResult = str(readResult)
        readCnt = readResult.count('uni')
        os.remove('/home/jhjang/auto/utest_suite/log/uni_num.txt')
        return readCnt # 'UNI count by show ethernet uni brief#

### Check Number of SEP ###
def checkNmbrSep(uni,host):                 
    sub_child = fbc.connect(host) 
    fbc.enable(sub_child)
    Command = "show ethernet uni uni"
    resultSum = 0
    for i in range (1,uni+1,1):
        with open('/home/jhjang/auto/utest_suite/log/sep_num'+str(i)+'.txt', 'wt') as fw:
            sub_child.logfile = fw
            sub_child.sendline(Command+str(i))
            sub_child.expect('#')
            time.sleep(1) 
            
        with open('/home/jhjang/auto/utest_suite/log/sep_num'+str(i)+'.txt', 'rt') as fr:
            readResult = fr.readlines()[15]
            print(readResult)
            result = readResult.split()
            resultSum  += int(result[4])
            os.remove('/home/jhjang/auto/utest_suite/log/sep_num'+str(i)+'.txt')
    return resultSum # 'SUM of sep of UNIs#

def checkDflSvc(host):                 
    sub_child = fbc.connect(host) 
    fbc.enable(sub_child)
    with open('/home/jhjang/auto/utest_suite/log/dfl_svc.txt', 'wt') as fw:
        sub_child.logfile = fw
        sub_child.sendline('show ethernet service')
        sub_child.expect('#')
        sub_child.sendline('show ethernet uni')
        sub_child.expect('#')
        sub_child.sendline('show ethernet nni')
        sub_child.expect('#')
        time.sleep(1) 
        
    with open('/home/jhjang/auto/utest_suite/log/dfl_svc.txt', 'rt') as fr:
        readResult = fr.readlines()       
        result = len(readResult)
#        print(result)
        os.remove('/home/jhjang/auto/utest_suite/log/dfl_svc.txt')
    return result # 'SUM of CLI result#
