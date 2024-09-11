import json
from jsonpath import jsonpath
from loguru import logger


def response_assertion(actual_response,expected_result):
    if expected_result is None:
        logger.info('no need to de assertion')
        return
    logger.info('------assertion started-------')
    expected_result = json.loads(expected_result)
    for key, value in expected_result.items():
        if key.startwith('$'):
            actual_data = jsonpath(actual_response.json(),key)
            logger.info(f'the actual result is ;{actual_data}')
            try:
                assert actual_data == value
                logger.info(f'assertion is successful')
            except AssertionError as e:
                logger.error('assertion did not meet')
                raise e

