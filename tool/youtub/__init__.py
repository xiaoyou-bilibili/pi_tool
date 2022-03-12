import core.net as net
import core.config as config

channelID = "UCdHNS1d3fTx-m69tKsr7n3w"
apiKey = config.get_config("youtub_token")


def get_youtube_fan():
    url = "https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id=%s&key=%s" % (channelID, apiKey)
    data = net.get_json(url, proxies={"https": "http://192.168.1.1:7890"})
    if "items" in data and len(data["items"][0]) >= 1 and "statistics" in data["items"][0]:
        static = data["items"][0]["statistics"]
        return {
            "view": static["viewCount"],
            "fan": static["subscriberCount"]
        }


if __name__ == '__main__':
    print(get_youtube_fan())
