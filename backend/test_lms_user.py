import unittest
from api.data_access.lms_user import LMSUser

# Author : Yu Quan
class testLMSUser(unittest.TestCase):
    def setUp(self):
        self.user = LMSUser(name = "Craig", email = "craig@lms.com",seniority_level = "Engineer",contact = "81234567")

    def tearDown(self):
        self.user = None

    def testGetName(self):
        self.assertEqual(self.user.getName(),"Craig")
    
    def testSetName(self):
        self.assertRaises(Exception,self.user.setName,["xerox","machine"])
        self.assertRaises(Exception, self.user.setName,"")
        longNameTestCase = "David Beckham" *10
        self.assertRaises(Exception, self.user.setName,longNameTestCase)
        self.assertEqual(self.user.setName("David"),"David")
        self.assertNotEqual(self.user.setName("Emile"),"David")
    
    def testGetEmail(self):
        self.assertEqual(self.user.getEmail(), "craig@lms.com")
    
    def testSetEmail(self):
        self.assertRaises(Exception,self.user.setEmail, 123)
        self.assertRaises(Exception, self.user.setEmail,"")
        self.assertRaises(Exception, self.user.setEmail,"craig")
        self.assertRaises(Exception, self.user.setEmail,"craig,com")
        self.assertRaises(Exception, self.user.setEmail,"craig@gmail")
        longEmailTestCase = "craig@test.com" *10
        self.assertRaises(Exception, self.user.setEmail,longEmailTestCase)
        self.assertEqual(self.user.setEmail("bob@lms.com"),"bob@lms.com")
        self.assertNotEqual(self.user.setEmail("bob@lms.com"),"bukayo@lms.com")

    def testGetSeniorityLevel(self):
        self.assertEqual(self.user.getSeniorityLevel(), "Engineer")
    
    def testSetSeniorityLevel(self):
        self.assertRaises(Exception,self.user.setSeniorityLevel, 986)
        self.assertRaises(Exception, self.user.setSeniorityLevel,"")
        self.assertRaises(Exception, self.user.setSeniorityLevel,"Boss")
        longSeniorityTestCase = "Senior Senior Senior Engineer"
        self.assertRaises(Exception, self.user.setSeniorityLevel,longSeniorityTestCase)
        self.assertEqual(self.user.setSeniorityLevel("Senior Engineer"),"Senior Engineer")
        self.assertNotEqual(self.user.setSeniorityLevel("Engineer"),"Senior Engineer")
    
    def testGetContact(self):
        self.assertEqual(self.user.getContact(), "81234567")
    
    def testSetContact(self):
        self.assertRaises(Exception,self.user.setContact, 99998888)
        self.assertRaises(Exception, self.user.setContact,"")
        longContactTestCase = "+6512345678901234567890"
        self.assertRaises(Exception, self.user.setContact,longContactTestCase)
        self.assertEqual(self.user.setContact("99998888"),"99998888")
        self.assertNotEqual(self.user.setContact("98765432"),"99998888")