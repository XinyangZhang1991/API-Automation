
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

        data_extraction(response_data,response_extraction_in_excel)
        logger.info(f'data  in response_extraction column of the excel sheet is {response_extraction_in_excel} ')
    else:
        logger.error('Response is None; no request was made')
    return resp


if __name__ =='__main__':

    # busniessflow1
    # case_3={'test_case': 1, 'case_details': 'login sucessful ', 'request_method': 'post', 'url': 'http://shop.lemonban.com:8107/login', 'request_header': '{"Content-Type":"application/json"}', 'request_parameter': '{"principal":"lemon_py","credentials":"12345678","appType":3,"loginType":0}', 'expected_result': '{"nickName": "lemon_py","enabled": true}', 'response_extraction': '{"access_token":"$..access_token","token_type":"$..token_type"}', 'database_assertion': None, 'pre_sql': None}
    # requests_api(case_3, token=None)
    # busniessflow2
    case_4 = {'test_case': 2, 'case_details': 'search for a product ', 'request_method': 'get',
              'url': 'http://shop.lemonban.com:8107/search/searchProdPage', 'request_header': None,
              'request_parameter': '{"prodName":"真皮圆筒包"}', 'expected_result': None,
               'response_extraction': '{"prodId":"$..prodId"}', 'database_assertion': None, 'pre_sql': None}
    requests_api(case_4, token=None)
    case_5 = {'test_case': 3, 'case_details': 'go to the specific product prage ', 'request_method': 'get',
              'url': 'http://shop.lemonban.com:8107/prod/prodInfo', 'request_header': None,
               'request_parameter': '{"prodId":"#prodId#"}', 'expected_result': None, 'response_extraction': '{"skuId":"$..skuId"}',
                'database_assertion': None, 'pre_sql': None}
    requests_api(case_5, token=None)
