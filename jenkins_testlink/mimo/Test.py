import logging
import unittest
import os
from write_to_xml import write_jenkins_result_to_file
from ReportObj import TestCase
import xml.etree.ElementTree as ET

class TestMimo(unittest.TestCase):
	# before test delete tmp export file
	def setUp(self):
		self.removexml("Set UP")
		logging.warning("================== Start Testing =================")

	""" input: list[obj1, obj2]
		new xml file generated and contains result parsed from input list
	"""
	def testReportWithoutName(self):
		fake_list = [TestCase("PLT#-123", status=True), TestCase("PLT#-234")]
		write_jenkins_result_to_file(fake_list)

		# new file generated and obj content wwrite into it
		target = [path for path in os.listdir('.') if path.endswith('.xml')][0]
		tree = ET.parse(target)
		root = tree.getroot()
		testcases = root.findall('testcase')
		# there should be 2 nodes of testcase 
		self.assertEqual(len(testcases), 2)
		for case in testcases :
			if "123" in case.attrib['external_id'] :
				self.assertEqual(case.find('result').text, 'p')
			else: 
				self.assertEqual(case.find('result').text, 'f')


	''' xml file name should be same as the given out name
	'''
	def testReportWithName(self):
			fakename = 'fake_report'
			write_jenkins_result_to_file([], fakename)
			ret = [path for path in os.listdir('.') if path.startswith(fakename)]
			print(ret)
			self.assertEqual(len(ret), 1)
			self.assertTrue(ret[0].endswith('.xml'))
			self.assertTrue(ret[0].startswith(fakename))


	#@classmethod
	#def tearDownClass(cls):
	#	cls.removexml("Class Tear Down")

	def removexml(self, methodname):
		for path in os.listdir('.'):
			if path.endswith('.xml'):
				logging.warning('%s Remove File: %s' %(methodname, path))
				os.remove(os.path.abspath(path))
		
if __name__ == "__main__":
	unittest.main()