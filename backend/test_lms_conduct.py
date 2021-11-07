import unittest
from api.data_access.lms_conduct import LMSConduct
import datetime
from datetime import timedelta,datetime

class testLMSConduct(unittest.TestCase):

    def testGetCourseId(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getCourseId(),1)
    
    def testGetTrainerId(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getTrainerId(),1)
    
    def testGetCapacity(self):
        currentDate= datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getCapacity(),73)
    
    def testSetCapacity(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.setCapacity,-4)
        self.assertRaises(Exception,conduct.setCapacity,0)
        self.assertRaises(Exception,conduct.setCapacity,"bla bla bla")
        self.assertEqual(conduct.setCapacity(28),28)
    
    def testIncrementCapacity(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.incrementCapacity(),74)
        self.assertEqual(conduct.incrementCapacity(),75)
    
    def testDecrementCapacity(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.decrementCapacity(),72)
        conduct.capacity=0
        self.assertRaises(Exception,conduct.decrementCapacity)
    
    def testIncreaseCapacity(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.increaseCapacity,"kahgiuwe aiuwhkjfwkj iuhweiew")
        self.assertEqual(conduct.increaseCapacity(7),80)
    
    def testDecreaseCapacity(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.decreaseCapacity,"abcdefghijklmnop")
        self.assertRaises(Exception,conduct.decreaseCapacity,80)
        self.assertEqual(conduct.decreaseCapacity(65),8)

    def testGetStartDate(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getStartDate(),currentDate+timedelta(days=10))
    
    def testSetStartDate(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.setStartDate,"SPM start date")
        self.assertRaises(Exception,conduct.setStartDate,currentDate-timedelta(days=3))
        self.assertRaises(Exception,conduct.setStartDate,currentDate+timedelta(days=15))
        self.assertEqual(conduct.setStartDate(currentDate+timedelta(days=8)),currentDate+timedelta(days=8))
    
    def testGetEndDate(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getEndDate(),currentDate+timedelta(days=13))

    def testSetEndDate(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.setEndDate,"ESM end date")
        self.assertRaises(Exception,conduct.setEndDate,currentDate-timedelta(days=2))
        self.assertRaises(Exception,conduct.setEndDate,currentDate-timedelta(days=3))
        self.assertEqual(conduct.setEndDate(currentDate+timedelta(days=15)),currentDate+timedelta(days=15))
   
    def testGetStartRegister(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getStartRegister(),currentDate+timedelta(days=3))
    
    def testSetStartRegister(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.setStartRegister,"ESD project deadline")
        self.assertRaises(Exception,conduct.setStartRegister,currentDate-timedelta(days=7))
        self.assertRaises(Exception,conduct.setStartRegister,currentDate+timedelta(days=20))
        self.assertEqual(conduct.setStartRegister(currentDate+timedelta(days=5)),currentDate+timedelta(days=5))

    def testGetEndRegister(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertEqual(conduct.getEndRegister(),currentDate+timedelta(days=7))
    
    def testSetEndRegister(self):
        currentDate = datetime.now()
        conduct = LMSConduct(course_id=1,trainer_id=1,capacity=73,start_date=currentDate+timedelta(days=10),end_date = currentDate+timedelta(days=13), start_register = currentDate+timedelta(days=3),end_register = currentDate+timedelta(days=7))
        self.assertRaises(Exception,conduct.setEndRegister,"DBTT project deadline")
        self.assertRaises(Exception,conduct.setEndRegister,currentDate-timedelta(days=7))
        self.assertRaises(Exception,conduct.setEndRegister,currentDate+timedelta(days=1))
        self.assertEqual(conduct.setEndRegister(currentDate+timedelta(days=9)),currentDate+timedelta(days=9))