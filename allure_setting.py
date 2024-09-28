import pytest



# 每次执行一次就会又重复生成结果文件不会清楚;会影响报告结果，所以 需要加一个清除的参数:
# pytest.main(["-v","--alluredir=outputs/allure_report","--clean-alluredir"])


# # 运行生成allure测试报告
# -  "--alluredir=outputs/allure_report"
# - 目录基于rootdir来算的
# - 注意：=前后不要加空格
# - 结果： 会在outputs文件夹下面 生成allure_report目录，并且把allure报告文件放在这个目录。
#    - 这些结果文件是json格式的，不是给人看的 是allure工具看的。
# - 生成html文件报告： 给人看的 直观页面报告
#     - cmd命令行去生成：  allure serve .\outputs\allure_report\  【相当于run.py 的rootdir的路径】
#     - 以后结合Jenkins之后 就可以不用这么麻烦了。
# - 重点关注失败的用例【红色的用例】
#    - 产品缺陷【prodect defect】： 断言失败的，大概率是产品的bug 分析定位bug  记录禅道/jira。
#    - 用例缺陷【test defect】: 用例脚本本身的问题 -- 优化脚本和代码。
#
# -  因为每次执行代码的时候 都会生成新的allure结果json文件，不会自动删除；报告又不会读取旧的文件；
#   - 所以一般都默认加上清除历史文件的参数："--clean-alluredir"
#   - 每次生成结果之前 先删除历史文件。