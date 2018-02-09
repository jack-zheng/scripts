import requests
from requests.auth import HTTPBasicAuth
import re
import logging

# define the regex to fetch case id from class name
regx = r"PLT\d+"
# define the status which means pass
pass_list = ['PASSED', 'FIXED']
# define a list to store test result, run_result[test01{name, status}, test02{name, status}]
xml_list = []

url = 'http://10.129.126.245:9090/job/qaautocand_tomcat_hana_qrayrun/124/testReport/api/json?pretty=true'
authorize = HTTPBasicAuth('upadmin', 'Initial1')
ret = requests.get(url, auth=authorize)
suites = ret.json()['suites']



# parse case name and case status
# there are three kinds of status: PASS and FIXED means pass and FAILED means failed
for test in suites:
    regx_ret = re.findall(regx, test['name'])
    if not regx_ret:
        case_name = test['name'].split('.')[-1]
        logging.warn('test case: %s not start with "PLT", skipped' % case_name)
        continue
    test_name = regx_ret[0]
    test_status = True
    cases = test['cases']
    
    # check the show out when there are multiple @Test method in on test case
    for case in cases:
        is_pass = case['status'] in pass_list
        test_status = test_status & is_pass

    xml_list.append({test_name:test_status})

    # xml generator: generateTestlinkReport(list, file_name) => result.xml
