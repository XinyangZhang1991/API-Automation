from loguru import logger
import re
from data.Environmetnal_Data import EnviromentalData



def replace_data(string_data):
    # Step 1 : check none
    if string_data is None:
        logger.info('no data in excel sheet shows need replacement')
        return
    # Step 2 : find placeholder
    result=re.findall('#(.*?)#',string_data)
    # (.*?): This is a non-greedy (or lazy) match for any sequence of characters
    # The pattern "#(.*?)#" looks for substrings in string_data that are enclosed between # characters
    # result will know which key needs replacement

    # Step 3: check whether placeholder is found
    if result:
        logger.info('-----data_replacement_start------')
        logger.info(f'the original data will be replaced is:{string_data}')
        logger.info(f'the key needs to be replaced are {result} ')
        for mark in result:
            if hasattr(EnviromentalData,mark):
                string_data=string_data.replace(f'#{mark}#',str(getattr(EnviromentalData,mark)))
    else:
        logger.info(f'no value need replacement, {result} no need to replace data ')
    logger.info(f'the placeholder has been replaced to {string_data}')
    return string_data

if __name__ == '__main__':
    class EnviData:
        prodId = 123
        skuId = 456
    str_data= '{"basketId": 0, "count": 1111, "prodId": #prodId#, "shopId": 1, "skuId": #skuId#}'
    print(replace_data(str_data))
