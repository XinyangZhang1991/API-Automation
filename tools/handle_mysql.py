# This function establish sql connection, enable data query

import pymysql
from pymysql.cursors import DictCursor  # 读取的数据默认变成字典的格式
from loguru import logger


class Handlemysql:
    def __init__(self,user,password,database,port,host):
        # two instance attributes (connection, cursor) were defined, therefore can be used for future instance method
        # Using self ensures that these variables are available across all methods in that particular instance.
        self.connection = pymysql.connect(
                        user="lemon_auto",
                        password="lemon!@123",
                        database="yami_shops",
                        port=3306,
                        host="mall.lemonban.com",
                        charset="utf8mb4",  # support chinese characters
                        cursorclass=DictCursor)  # data change to dictionary format by default

        self.cursor = self.connection.cursor()

# instance method 1:
    def query_data(self,sql_query,match_number=1,size=None): # I set the initial match number to 1 as in most case we only need 1 row of data, so later on do not need to pass parameter/argument anymore
        result=self.cursor.execute(sql_query)
        try:
            result=self.cursor.execute(sql_query) #this get the number of row in result, not the actual result.
            if result > 0:
                if match_number == 1:
                    data = self.cursor.fetchone() #here we get the actual data
                    return data
                elif match_number ==2:
                    data = self.cursor.fetchmany(size)
                    return data
                elif match_number ==-1:
                    data =self.cursor.fetchall()
                    return data
            else:
                logger.info(f'no data found in database')
        except Exception as error:
            logger.error(f'errors in database : {error}')
        finally:
            self.cursor.close()
            self.connection.close()
# Self is used to differentiating Between Local and Instance Variables:Inside a method, without self, any variable you define would be considered a local variable that is scoped only to that function.When you use self, it makes it clear that the variable or method being referenced belongs to the object instance (and not just a local function variable).

if __name__ == '__main__':
    sql = 'select user_phone,mobile_code from tz_sms_log where user_phone = "13555554444" order by rec_date desc;'
    my_db = {
            "user": "lemon_auto",
            "password": "lemon!@123",
            "database": "yami_shops",
            "port": 3306,
            "host": "mall.lemonban.com"
        }
    handle_sql= Handlemysql(**my_db) #The ** : unpack a dictionary into keyword arguments when passing them to a function or class constructor.
    result=handle_sql.query_data(sql)
    print(result)
