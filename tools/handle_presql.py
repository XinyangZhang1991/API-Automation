from tools.handle_mysql import Handlemysql
from data.Environmental_Data import EnviromentalData
from loguru import logger
from data.my_sql_database_info import my_db_details
import json


def pre_sql(sql_data):
    if sql_data is None:
        return
    logger.info ('--------pre-sql-query-start--------')

    # step 2:
    sql_data=json.loads(sql_data)
    logger.info(f'pre-sql query is {sql_data}')

    # step 3:
    for key, value in sql_data.items():  # .item () is to get all the keyvalue pairs in a dictionary
        # step 4: search the data in db using the encapsulated functions in handle_mysql
        # sql_result will get us the real result
        sql_result = Handlemysql(**my_db_details).query_data(value)
        # step 5: save the result in environmental attribute
        for i,j in sql_result.items(): #i is attribute name, j is attribute value
            setattr(EnviromentalData,i,j)
    logger.info(f'the result that has been saved as environmental attribute is {EnviromentalData.__dict__}')

# if __name__=='__main__'
