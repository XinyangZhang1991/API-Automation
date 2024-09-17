from loguru import logger
import re
from data.Environmental_Data import EnviromentalData
from tools.fake_data_generation import fake_data_generation


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
            # below if test whether the placeholder is a faker function
            if '()' in mark: # Checks if the current placeholder (mark) contains the string '()'. This suggests that the placeholder corresponds to a function call, likely to generate fake data dynamically
                # If mark is gen_unregister_phone(), it evaluates and calls fake_data_generation().gen_unregister_phone().
                # Uses the eval() function to dynamically execute the string fake_data_generation().{mark}
                gen_data=eval(f'fake_data_generation().{mark}')
                variable_name=mark.strip('()')
                # Sets an attribute in the EnviromentalData object with the name variable_name and the value gen_data. This allows you to store the generated data in a global or shared context.
                setattr(EnviromentalData,variable_name,gen_data)
                string_data=string_data.replace(f'#{mark}#',str(gen_data))
                logger.info(f'data generated from faker saved into environmental variable is {EnviromentalData.__dict__}')
            #  This else block below handles the case where mark is not a function but rather a simple placeholder
            else:
                # hasattr(EnviromentalData, mark) checks if mark exists as an attribute in EnviromentalData
                if hasattr(EnviromentalData,mark):
                    # replaces the placeholder #mark# with this value.
                    string_data=string_data.replace(f'#{mark}#',str(getattr(EnviromentalData,mark)))
    else:
        logger.info(f'no value need replacement, {result} no need to replace data ')
    logger.info(f'the placeholder has been replaced to {string_data}')
    return string_data

if __name__ == '__main__':
    class EnviData:
        prodId = 123
        skuId = 456
    # string_data= '{"basketId": 0, "count": 1111, "prodId": #prodId#, "shopId": 1, "skuId": #skuId#}'
    haha_data = '{"mobile": "#gen_unregister_phone()#"}'
    print(replace_data(haha_data))
