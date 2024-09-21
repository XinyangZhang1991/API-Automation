import requests


# 1、发送post请求 【四大要素】
url_search = "http://shop.lemonban.com:8107/login"
metd = "post"
param = {"principal":"lemon_py",
"credentials":"12345678",
"appType":3,
"loginType":0
}
# header = {"Content-Type":"application/json"}

#发送post接口请求
# resp = requests.request(method=metd,url=url_search,json=param,headers=header)
# resp = requests.request(method=metd, url=url_search, json=param)
# print(resp)  # Response对象  可以获取详细的方法
# print(resp.status_code)  # 获取响应状态码
# print(resp.text) #获取响应文本 -数据 字符串
# print(resp.json()) # 响应文本如果是json格式，直接转化Python的字典



import requests
# 发送get请求 【四大要素】
url_search = "http://shop.lemonban.com:8107/search/searchProdPage"
metd = "get"
param = {"prodName":"圆筒包"}

#发送接口请求
resp = requests.request(method=metd,url=url_search,params=param)
print(resp)  # Response对象  可以获取详细的方法
print(resp.status_code)  # 获取响应状态码
print(resp.text) #获取响应文本 -数据 字符串
print(resp.json()) # 响应文本如果是json格式，直接转化Python的字典
