import unittest
from api.data_access.lms_quiz_attempt import LMSQuizAttempt
import datetime
from datetime import datetime,timedelta

# Author : Shobana
class testLMSQuizAttempt(unittest.TestCase):
    def setUp(self):
        self.currentDate = datetime.now()
        self.quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=self.currentDate,grade=70)
    
    def tearDown(self):
        self.currentDate = None
        self.quizAttempt = None 

    def testGetSectionId(self):
        self.assertEqual(self.quizAttempt.getSectionID(),1)

    def testSetSectionId(self):
        self.assertRaises(Exception,self.quizAttempt.setSectionID,"xerox")
        self.assertRaises(Exception,self.quizAttempt.setSectionID,-9)
        self.assertEqual(self.quizAttempt.setSectionID(9),9)
        self.assertNotEqual(self.quizAttempt.setSectionID(45),9)
    
    def testGetLearnerId(self):
        self.assertEqual(self.quizAttempt.getLearnerID(),1)
    
    def testSetLearnerId(self):
        self.assertRaises(Exception,self.quizAttempt.setLearnerID,"expert")
        self.assertRaises(Exception,self.quizAttempt.setLearnerID,-3)
        self.assertEqual(self.quizAttempt.setLearnerID(7),7)
        self.assertNotEqual(self.quizAttempt.setLearnerID(10),7)
    
    def testGetAttemptDate(self):
        self.assertEqual(self.quizAttempt.getAttemptDate(),self.currentDate)

    def testSetAttemptDate(self):
        faultyDate = self.currentDate + timedelta(days=3)
        newDate = self.currentDate - timedelta(days=3)
        self.assertRaises(Exception,self.quizAttempt.setAttemptDate,[2021,5,29])
        self.assertRaises(Exception,self.quizAttempt.setAttemptDate,faultyDate)
        self.assertEqual(self.quizAttempt.setAttemptDate(newDate),newDate)
        self.assertNotEqual(self.quizAttempt.setAttemptDate(self.currentDate-timedelta(days=2)),newDate)
    
    def testGetGrade(self):
        self.assertEqual(self.quizAttempt.getGrade(),70)
    
    def testSetGrade(self):
        self.assertRaises(Exception,self.quizAttempt.setGrade,"Confirm pass")
        self.assertRaises(Exception,self.quizAttempt.setGrade,-80)
        self.assertEqual(self.quizAttempt.setGrade(90),90)
        self.assertNotEqual(self.quizAttempt.setGrade(70),90)