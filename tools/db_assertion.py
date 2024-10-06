
from loguru import logger
import json
from handle_replacement import replace_data
from handle_mysql import Handlemysql
from tools.handle_mysql import Handlemysql
from data.my_sql_database_info import my_db_details


def db_assertion(sql_used_for_assertion):
    if sql_used_for_assertion is None:
        return
    logger.info("--------Database Assertation Starts-----")
    # step 1 - change json to dictionary format
    dic_format_assertion_sql = json.loads(sql_used_for_assertion)
    logger.info(f'the sql query is {sql_used_for_assertion}')
    # step 2 - using for loop to get the key (sql) and value (the result from DB query)
    for k,v in dic_format_assertion_sql.items():
        # step 3 - replace the placeholder for in the sql
        k = replace_data(k)
        sql_result =Handlemysql(**my_db_details).query_data(k)
        for i in sql_result.values():# 因为数据库结果的key不固定的 不能通过key取值value .values获取得到实际结果
            logger.info(f"数据库的实际结果是：{i}")
            logger.info(f"数据库的预期结果是：{v}")
            try:
                assert i==v
                logger.info("DB assertion is successful")
            except AssertionError as e:
                logger.error("DB assertion failed")
                raise e


if __name__ == '__main__':

    sql_1 ={"select count(*) from tz_order where order_number = '#orderNumbers#'":1,
"select status from tz_order where order_number = '#orderNumbers#'":1}
    sql_2 ={"select status from tz_order where order_number = '#orderNumbers#'":2,"select is_payed from tz_order where order_number = '#orderNumbers#'":1}

    db_assertion(sql_1)