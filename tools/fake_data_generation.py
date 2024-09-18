from faker import Faker
from tools.handle_mysql import Handlemysql
from data.my_sql_database_info import my_db_details


class fake_data_generation:

    def gen_unregister_phone(self):
        fk = Faker(locale='zh_CN')
        while True: # creates an infinite loop that will keep running until it meets the condition to stop.
            phone_number = fk.phone_number()
            sql = f'select * from tz_user where user_mobile = "{phone_number}"'
            result = Handlemysql(**my_db_details).query_data(sql)

            if result is not None:
                continue
            else:
                return phone_number

    def gen_unregister_name(self):
        fk= Faker(locale='zh_CN')
        while True:
            user_name=fk.user_name()
            sql = f'select * from tz_user where nick_name  = "{user_name}"'
            result=Handlemysql(**my_db_details).query_data(sql)

            if result is not None or (len(user_name)>16 or len(user_name)<4):
                continue
            else:
                return user_name