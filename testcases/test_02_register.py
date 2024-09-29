import allure
import pytest
from tools.handle_excel import read_excel
from tools.handle_path import excel_path_xinyangapitesting
from tools.handle_request_api import requests_api
from tools.handle_response_assertion import response_assertion

# step 1 : read from the excel spreadsheet

case_all=read_excel(excel_path_xinyangapitesting,'test_register')
@allure.suite('Account Registeration Module')
@allure.title('{case[case_details]}')
@pytest.mark.parametrize('case',case_all)
def test_register_case(case):
    resp=requests_api(case)
    expected=case['expected_result']
    response_assertion(resp,expected)
