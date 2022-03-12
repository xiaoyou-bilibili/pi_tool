import core.net as net
import core.config as config

uid = '343147393'


# 获取B站粉丝数
def get_bilibili_fans():
    data = net.get_json("https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp" % uid)
    if 'code' in data and data['code'] == 0:
        return str(data['data']['follower'])
    else:
        return '0'


# 获取视频播放数
def get_video_play():
    cookie = config.get_config("bili_cookie")
    data = net.get_json("https://api.bilibili.com/x/space/upstat?mid=%s&jsonp=jsonp" % uid, cookie)
    if 'code' in data and data['code'] == 0 and 'archive' in data['data']:
        return str(data['data']['archive']['view'])
    else:
        return '0'


if __name__ == '__main__':
    print(get_video_play())
