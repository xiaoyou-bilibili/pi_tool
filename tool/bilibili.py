import core.net as net

uid = '343147393'
cookie = "_uuid=9448A248-58DC-9936-A9103-8CFCA17910921032370infoc; buvid3=A1AC5D76-EBE9-4C70-95F7-1F70B6CC82DA167633infoc; b_nut=1638837032; blackside_state=1; rpdid=|(k|YuY~m~YY0J'uYJ)mkR~Rm; DedeUserID=343147393; DedeUserID__ckMd5=12513b11ac02b3e1; sid=6c0edl8x; LIVE_BUVID=AUTO2116406954609637; dy_spec_agreed=1; i-wanna-go-back=-1; b_ut=5; buvid4=8C145BCF-6A50-4B66-7AD8-5911A5A9253F03794-022013122-Id4lnZ0wDzhZt7VD3iBwcQ%3D%3D; fingerprint=55752fe967f0cafb6358f9ef0d20478a; buvid_fp_plain=undefined; buvid_fp=55752fe967f0cafb6358f9ef0d20478a; SESSDATA=03d28da0%2C1659190419%2Ce1aef*11; bili_jct=9808dd24ddd63d89ea25fa0c7efd42cd; CURRENT_BLACKGAP=0; bp_video_offset_343147393=633025016417484900; bp_t_offset_343147393=635975830744334361; b_lsid=52E3C4D7_17F768E2379; innersign=1; CURRENT_QUALITY=116; CURRENT_FNVAL=80; PVID=2"


# 获取B站粉丝数
def get_bilibili_fans():
    data = net.get_json("https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp" % uid)
    if 'code' in data and data['code'] == 0:
        return data['data']['follower']
    else:
        return '0'


# 获取视频播放数
def get_video_play():
    data = net.get_json("https://api.bilibili.com/x/space/upstat?mid=%s&jsonp=jsonp" % uid, cookie)
    print(data)
    if 'code' in data and data['code'] == 0:
        return data['data']['archive']['view']
    else:
        return '0'


if __name__ == '__main__':
    print(get_video_play())
