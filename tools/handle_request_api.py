
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
    response_extraction_in_excel = case['response_extraction']
    presql = case['pre_sql']
    # Handle data replacements and pre-SQL execution
    if presql is not None:
        presql=replace_data(presql)
        pre_sql(presql)

    header = replace_data(header)
    logger.info(f"Header after replacement: {header}")
    param=replace_data(param)
    logger.info(f"parameter after replacement is: {param}")

    if header is None:  # Ensure that `header` is a dictionary, even if None initially
        header={}
    else:
        try:
            header = json.loads(header)
        except json.JSONDecodeError as e:
            logger.error(f'Header JSON decode error:{e}')
            logger.error(f"Received header: {header}")
            return
        # Ensure token is added to the header if available
        if token is not None:
            header["authorization"]=token



    if param is not None:

        try:
            param =json.loads(param)
        except json.JSONDecodeError as e:
            logger.error(f'Header JSON decode error:{e}')
            return

    # Log the final request details for debugging
    logger.info(f"URL: {url}")
    logger.info(f"Method: {method}")
    logger.info(f"Headers: {header}")
    logger.info(f"Params: {param}")


    # Initialize response variable
    resp=None
    # Make the HTTP request
    try:
        if method.lower() == 'get':
            resp =requests.request(method=method,url=url,headers=header,params=param)
        elif method.lower() == 'post':
            if header.get("Content-Type") == "application/json":
                resp = requests.request(method=method,url=url,headers=header,json=param)
            elif header.get('Content-Type') == "application/x-www-form-urlencoded":
                resp = requests.request(method=method,url=url,headers=header,data=param)
            elif header.get('Content-Type')== 'multipart/form-data':
                header.pop('Content-Type') # needs to delete content-type data field
                filename = param.get('filename')
                file_obj = {'file':open(file_path/filename,'rb')}
                resp =requests.request(method=method,url=url,headers=header, files=file_obj)
        elif method.lower() =='put':
            resp=requests.request(method=method,url=url,headers=header,json=param)
            print(f'put method response is {resp}')

        if resp is None:
            logger.error("The response object is None after the request")
# f there are issues related to the network, they are caught with requests.RequestException and logged.

    except requests.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return
    except requests.Timeout as e:
        logger.error(f"Timeout error: {e}")
        return
    except requests.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return


    if resp is not None:
        logger.info('---response message------')
        logger.info(f'response status code:{resp.status_code}')
        logger.info(f'response body: {resp.text}')
        # Handle non-JSON responses
        try:
            response_data = resp.json()  # Try to parse as JSON
        except requests.JSONDecodeError:
            response_data = resp.text  # If not JSON, treat it as plain text
            print(response_data)

        data_extraction(resp,response_extraction_in_excel)
        logger.info(f'data  in response_extraction column of the excel sheet is {response_extraction_in_excel} ')
    else:
        logger.error('Response is None; no request was made')
    return resp


if __name__ =='__main__':

    # # busniessflow1
    # case_1={'test_case': 1, 'case_details': 'login sucessful ', 'request_method': 'post', 'url': 'http://shop.lemonban.com:8107/login', 'request_header': '{"Content-Type":"application/json"}', 'request_parameter': '{"principal":"lemon_py","credentials":"12345678","appType":3,"loginType":0}', 'expected_result': '{"nickName": "lemon_py","enabled": true}', 'response_extraction': '{"access_token":"$..access_token","token_type":"$..token_type"}', 'database_assertion': None, 'pre_sql': None}
    # requests_api(case_1, token=None)
    # # busniessflow2
    # case_2 = {'test_case': 2, 'case_details': 'search for a product ', 'request_method': 'get',
    #           'url': 'http://shop.lemonban.com:8107/search/searchProdPage', 'request_header': None,
    #           'request_parameter': '{"prodName":"真皮圆筒包"}', 'expected_result': None,
    #            'response_extraction': '{"prodId":"$..prodId"}', 'database_assertion': None, 'pre_sql': None}
    # requests_api(case_2, token=None)
    # case_3= {'test_case': 3, 'case_details': 'go to the specific product prage ', 'request_method': 'get',
    #           'url': 'http://shop.lemonban.com:8107/prod/prodInfo', 'request_header': None,
    #            'request_parameter': '{"prodId":"#prodId#"}', 'expected_result': None, 'response_extraction': '{"skuId":"$..skuId"}',
    #             'database_assertion': None, 'pre_sql': None}
    # requests_api(case_3, token=None)
    #
    # case_4={'test_case': 4, 'case_details': 'adding into the trolley', 'request_method': 'post', 'url': 'http://shop.lemonban.com:8107/p/shopCart/changeItem', 'request_header': '{"Content-Type":"application/json","Authorization": "#token_type##access_token#"}', 'request_parameter': '{"basketId": 0, "count": 1, "prodId": "#prodId#", "shopId": 1, "skuId": "#skuId#"}', 'expected_result': None, 'response_extraction': None, 'database_assertion': None, 'pre_sql': None}
    # requests_api(case_4, token=None)
    # case_5={'test_case': 5, 'case_details': 'search trolley list ', 'request_method': 'post', 'url': 'http://shop.lemonban.com:8107/p/shopCart/info', 'request_header': '{"Content-Type":"application/json","Authorization": "#token_type##access_token#"}', 'request_parameter': '{}', 'expected_result': None, 'response_extraction': '{"basketId":"$..basketId"}', 'database_assertion': None, 'pre_sql': None}
    # requests_api(case_5, token=None)
    # # case_6={'test_case': 6, 'case_details': 'tick the product ', 'request_method': 'POST', 'url': '\thttp://shop.lemonban.com:8107/p/shopCart/totalPay', 'request_header': '{"Content-Type":"application/json","Authorization": "#token_type##access_token#"}', 'request_parameter': None, 'expected_result': None, 'response_extraction': None, 'database_assertion': None, 'pre_sql': None}
    # # requests_api(case_6, token=None)
    # # case_7={'test_case': 7, 'case_details': 'confirm the order', 'request_method': 'POST', 'url': 'http://shop.lemonban.com:8107/p/order/confirm', 'request_header': '{"Content-Type":"application/json","Authorization": "#token_type##access_token#"}', 'request_parameter': '{"addrId": 0, "basketIds": "[#basketId#]", "couponIds": [], "isScorePay": 0, "userChangeCoupon": 0,       "userUseScore": 0}', 'expected_result': None, 'response_extraction': None, 'database_assertion': None, 'pre_sql': None}
    # # requests_api(case_7, token=None)
    # # case_8={'test_case': 8, 'case_details': 'submit the order', 'request_method': 'post', 'url': 'http://shop.lemonban.com:8107/p/order/submit', 'request_header': '{"Content-Type":"application/json","Authorization": "#token_type##access_token#"}', 'request_parameter': '{"orderShopParam": [{"remarks": "", "shopId": 1}]}', 'expected_result': '{"$..duplicateError":null}', 'response_extraction': '{"orderNumbers":"$..orderNumbers"}', 'database_assertion': '"{""select count(*) from tz_order where order_number = \'#orderNumbers#\'"":1, \n""select status from tz_order where order_number = \'#orderNumbers#\'"":1}"', 'pre_sql': None}
    # # requests_api(case_8, token=None)
    #


    # login_testcase1 ={'test_case': 'login_001', 'case_details': 'Login_in_sucessful', 'request_method': 'post',
    #  'url': 'http://shop.lemonban.com:8107/login', 'request_header': '{"Content-Type":"application/json"}',
    #  'request_parameter': '{"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType": 0}',
    #  'expected_result': '{"$..nickName":"lemon_py","$..enabled":true}', 'response_extraction': None,
    #  'database_assertion': None, 'pre_sql': None}
    #
    # requests_api(login_testcase1, token=None)


    # case_2= {'test_case': 2, 'case_details': 'press next step to verify registration SMS verification code', 'request_method': 'PUT', 'url': 'http://shop.lemonban.com:8107/user/checkRegisterSms', 'request_header': '{"Content-Type": "application/json; charset=UTF-8"}', 'request_parameter': '{"mobile":"#gen_unregister_phone#","validCode":"#mobile_code#"}', 'expected_result': None, 'response_extraction': '{"check_code":"text"}', 'pre_sql': '{"mobile_code":\n"select mobile_code  from tz_sms_log where user_phone=\'#gen_unregister_phone#\' order by rec_date desc limit 1;"}', 'database_assertion': None}
    #
    # requests_api(case_2, token=None)

    login_case = {'test_case': 'login_002', 'case_details': 'Login_in_fail', 'request_method': 'post',
     'url': 'http://shop.lemonban.com:8107/login', 'request_header': '{"Content-Type":"application/json"}',
     'request_parameter': '{"principal": "", "credentials": "lemon123456", "appType": 3, "loginType": 0}',
     'expected_result': '{"text":"账号或密码不正确"}', 'response_extraction': None, 'database_assertion': None,
     'pre_sql': None}

    login_case_3 = {'test_case': 'login_003', 'case_details': 'Login_in_fail (usename<4letters)', 'request_method': 'post',
     'url': 'http://shop.lemonban.com:8107/login', 'request_header': '{"Content-Type":"application/json;charset=UTF-8"}',
     'request_parameter': '{"principal": "lem", "credentials": "lemon123456", "appType": 3, "loginType": 0}',
     'expected_result': '{"text":"账号或密码不正确"}', 'response_extraction': None, 'database_assertion': None,
     'pre_sql': None}

    requests_api(login_case_3, token=None)
