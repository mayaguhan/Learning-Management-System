import unittest
from api.data_access.lms_material import LMSMaterial

# Author : Craig
class testLMSMaterial(unittest.TestCase):
    def setUp(self):
        self.material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
    
    def tearDown(self):
        self.material = None
        
    def testGetSectionID(self):
        self.assertEqual(self.material.getSectionID(),1)
    
    def testGetFileName(self):
        self.assertEqual(self.material.getFileName(),"Fixing Xerox 101.pdf")
    
    def testSetFileName(self):
        reallyLongString = "abcdefghijk" * 10
        self.assertRaises(Exception,self.material.setFileName,"")
        self.assertRaises(Exception,self.material.setFileName,reallyLongString)
        self.assertRaises(Exception,self.material.setFileName,[reallyLongString,"abcdefghijklmnop"])
        self.assertRaises(Exception,self.material.setFileName,987345)
        self.assertEqual(self.material.setFileName("Replacing ink catridge.docx"),"Replacing ink catridge.docx")
        self.assertNotEqual(self.material.setFileName("Replacing ink holder.docx"),"Replacing ink catridge.docx")

    def testGetLink(self):
        self.assertEqual(self.material.getLink(),"https://www.aws.s3.fixing&xerox&101.com")
    
    def testSetLink(self):
        reallyLongString = "https://www.google.com" * 23
        self.assertRaises(Exception,self.material.setFileName,"")
        self.assertRaises(Exception,self.material.setFileName,reallyLongString)
        self.assertRaises(Exception,self.material.setFileName,[reallyLongString, 975172])
        self.assertRaises(Exception,self.material.setFileName,{"link" : "youtube.com"})
        self.assertEqual(self.material.setFileName("https://www.youtube.com?file=learning&video"),"https://www.youtube.com?file=learning&video")
        self.assertNotEqual(self.material.setFileName("https://www.youtube.com?file=testing&video"),"https://www.youtube.com?file=learning&video")