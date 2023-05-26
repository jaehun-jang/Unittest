# $language = "python"
# $interface = "1.0"

import unittest
import pexpect
import sys
import time
import os
import basic.basicConf as bc
import basic.basicVef as bv
import mef.mefConf as mc
import mef.mefVef as mv
import flexport.flexConf as fc
import flexport.flexVef as fv
import flexport.flexConfExam as fce
import flexport.flexBreakoutConf as fbc
import lag.lagConf as lac
import lag.lagVef as lav
import lldp.lldpConf as llc
import lldp.lldpVef as llv
import eoam.eoamConf as eoc
import eoam.eoamVef as eov

#######################  UNITTEST   ##########################

dut1 = '192.168.0.201'
dut2 = '192.168.0.202'

# TestCase를 작성
class CustomTests(unittest.TestCase):

    # dut1 = '192.168.0.201'
    # dut2 = '192.168.0.202'

    def setUp(self):
        print('➽', sys._getframe(0).f_code.co_name)
        """테스트 시작되기 전 파일 작성"""  
        child = bc.connect(dut1)    
        child2 = bc.connect(dut2)
        bc.defaultSetup(child,dut1)   
        bc.defaultSetup(child2,dut2)
        child.close() 
        child2.close()

    def tearDown(self):
        print('➽', sys._getframe(0).f_code.co_name)
        """테스트 종료 후 파일 삭제 """ 

    def test_runs_001(self):
        """"
        maximum number of VLAN TEST 
        """
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " maximum number of VLAN TEST   " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout 
            try:        
                bc.disTitle(child,Title)
#                vlan = int(input('Enter the last vlan number: '))
                vlan = 4020
                bc.crtVlan(child,vlan)
                time.sleep(1)
                self.assertEqual(bv.checkVlanNum(dut1),str(vlan))         
                time.sleep(1)        
                bc.dltVlan(child,vlan)
                self.assertEqual(bv.checkVlanNum(dut1),'1')        
                time.sleep(1) 
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)       
            except: # This code is added to execute removeLag() function when the test fail.
                bc.defVlan(child)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2) 

    def test_runs_002(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " maximum number of VTY Session TEST    " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout 
            try: 
                bc.disTitle(child,Title) 
                self.assertEqual(bv.checkVtySsion(dut1),40) 
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2) 
            except:  
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2) 

    def test_runs_003(self): 
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " maximum number of VTY Session Configuration TEST    " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout
            try:     
                bc.disTitle(child,Title) 
#                vty = input('Enter the maximum numbers of vty sessions: ')
                vty = 8
                bc.confVty(child,vty)
                self.assertEqual(bv.checkVtySsion(dut1),int(vty)) 
                time.sleep(1)
                bc.deftVty(child)
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2) 
            except:
                bc.deftVty(child)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)

    def test_runs_004(self): 
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " maximum number of of SVCs TEST    " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout
            try:  
                bc.disTitle(child,Title) 
#                svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())
#                while svc == 0 or uni == 0 or svc < uni or svc > 256 or uni > 24:  
#                    print ('Try agan, the number of UNIs must be larger than EVCs: ')
#                    svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())    
                svc = 256
                uni = 24 
                mc.crtServi(child,svc,uni)
                self.assertEqual(mv.checkNmbrSvc(dut1),svc) 
                time.sleep(1)
                self.assertEqual(mv.checkNmbrUni(dut1),uni) 
                time.sleep(1)
                self.assertEqual(mv.checkNmbrSep(uni,dut1),svc)
                time.sleep(1) 
                mc.dltServi(child,svc,uni)
                self.assertLessEqual(mv.checkDflSvc(dut1),11)
                time.sleep(1)        
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)  
            except:
                mc.dltServi(child,svc,uni)               
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)

    def test_runs_005(self): 
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Basic configuration Test " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout
            try:  
                bc.disTitle(child,Title) 
                self.assertEqual(fc.confFlexPort(child,dut1),12)
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2) 
            except: 
                bc.deftSystem(child)
                time.sleep(1)   
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)  

    def test_runs_006(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Example configuration Test " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout
            try: 
                bc.disTitle(child,Title) 
                self.assertEqual(fce.confFlexPortExam(child,dut1),7)
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)  
            except:
                bc.deftSystem(child)
                time.sleep(1) 
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2) 

    def test_runs_007(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Breakout configuration Test " + "#" * 5
        child = bc.connect(dut1) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout
            try: 
                bc.disTitle(child,Title) 
                self.assertEqual(fbc.flexPortBreakout(child,dut1),5)
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)  
            except:
                bc.deftSystem(child)
                time.sleep(1) 
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2) 

    def test_runs_008(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Link Aggregation Test " + "#" * 5
        child = bc.connect(dut1)
        child2 = bc.connect(dut2) 
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child.logfile = fout
            child.logfile_read = sys.stdout 
            try: 
                bc.disTitle(child,Title)
                lac.confLag (child2) 
                self.assertEqual(lac.confStaticLag(child,dut1),2)
                time.sleep(1)
                lac.removeLag(child2)
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2) 
            except:
                lac.removeLag(child2)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2) 

    def test_runs_009(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " LACP Basic Test " + "#" * 5
        child1 = bc.connect(dut1) 
        child2 = bc.connect(dut2)
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child1.logfile = fout
            child1.logfile_read = sys.stdout
            try: 
                bc.disTitle(child1,Title)
                lac.confLacp(child2)
                self.assertEqual(lac.confBasicLacp(child1,dut1),10)
                time.sleep(1)
                lac.removeLacp(child2) 
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2) 
            except: 
                lac.removeLacp(child2)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)

    def test_runs_010(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " LLDP Basic Test " + "#" * 5
        child1 = bc.connect(dut1) 
        child2 = bc.connect(dut2)
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child1.logfile = fout
            child1.logfile_read = sys.stdout
            try: 
                bc.disTitle(child1,Title)
                llc.confEthService(child2)
                self.assertEqual(llc.confBasicLldp(child1,dut2),7)
                time.sleep(1)
                llc.removeEthService(child2) 
                time.sleep(1)
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)
            except: 
                llc.removeEthService(child2)  
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)

    def test_runs_011(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " EOAM Basic Test " + "#" * 5
        child1 = bc.connect(dut1) 
        child2 = bc.connect(dut2)
        with open('/home/jhjang/auto/utest_suite/log/' + testName +'_log.txt', 'wt' ) as fout: 
            child1.logfile = fout
            child1.logfile_read = sys.stdout
            try: 
                bc.disTitle(child1,Title)
                eoc.confEoam(child2)
                self.assertEqual(eoc.confBasicEoam(child1,dut1,dut2),8)
                time.sleep(1)
                eoc.removeEoam(child2) 
                time.sleep(1)                
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(2)
            except: 
                eoc.removeEoam(child2)  
                self.assertEqual(bv.checkPlog(testName,dut1),'OK')
                time.sleep(1)                
                self.assertEqual(bv.ExceptionLog(testName),'normal')
                time.sleep(2)

# unittest를 실행
if __name__ == '__main__':
    unittest.main()






