import json
from jsonpath import jsonpath
from data.Environmental_Data import EnviromentalData
from loguru import logger


def data_extraction(api_response,response_extraction):
    if response_extraction is None:
        logger.info('no data extraction')
        return # this return terminates this function at this point, none of the subsequent code is executed
    logger.info('-------data extraction start--------')
    response_extraction = json.loads(response_extraction)
    logger.info(f'data has been extracted in this round is {response_extraction}')
    # Iterate over the key-value pairs in the dictionary
    for key,value in response_extraction.items():
        # extract teh value from api_response using jsonpath
        value_to_save=jsonpath(api_response.json(),value)[0]
        # set the attribute in EnvironmentalData class
        setattr(EnviromentalData,key,value_to_save)
    logger.info(f'data has been saved into the environmental files attribute is {EnviromentalData.__dict__}')

if __name__ == '__main__':
    response = {"access_token": "0efdce50-0e2f-4ed0-b4d1-944be5ab518a",
                "token_type": "bearer", "refresh_token": "4bfc3638-e7e4-4844-a83d-c0f8340bc146",
                "expires_in": 1295999,
                "pic": "http://mall.lemonban.com:8108/2023/09/b5a479b28d514aa59dfa55422b23a6f0.jpg",
                "userId": "46189bfd628e4a738f639017f1d9225d", "nickName": "lemon_auto", "enabled": True}
    extract_data = '{"access_token":"$..access_token","token_type":"$..token_type"}'
    data_extraction(response, extract_data)


