import math

import core.net as net
import core.config as config

uid = '343147393'


# 获取cookie数据
def get_cookie():
    return config.get_config("bili_cookie")


# 获取B站粉丝数
def get_bilibili_fans():
    data = net.get_json("https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp" % uid)
    if 'code' in data and data['code'] == 0:
        return str(data['data']['follower'])
    else:
        return '0'


# 获取视频播放数
def get_video_play():
    cookie = get_cookie()
    data = net.get_json("https://api.bilibili.com/x/space/upstat?mid=%s&jsonp=jsonp" % uid, cookie)
    if 'code' in data and data['code'] == 0 and 'archive' in data['data']:
        return str(data['data']['archive']['view'])
    else:
        return '0'


# 获取视频播放列表
def get_video_list(now):
    cookie = config.get_config("bili_cookie")
    data = net.get_json("https://api.bilibili.com/x/space/arc/search?mid=%s&ps=6&tid=0&pn=%d&keyword=&order=pubdate"
                        "&jsonp=jsonp" % (uid, now), cookie)
    response = {
        "total": 0,
        "now": 0,
        "data": []
    }
    # 解析数据
    if "code" in data and data["code"] == 0 and "data" in data:
        data = data["data"]
        if "page" in data:
            response["total"] = math.ceil(data["page"]["count"]/data["page"]["ps"])
            response["now"] = data["page"]["pn"]
        if "list" in data and "vlist" in data["list"]:
            for video in data["list"]["vlist"]:
                response["data"].append({
                    "title": video["title"],
                    "pic": video["pic"],
                    "view": video["play"],
                    "comment": video["comment"]
                })
    return response


if __name__ == '__main__':
    print(get_video_list(1))
