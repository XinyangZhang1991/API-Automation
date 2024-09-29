import allure
import pytest
from tools.handle_excel import read_excel
from tools.handle_path import excel_path_xinyangapitesting
from tools.handle_request_api import requests_api
from tools.handle_response_assertion import response_assertion


case_all=read_excel(excel_path_xinyangapitesting,'test_business_flow')
first_case = case_all[:1]
second_case= case_all[:2]
third_case= case_all[:3]
fourth_case= case_all[:4]
fifth_case= case_all[:5]


@allure.suite('Order Submission Module - a Business Flow')
@allure.title('{case[case_details]}')
@pytest.mark.parametrize('case',case_all)
# @pytest.mark.parametrize('case',case_all,ids=[f"case_{i}" for i in range(len(case_all))])
def test_business_workflow(case):
    resp=requests_api(case)
    expected=case['expected_result']
    response_assertion(resp,expected)


