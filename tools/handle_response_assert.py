import json
from jsonpath import jsonpath
from loguru import logger


def response_assertion(actual_response,expected_result):
    if expected_result is None:
        logger.info('no need to do assertion')
        return
    logger.info('------assertion started-------')
    expected_result = json.loads(expected_result)
    for key, value in expected_result.items():# .item () is to get all the keyvalue pairs in a dictionary
        if key.startswith('$'):
            actual_data = jsonpath(actual_response.json(), key)[0]
            #.json()method is used to parse the Json data for an HTTP response object.
            #.jsonpath(要查找的对象，找的值是什么）,always return back as a list format, even there are just one match!
            logger.info(f'the actual result is ;{actual_data}')
            try:
                assert actual_data == value
                logger.info(f'assertion was successful')
            except AssertionError as e:
                logger.error('assertion failed')
                raise e
        elif key=='text':
            actual_data=actual_response.text
            logger.info (f'the actual result is ;{actual_data}')
            try:
                assert actual_data == value
                logger.info(f'assertion was successful')
            except AssertionError as e:
                logger.error('assertion failed')
                raise e

if __name__ == '__main__':
    actual_response='账号或密码不正确'
    expected_result={"text":"账号或密码不正确"}

    response_assertion(actual_response, expected_result)