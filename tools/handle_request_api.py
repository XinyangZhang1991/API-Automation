
import json
import requests
from loguru import logger
from tools.handle_path import file_path
from tools.handle_replacement import replace_data
from tools.handle_extraction import data_extraction
from tools.handle_presql import pre_sql

def requests_api(case,token=None):
    method = case['request_method']
    url=case['url']
    header=case['request_header']
    param=case['request_parameter']
    presql = case['pre_sql']
    presql=replace_data(presql)
    pre_sql(presql)
    header=replace_data(header)
    param=replace_data(param)

    if header is not None:
        header = json.loads(header)
        if token is not None:
            header["authoriazation"]=token
    if param is not None:
        param =json.loads(param)

    if method.lower() == 'get':
        resp =requests.request(method=method,url=url,headers=header,params=param)
    elif method.lower() == 'post':
        if header["Content-Type"] == "application/json":
            resp = requests.request(method=method,url=url,headers=header,json=param)
        if header['Content-Type'] == "application/x-www-form-urlencoded":
            resp =requests.request(method=method,url=url,headers=header,data=param)
        if header['Content-Type'] == 'multipart/form-data':
            header.pop('Content-Type') # needs to delete content-type data field
            filename = param['filename']
            file_obj = {'file':open(file_path/filename,'rb')}
            resp =requests.request(method=method,url=url,header=header, files=file_obj)
    elif method.lower() =='put':
        resp=requests.request(method=method,url=url,headers=header,json=param)
    logger.info('---response message------')
    logger.info(f'response status code:{resp.status_code}')
    logger.info(f'response body: {resp.text}')
    data_extraction(resp,case['response_extraction'])
    return resp


if __name__ =='__main__':
    case={'test_case': 1, 'case_details': 'Send registration SMS verification code', 'request_method': 'PUT',
     'url': 'http://shop.lemonban.com:8107/user/sendRegisterSms',
     'request_header': '{ "Content-Type": "application/json; charset=UTF-8"}',
     'request_parameter': '{"mobile":"#gen_unregister_phone()#"}', 'expected_result': None, 'response_extraction': None,
     'pre_sql': None, 'database_assertion': None}
    requests_api(case, token=None)

    case_2= {'test_case': 2, 'case_details': 'press next step to verify registration SMS verification code', 'request_method': 'PUT', 'url': 'http://shop.lemonban.com:8107/user/checkRegisterSms', 'request_header': '{"Content-Type": "application/json; charset=UTF-8"}', 'request_parameter': '{"mobile":"#gen_unregister_phone#","validCode":"#mobile_code#"}', 'expected_result': None, 'response_extraction': '{"check_code":"text"}', 'pre_sql': '{"mobile_code":\n"select mobile_code  from tz_sms_log where user_phone=\'#gen_unregister_phone#\' order by rec_date desc limit 1;"}', 'database_assertion': None}
    requests_api(case_2, token=None)