import unittest
from api.data_access.lms_user import LMSUser

class testLMSUser(unittest.TestCase):
    def testGetName(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertEqual(user.getName(),"Craig")
    
    def testSetName(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertRaises(Exception,user.setName,["xerox","machine"])
        self.assertRaises(Exception, user.setName,"")
        longNameTestCase = "David Beckham" *10
        self.assertRaises(Exception, user.setName,longNameTestCase)
        self.assertEqual(user.setName("David"),"David")
    
    def testGetEmail(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertEqual(user.getEmail(), "craig@lms.com")
    
    def testSetEmail(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertRaises(Exception,user.setEmail, 123)
        self.assertRaises(Exception, user.setEmail,"")
        longEmailTestCase = "craig@test.com" *10
        self.assertRaises(Exception, user.setEmail,longEmailTestCase)
        self.assertEqual(user.setEmail("bob@lms.com"),"bob@lms.com")

    def testGetSeniorityLevel(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertEqual(user.getSeniorityLevel(), "Engineer")
    
    def testSetSeniorityLevel(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertRaises(Exception,user.setSeniorityLevel, 986)
        self.assertRaises(Exception, user.setSeniorityLevel,"")
        longSeniorityTestCase = "Senior Senior Senior Engineer"
        self.assertRaises(Exception, user.setSeniorityLevel,longSeniorityTestCase)
        self.assertEqual(user.setSeniorityLevel("Senior Engineer"),"Senior Engineer")
    
    def testGetContact(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertEqual(user.getContact(), "81234567")
    
    def testSetContact(self):
        user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")
        self.assertRaises(Exception,user.setContact, 99998888)
        self.assertRaises(Exception, user.setContact,"")
        longContactTestCase = "+6512345678901234567890"
        self.assertRaises(Exception, user.setContact,longContactTestCase)
        self.assertEqual(user.setSeniorityLevel("99998888"),"99998888")