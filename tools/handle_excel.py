# Turn the testcase in Excel spreadsheet into the dictionary format  we need

from openpyxl import load_workbook
from tools.handle_path import excel_path_day16


def read_excel(filename,sheetname):
    wb = load_workbook(filename)
    sh = wb[sheetname] #固定的格式，就得这么写
    case_all = list(sh.values)
    print(case_all)
    title = case_all[0]
    entire_testcase_list = []  #Initalise an empty list for zip dictionary later
    for case in case_all[1:]:  #从列表中的第二个开始,因为第一个数据是标题
        data = dict(zip(title, case))
        print(data)
        entire_testcase_list.append(data)
    return entire_testcase_list

if __name__ =='__main__':
    from handle_path import excel_path_day16
    print(read_excel(excel_path_day16,'登录'))
