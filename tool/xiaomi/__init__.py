import core.net as net
import core.config as config


# homeAssistant服务控制
def homeAssistantControl(domain, service, entity):
    net.json_post_json("http://192.168.1.18:8053/api/services/%s/%s" % (domain, service), {
        "entity_id": entity
    }, heads={
        "Authorization": "Bearer %s" % config.get_config("ha_token")
    })


# 获取服务状态
def homeAssistant_status(entity):
    return net.get_json("http://192.168.1.18:8053/api/states/%s" % entity, heads={
        "Authorization": "Bearer %s" % config.get_config("ha_token")
    })


# 灯光控制
def light_switch(status):
    if status:
        homeAssistantControl("light", "turn_on", "light.mbulb3_cloud_128410")
    else:
        homeAssistantControl("light", "turn_off", "light.mbulb3_cloud_128410")


# 开关控制
def switch_switch(status):
    if status:
        homeAssistantControl("switch", "turn_on", "switch.212a01_cloud_149431")
    else:
        homeAssistantControl("switch", "turn_off", "switch.212a01_cloud_149431")


# 室内温度
def get_home_temperature():
    state = homeAssistant_status("sensor.t2_cloud_m0ek00_temperature")
    if "attributes" in state:
        return {
            "temperature": state["attributes"]["temperatur_temperature"],
            "humidity": state["attributes"]["temperatur_relative_humidity"]
        }
