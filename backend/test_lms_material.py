import unittest
from api.data_access.lms_material import LMSMaterial

class testLMSMaterial(unittest.TestCase):
    def testGetSectionID(self):
        material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
        self.assertEqual(material.getSectionID(),1)
    
    def testGetFileName(self):
        material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
        self.assertEqual(material.getFileName(),"Fixing Xerox 101.pdf")
    
    def testSetFileName(self):
        material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
        reallyLongString = "abcdefghijk" * 10
        self.assertRaises(Exception,material.setFileName,"")
        self.assertRaises(Exception,material.setFileName,reallyLongString)
        self.assertEqual(material.setFileName("Replacing ink catridge.docx"),"Replacing ink catridge.docx")

    def testGetLink(self):
        material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
        self.assertEqual(material.getLink(),"https://www.aws.s3.fixing&xerox&101.com")
    
    def testSetLink(self):
        material = LMSMaterial(section_id = 1,file_name = "Fixing Xerox 101.pdf" , link = "https://www.aws.s3.fixing&xerox&101.com")
        reallyLongString = "https://www.google.com" * 23
        self.assertRaises(Exception,material.setFileName,"")
        self.assertRaises(Exception,material.setFileName,reallyLongString)
        self.assertEqual(material.setFileName("https://www.youtube.com?file=learning&video"),"https://www.youtube.com?file=learning&video")
    