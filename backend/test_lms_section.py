import unittest
from api.data_access.lms_section import LMSSection

class testLMSSection(unittest.TestCase):
    def testGetConductId(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertEqual(section.getConductID(),1)

    def testGetSequence(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertEqual(section.getSequence(),2)

    def testGetSectionName(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertEqual(section.getSectionName(),"Xerox Learners G1")
    
    def testSetSectionName(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertRaises(Exception,section.setSectionName,980)
        self.assertRaises(Exception,section.setSectionName,"")
        nameMoreThanFifty = "Xerox Experts"*10
        self.assertRaises(Exception,section.setSectionName,nameMoreThanFifty)
        self.assertEqual(section.setSectionName("Xerox Pros G4"),"Xerox Pros G4")
    
    def testGetQuizDuration(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertEqual(section.getQuizDuration(),60)

    def testSetQuizDuration(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertRaises(Exception,section.setQuizDuration,"xerox copiers are great")
        self.assertRaises(Exception,section.setQuizDuration,-90)
        self.assertEqual(section.setQuizDuration(45),45)
    
    def testGetPassingGrade(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertEqual(section.getPassingGrade(),50)
    
    def testSetPassingGrade(self):
        section = LMSSection(conduct_id = 1,sequence = 2,section_name = "Xerox Learners G1",quiz_duration = 60,passing_grade = 50)
        self.assertRaises(Exception,section.setPassingGrade,[1,2,3,4,5])
        self.assertRaises(Exception,section.setPassingGrade,0)
        self.assertEqual(section.setPassingGrade(30),30)