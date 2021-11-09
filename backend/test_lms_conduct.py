import unittest
from api.data_access.lms_conduct import LMSConduct
import datetime
from datetime import timedelta,datetime

# Author : David
class testLMSConduct(unittest.TestCase):

    def setUp(self):
        self.currentDate = datetime.now()
        self.conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=self.currentDate+timedelta(days=10),end_date = self.currentDate+timedelta(days=13), start_register = self.currentDate+timedelta(days=3),end_register = self.currentDate+timedelta(days=7))
    
    def tearDown(self):
        self.currentDate = None
        self.conduct = None

    def testGetCourseId(self):
        self.assertEqual(self.conduct.getCourseId(),1)
    
    def testGetTrainerId(self):
       self.assertEqual(self.conduct.getTrainerId(),1)
    
    def testGetCapacity(self):
        self.assertEqual(self.conduct.getCapacity(),73)
    
    def testSetCapacity(self):
        self.assertRaises(Exception,self.conduct.setCapacity,-4)
        self.assertRaises(Exception,self.conduct.setCapacity,7.5)
        self.assertRaises(Exception,self.conduct.setCapacity,"bla bla bla")
        self.assertEqual(self.conduct.setCapacity(28),28)
        self.assertEqual(self.conduct.setCapacity(0),0)
        self.assertNotEqual(self.conduct.setCapacity(20),0)
    
    def testIncrementCapacity(self):
        self.assertEqual(self.conduct.incrementCapacity(),74)
        self.assertEqual(self.conduct.incrementCapacity(),75)
        self.assertNotEqual(self.conduct.incrementCapacity(),77)
        self.assertNotEqual(self.conduct.incrementCapacity(),76)
    
    def testDecrementCapacity(self):
        self.assertEqual(self.conduct.decrementCapacity(),72)
        self.assertNotEqual(self.conduct.decrementCapacity(),70)
        self.assertNotEqual(self.conduct.decrementCapacity(),80)
        self.conduct.capacity=0
        self.assertRaises(Exception,self.conduct.decrementCapacity)
    
    def testIncreaseCapacity(self):
        self.assertRaises(Exception,self.conduct.increaseCapacity,"kahgiuwe aiuwhkjfwkj iuhweiew")
        self.assertRaises(Exception,self.conduct.increaseCapacity,90.524)
        self.assertEqual(self.conduct.increaseCapacity(7),80)
        self.assertNotEqual(self.conduct.increaseCapacity(7),80)
        self.assertNotEqual(self.conduct.increaseCapacity(7),83)
    
    def testDecreaseCapacity(self):
        self.assertRaises(Exception,self.conduct.decreaseCapacity,"abcdefghijklmnop")
        self.assertRaises(Exception,self.conduct.decreaseCapacity,80)
        self.assertRaises(Exception,self.conduct.decreaseCapacity,40.29837153)
        self.assertEqual(self.conduct.decreaseCapacity(65),8)
        self.assertNotEqual(self.conduct.decreaseCapacity(4),2)
        self.assertNotEqual(self.conduct.decreaseCapacity(1),10)

    def testGetStartDate(self):
        self.assertEqual(self.conduct.getStartDate(),self.currentDate+timedelta(days=10))
    
    def testSetStartDate(self):
        self.assertRaises(Exception,self.conduct.setStartDate,"SPM start date")
        self.assertRaises(Exception,self.conduct.setStartDate,self.currentDate-timedelta(days=3))
        self.assertRaises(Exception,self.conduct.setStartDate,self.currentDate+timedelta(days=15))
        self.assertEqual(self.conduct.setStartDate(self.currentDate+timedelta(days=8)),self.currentDate+timedelta(days=8))
        self.assertNotEqual(self.conduct.setStartDate(self.currentDate+timedelta(days=4)),self.currentDate+timedelta(days=8))
    
    def testGetEndDate(self):
        self.assertEqual(self.conduct.getEndDate(),self.currentDate+timedelta(days=13))

    def testSetEndDate(self):
        self.assertRaises(Exception,self.conduct.setEndDate,"ESM end date")
        self.assertRaises(Exception,self.conduct.setEndDate,self.currentDate-timedelta(days=2))
        self.assertRaises(Exception,self.conduct.setEndDate,self.currentDate-timedelta(days=3))
        self.assertEqual(self.conduct.setEndDate(self.currentDate+timedelta(days=15)),self.currentDate+timedelta(days=15))
        self.assertNotEqual(self.conduct.setEndDate(self.currentDate+timedelta(days=16)),self.currentDate+timedelta(days=15))
   
    def testGetStartRegister(self):
        self.assertEqual(self.conduct.getStartRegister(),self.currentDate+timedelta(days=3))
    
    def testSetStartRegister(self):
        self.assertRaises(Exception,self.conduct.setStartRegister,"ESD project deadline")
        self.assertRaises(Exception,self.conduct.setStartRegister,self.currentDate-timedelta(days=7))
        self.assertRaises(Exception,self.conduct.setStartRegister,self.currentDate+timedelta(days=20))
        self.assertEqual(self.conduct.setStartRegister(self.currentDate+timedelta(days=5)),self.currentDate+timedelta(days=5))
        self.assertNotEqual(self.conduct.setStartRegister(self.currentDate+timedelta(days=4)),self.currentDate+timedelta(days=5))

    def testGetEndRegister(self):
        self.assertEqual(self.conduct.getEndRegister(),self.currentDate+timedelta(days=7))
    
    def testSetEndRegister(self):
        self.assertRaises(Exception,self.conduct.setEndRegister,"DBTT project deadline")
        self.assertRaises(Exception,self.conduct.setEndRegister,self.currentDate-timedelta(days=7))
        self.assertRaises(Exception,self.conduct.setEndRegister,self.currentDate+timedelta(days=1))
        self.assertEqual(self.conduct.setEndRegister(self.currentDate+timedelta(days=9)),self.currentDate+timedelta(days=9))
        self.assertNotEqual(self.conduct.setEndRegister(self.currentDate+timedelta(days=8)),self.currentDate+timedelta(days=9))