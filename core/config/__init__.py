import nacos

SERVER_ADDRESSES = "http://192.168.1.18:8036"
NAMESPACE = "public"
client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE)


# 获取配置
def get_config(key):
    global client
    if client is not None:
        return client.get_config(key, "pi")
    return ""


if __name__ == '__main__':
    print(get_config("ha_token"))
