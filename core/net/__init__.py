import requests
import json

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47",
}


# 更新map数据
def set_map_data(old, new):
    if new is not None:
        for key in new:
            old[key] = new[key]
    return old


# 原始json下载
def get(url):
    data = requests.get(url)
    return data.text


# 获取json形式的数据
def get_json(url, cookie=None, heads=None, proxies=None):
    global head
    if cookie is not None:
        head["cookie"] = cookie
    head = set_map_data(head, heads)
    data = requests.get(url, headers=head, proxies=proxies)
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        return {}


# post请求获取JSON数据
def post_json(url, data, cookie=None, heads=None):
    global head
    if cookie is not None:
        head["cookie"] = cookie
    head = set_map_data(head, heads)
    data = requests.post(url, data, headers=head)
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        return {}


# post的多文件上传
def form_post(url, data, file):
    r = requests.post(url, data=data, files=file)
    return r.text


# 发送json格式数据
def json_post_json(url, data, heads=None):
    global head
    head = set_map_data(head, heads)
    head["Content-Type"] = "application/json"
    data = requests.post(url, data=json.dumps(data), headers=head)
    if data.status_code == requests.codes.ok:
        return data.json()
    else:
        return {}