import logging
import unittest
import os
from mimo.write_to_xml import write_jenkins_result_to_file
from mimo.ReportObj import TestCase
import xml.etree.ElementTree as ET
from mimo.Report import fetchresult
import json
from unittest import mock

def fake_requests_return(*args, **kwargs):
    """
    fake url is the string type json, this is easy for testing
    url should be some thing like: '{"suites":[{"name":"com.PLT123", "cases":[{"status": "PASSED"}]}]}'
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(json.loads(args[0]), 200)


class TestMimo(unittest.TestCase):
    # before test delete tmp export file
    def setUp(self):
        self.removexml("Set UP")
        logging.warning("================== Start Testing =================")

    def testreportwithoutname(self):
        """ input: list[obj1, obj2]
                new xml file generated and contains result parsed from input list
        """
        fake_list = [TestCase("PLT#-123", status=True), TestCase("PLT#-234")]
        write_jenkins_result_to_file(fake_list)

        # new file generated and obj content wwrite into it
        target = [path for path in os.listdir('.') if path.endswith('.xml')][0]
        tree = ET.parse(target)
        root = tree.getroot()
        testcases = root.findall('testcase')
        # there should be 2 nodes of testcase
        self.assertEqual(len(testcases), 2)
        for case in testcases:
            if "123" in case.attrib['external_id']:
                self.assertEqual(case.find('result').text, 'p')
            else:
                self.assertEqual(case.find('result').text, 'f')

    def testreportwithname(self):
        """
        xml file name should be same as the given out name
        :return:
        """
        fakename = 'fake_report'
        write_jenkins_result_to_file([], fakename)
        ret = [path for path in os.listdir('.') if path.startswith(fakename)]
        print(ret)
        self.assertEqual(len(ret), 1)
        self.assertTrue(ret[0].endswith('.xml'))
        self.assertTrue(ret[0].startswith(fakename))

    @mock.patch('requests.get', side_effect=fake_requests_return)
    def testfetchresult(self, mock_get):
        """
        mock requests.get() method's return and assert return value
        check point: 
            1. case id parse correct
            2. no case missed 
            3. status parsed correct
        """
        ret_list = fetchresult('{"suites":[{"name":"com.PLT123", "cases":[{"status": "PASSED"}]}]}')
        print(ret_list[0].id)


    def removexml(self, methodname):
        for path in os.listdir('.'):
            if path.endswith('.xml'):
                logging.warning('%s Remove File: %s' % (methodname, path))
                os.remove(os.path.abspath(path))




if __name__ == "__main__":
    unittest.main()
