import unittest
from api.data_access.lms_quiz_attempt import LMSQuizAttempt
import datetime
from datetime import datetime,timedelta
class testLMSQuizAttempt(unittest.TestCase):
    def testGetSectionId(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertEqual(quizAttempt.getSectionID(),1)

    def testSetSectionId(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertRaises(Exception,quizAttempt.setSectionID,"xerox")
        self.assertRaises(Exception,quizAttempt.setSectionID,-9)
        self.assertEqual(quizAttempt.setSectionID(9),9)
    
    def testGetLearnerId(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertEqual(quizAttempt.getLearnerID(),1)
    
    def testSetLearnerId(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertRaises(Exception,quizAttempt.setLearnerID,"expert")
        self.assertRaises(Exception,quizAttempt.setLearnerID,-3)
        self.assertEqual(quizAttempt.setLearnerID(7),7)
    
    def testGetAttemptDate(self):
        currentDate = datetime.now()
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=currentDate,grade=70)
        self.assertEqual(quizAttempt.getAttemptDate(),currentDate)

    def testSetAttemptDate(self):
        currentDate = datetime.now()
        faultyDate = currentDate + timedelta(days=3)
        newDate = currentDate - timedelta(days=3)
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=currentDate,grade=70)
        self.assertRaises(Exception,quizAttempt.setAttemptDate,[2021,5,29])
        self.assertRaises(Exception,quizAttempt.setAttemptDate,faultyDate)
        self.assertEqual(quizAttempt.setAttemptDate(newDate),newDate)
    
    def testGetGrade(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertEqual(quizAttempt.getGrade(),70)
    
    def testSetGrade(self):
        quizAttempt = LMSQuizAttempt(learner_id=1,section_id=1,attempt_date=datetime.now(),grade=70)
        self.assertRaises(Exception,quizAttempt.setGrade,"Confirm pass")
        self.assertRaises(Exception,quizAttempt.setGrade,-80)
        self.assertEqual(quizAttempt.setGrade(90),90)