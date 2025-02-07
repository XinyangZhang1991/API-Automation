import pytest


# run the below command
# 每次执行一次就会又重复生成结果文件不会清楚;会影响报告结果，所以 需要加一个清除的参数:
# Run all tests in the current project (based on your test discovery).
# Save the raw test results in outputs/allure_report directory.
# Clean the directory of old results before saving new ones.
# Show detailed (verbose) output in the console during the execution.
pytest.main(["-v","--alluredir=outputs/allure_report","--clean-alluredir"])

# 或者直接在terminal里面输入这句话 pytest --alluredir=outputs/allure_report --clean-alluredir -v


# after running the above command , run the below command to generate HTML report

# 生成报告 输入这句话： allure serve outputs/allure_report

# 删除所有关于上次allure的东西， 输入这句话在terminal里面 ： Remove-Item -Path "outputs\allure_report\*" -Recurse -Force