# used for handle the path of the file

import pathlib


# # get the path for the current file:Pycharm/API-Automation/tools/handle_path.
# print (pathlib.Path(__file__).absolute())
# # get the path for the current file' parent:Pycharm/API-Automation/tools
# print (pathlib.Path(__file__).absolute().parent)
# # get the path for the current file' parent.parent:Pycharm/API-Automation
# print (pathlib.Path(__file__).absolute().parent.parent)


log_path = pathlib.Path(__file__).absolute().parent.parent/"outputs"/"logs"

file_path = pathlib.Path(__file__).absolute().parent.parent/"data"

# testing_mall_path
excel_path_day16= pathlib.Path(__file__).absolute().parent.parent/'data'/'testing_mall_day16.xlsx'
# print (excel_path)
excel_path_xinyangapitesting= pathlib.Path(__file__).absolute().parent.parent/'data'/'xinyangapitesting own.xlsx'


