import unittest
from api.data_access.lms_section import LMSSection

class testLMSSection(unittest.TestCase):
    def setUp(self):
        self.section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
    
    def tearDown(self):
        self.sectoin = None
    
    def testGetConductId(self):
        self.assertEqual(self.section.getConductID(),1)

    def testGetSequence(self):
        self.assertEqual(self.section.getSequence(),2)

    def testGetSectionName(self):
        self.assertEqual(self.section.getSectionName(),"Xerox Learners G1")
    
    def testSetSectionName(self):
        self.assertRaises(Exception,self.section.setSectionName,980)
        self.assertRaises(Exception,self.section.setSectionName,"")
        nameMoreThanFifty = "Xerox Experts"*10
        self.assertRaises(Exception,self.section.setSectionName,nameMoreThanFifty)
        self.assertEqual(self.section.setSectionName("Xerox Pros G4"),"Xerox Pros G4")
        self.assertNotEqual(self.section.setSectionName("Xerox Pros G7"),"Xerox Pros G4")
    
    def testGetQuizDuration(self):
        self.assertEqual(self.section.getQuizDuration(),60)

    def testSetQuizDuration(self):
        self.assertRaises(Exception,self.section.setQuizDuration,"xerox copiers are great")
        self.assertRaises(Exception,self.section.setQuizDuration,-90)
        self.assertEqual(self.section.setQuizDuration(45),45)
        self.assertNotEqual(self.section.setQuizDuration(60),45)
    
    def testGetPassingGrade(self):
        self.assertEqual(self.section.getPassingGrade(),50)
    
    def testSetPassingGrade(self):
        self.assertRaises(Exception,self.section.setPassingGrade,[1,2,3,4,5])
        self.assertRaises(Exception,self.section.setPassingGrade,0)
        self.assertEqual(self.section.setPassingGrade(30),30)
        self.assertNotEqual(self.section.setPassingGrade(70),30)