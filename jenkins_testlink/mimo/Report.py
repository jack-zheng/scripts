import requests
from requests.auth import HTTPBasicAuth
import re
import logging
from .write_to_xml import write_jenkins_result_to_file
from .ReportObj import TestCase

# define case id prefix
id_prefix = "PLT"
# define the regex to fetch case id from class name
regx = r"PLT\d+"
# define the status which means pass
pass_list = ['PASSED', 'FIXED']
# define a list to store test result, run_result[test01{name, status, count}]
xml_list = []
# define defaule domain of Jenkins server
domain = "http://10.129.126.245:9090/job/jobname/start/testReport/api/json?pretty=true"
# define default auth username and password
auth_info = ['upadmin', 'Initial1']

def exportxml(jobname, start, end=-1):
    # if end num bigger then start, we calculate multiple times and get intersection
    if end < start:
        end = start
    else:
        logging.warn("Calculate Intersection")
        
    while (start <= end ):
       url = domain.replace("jobname", jobname).replace("start", str(start))
       tmp_list = fetchresult(url)
       for sub in tmp_list:
           if sub in 
       start = start + 1

    # xml generator: generateTestlinkReport(list, file_name) => result.xml
    write_jenkins_result_to_file(xml_list)


"""ecapsulate method to fetch result
"""
def fetchresult(url):
    logging.warn("request url: %s" %url)
    authorize = HTTPBasicAuth(auth_info[0], auth_info[1])
    ret = requests.get(url, auth=authorize)
    suites = ret.json()['suites']
        
    # parse case name and case status
    # there are three kinds of status: PASS and FIXED means pass and FAILED means failed
    ret_list = []
    for test in suites:
        # parse case id, finally we get some id like: PLT#-XXX
        regx_ret = re.findall(regx, test['name'])
        if not regx_ret:
            case_name = test['name'].split('.')[-1]
            logging.warn('test case: %s not start with "%s", skipped' % (case_name, id_prefix))
            continue
        test_name = regx_ret[0].replace(id_prefix, (id_prefix + "#-"))
        test_status = True
        cases = test['cases']
        
        # check the show out when there are multiple @Test method in on test case
        for case in cases:
            is_pass = case['status'] in pass_list
            test_status = test_status & is_pass

        ret_list.append(TestCase(test_name, status=test_status))
    return ret_list
