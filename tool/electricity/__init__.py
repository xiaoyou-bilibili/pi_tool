import datetime
import core.net as net
import core.config as config


# 获取电费使用情况
def get_electricity_use():
    today = datetime.datetime.today()
    data = net.post_json("https://api.baletu.com/App401/User/getElectricMeterMonthlyWattage", {
        "year": str(today.year),
        "month": str(today.month),
        "v": "6.0.7",
        "use_type": "0",
        "city_id": "1",
        "ut": config.get_config("electricity_token"),
        "user_id": "1017963078",
    })
    use = 0.0
    share = 0.0
    # 最终结果
    res = {
        "remain": 0,
        "money": 0,
        "use": 0,
        "yesterday": 0,
    }

    # 计算本月总用电量
    if "result" in data and "list" in data["result"]:
        for day in data["result"]["list"]:
            try:
                use += float(day["wattage"])
                share += float(day["shared_value"])
            except Exception as e:
                pass
        # 获取剩余用电和昨日用电
        remain = data["result"]["list"][-1]["read_value"]
        today = data["result"]["list"][-1]["wattage"]
        # 保存结果
        total = use + share
        res["remain"] = remain
        res["money"] = total * 0.9
        res["use"] = use
        res["yesterday"] = today

    return res


if __name__ == '__main__':
    print(get_electricity_use())
