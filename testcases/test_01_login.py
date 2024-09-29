import allure
import pytest
import requests
from tools.handle_excel import read_excel
from tools.handle_path import excel_path_xinyangapitesting
from tools.handle_request_api import requests_api
from tools.handle_response_assertion import response_assertion

# read out the data into dictionary format from my excel spreadsheet
all_case = read_excel(excel_path_xinyangapitesting,'login')
# @pytest.mark.p1
@allure.suite('Login Module')
@allure.title('{case[case_details]}')
@pytest.mark.parametrize('case',all_case) #DDT iterate all the cases in all_case value
def test_login_case(case):
    response = requests_api(case)
    print(response)
    expected_result = case['expected_result']
    print(expected_result)
    response_assertion(response,expected_result)

# if __name__ =='__main__':
#     test_login_case(case)