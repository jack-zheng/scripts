import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom
import logging

"""input:
   result list, contains test id and test result
       list[
               {
                   "id": "PLT#-XXX",
                   "status": False/True
               }
           ]
    file name, defualt file name is 'mimo_jenkins_testlink_timestamp'
"""   
def write_jenkins_result_to_file(ret_list, file_name='mimo_jenkins_testlink_'):
    ret_parse = parse_result_list(ret_list)
    ret_format = (prettify(ret_parse))
    timestamp = datetime.now().strftime('%m_%d_%H%M%S')
    file_name = file_name + timestamp + '.xml'
    with open(file_name, 'w') as f:
        f.write(ret_format)
    logging.warn("------------------- Finish Export -------------------")

"""parse result list and return xml element object
"""
def parse_result_list(ret_list):
    # parse list result and write them into xml element
    results = ET.Element('results')
    # for loop and write test case
    for sub in ret_list:
        test = ET.SubElement(results, 'testcase')
        test.set('external_id', sub["id"])
        # set result node
        result = ET.SubElement(test, 'result')
        result.text = 'p' if sub["status"] else 'f'
        # set notes node
        nodes = ET.SubElement(test, 'nodes')
    logging.warn("------------------- Finish Parse -------------------")
    return results
    
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == '__main__':
    write_jenkins_result_to_file([{"id":"PLT#-123", "status":True},\
                                  {"id":"PLT#-456", "status":False}])
