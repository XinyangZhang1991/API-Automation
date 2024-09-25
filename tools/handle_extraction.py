import json
from jsonpath import jsonpath
from data.Environmental_Data import EnviromentalData
from loguru import logger
import requests


def data_extraction(api_response,response_extraction_in_excel):
    if response_extraction_in_excel is None:
        logger.info('no data extraction')
        return # this return terminates this function at this point, none of the subsequent code is executed
    #
    # logger.info('-------data extraction start--------')
    # # check if api_response is a requests.Response,try to convert it to Json
    # if isinstance(api_response, requests.Response):
    #     try:
    #         api_response = api_response.json()  # Convert response to JSON if it's a Response object
    #         logger.info(f'api response is {api_response}')
    #     except requests.JSONDecodeError as e :
    #         logger.error("Failed to parse response as JSON")
    #         return None  # Handle the error appropriately
    # # Check if api_response is a string, attempt to parse it as JSON
    # if isinstance(api_response, str):
    #     try:
    #         api_response = json.loads(api_response)
    #     except json.JSONDecodeError as e:
    #         logger.error(f"Response is not a valid JSON string:{e}")
    #         return
    # # If the response is still not a dict at this point, log an error
    # if not isinstance (api_response,dict):
    #     logger.error('API response is not a valid dictionary or JSON')
    #     return
    #
    # # response_extraction_in_excel = what is written in the excel sheet
    # # Parse response_extraction if it is a string (assumed to be in JSON format)
    try:
        response_extraction_in_excel = json.loads(response_extraction_in_excel)
        logger.info(f'data has been extracted from excelsheet is {response_extraction_in_excel}')
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse response_extraction as JSON: {e}")
        return

    if isinstance(response_extraction_in_excel, dict):
      # Iterate over the key-value pairs in the dictionary
        for key,value in response_extraction_in_excel.items():
            try:
                # extract teh value from api_response using jsonpath
                value_to_save=jsonpath(api_response, value)[0]
                logger.info(f'data found from API response is {value_to_save}')
                # set the attribute in EnvironmentalData class
                setattr(EnviromentalData,key,value_to_save)
                logger.info(f'data has been saved into the environmental files attribute is {EnviromentalData.__dict__}')
            except Exception as e:
                logger.error(f"Error extracting data for {key}: {e}")
    else:
        logger.error("Invalid response_extraction format; must be a dictionary")


if __name__ == '__main__':
    response = {"access_token": "0efdce50-0e2f-4ed0-b4d1-944be5ab518a",
                "token_type": "bearer", "refresh_token": "4bfc3638-e7e4-4844-a83d-c0f8340bc146",
                "expires_in": 1295999,
                "pic": "http://mall.lemonban.com:8108/2023/09/b5a479b28d514aa59dfa55422b23a6f0.jpg",
                "userId": "46189bfd628e4a738f639017f1d9225d", "nickName": "lemon_auto", "enabled": True}
    extract_data = '{"access_token":"$..access_token","token_type":"$..token_type"}'
    data_extraction(response, extract_data)


