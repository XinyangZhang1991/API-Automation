import pytest
from tools.handle_excel import read_excel
from tools.handle_path import excel_path_xinyangapitesting
from tools.handle_request_api import requests_api
from tools.handle_response_assert import response_assertion


case_all=read_excel(excel_path_xinyangapitesting,'test_business_flow')


@pytest.mark.parametrize('case',all_case)
def test_business_workflow(case):
    resp=requests_api(case)
    expected=case['expected_result']
    response_assertion(resp,expected)
