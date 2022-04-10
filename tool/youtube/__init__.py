import core.net as net
import core.config as config

channelID = "UCdHNS1d3fTx-m69tKsr7n3w"


def get_youtube_fan():
    key = config.get_config("youtub_token")
    url = "https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id=%s&key=%s" % (channelID, key)
    data = net.get_json(url, proxies={"https": "http://192.168.1.1:7890"})
    res = {"view": "0", "fan": "0"}
    if "items" in data and len(data["items"][0]) >= 1 and "statistics" in data["items"][0]:
        static = data["items"][0]["statistics"]
        res["view"] = str(static["viewCount"])
        res["fan"] = str(static["subscriberCount"])
    else:
        print("错误:", data)

    return res


if __name__ == '__main__':
    print(get_youtube_fan())
