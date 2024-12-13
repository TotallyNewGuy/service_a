import requests

# 请求的参数
data = {
    'content': 'woshini',
}

# 发送POST请求
response = requests.post('http://localhost:8080/topic/publish/bus-data', json=data)


# 输出响应的状态码和内容
print("Status Code:", response.status_code)  # 状态码
print("Response Content:", response.text)  # 响应内容
