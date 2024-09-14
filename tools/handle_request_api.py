
import json
import requests
from loguru import logger
from tools.handle_path import file_path
from tools.handle_replacement import replace_data
from tools.handle_extraction import data_extraction

def requests_api(case,token=None):
    method = case['request_method']
    url=case['url']
    header=case['request_header']
    param=case['request_parameter']
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
        pass
    logger.info('---response message------')
    logger.info(f'response status code:{resp.status_code}')
    logger.info(f'response body: {resp.text}')
    data_extraction(resp,case['response_extraction'])
    return resp