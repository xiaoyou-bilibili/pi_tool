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
    response = requests.get(url)
    return response.text


# 获取json形式的数据
def get_json(url, cookie=None, heads=None, proxies=None):
    new_head = head.copy()
    if cookie is not None:
        new_head["cookie"] = cookie
    new_head = set_map_data(new_head, heads)
    response = requests.get(url, headers=new_head, proxies=proxies)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print(response.content)
        return {}


# post请求获取JSON数据
def post_json(url, post_data, cookie=None, heads=None):
    new_head = head.copy()
    if cookie is not None:
        new_head["cookie"] = cookie
    new_head = set_map_data(new_head, heads)
    response = requests.post(url, post_data, headers=new_head)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return {}


# post的多文件上传
def form_post(url, form_data, file):
    r = requests.post(url, data=form_data, files=file)
    return r.text


# 发送json格式数据
def json_post_json(url, post_data, heads=None):
    new_head = head.copy()
    new_head = set_map_data(new_head, heads)
    head["Content-Type"] = "application/json"
    post_data = requests.post(url, data=json.dumps(post_data), headers=new_head)
    if post_data.status_code == requests.codes.ok:
        return post_data.json()
    else:
        return {}


# 获取二进制数据
def get_row_data(url):
    return requests.get(url, timeout=3).content


if __name__ == '__main__':
    data = get_row_data("https://i0.hdslb.com/bfs/archive/1ebd4c2c1bc45e5f4cc814ee33d8dfe064650fd1.png")
    print(data)