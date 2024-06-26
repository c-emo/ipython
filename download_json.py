import requests
import json
import os
import time

def baidu_map_search(region, key):
    apk_key = "IVKytPOUvPgnV1IZIZDHgS0iBtKCndNp"
    url = "http://api.map.baidu.com/place/v2/search"

    all_results = []
    page_num = 0
    page_size = 20  # 百度API默认每页返回20条数据

    while True:
        params = {
            "query": key,
            "output": "json",
            "ak": apk_key,
            "region": region,
            "scope": 2,
            "page_num": page_num,
            "page_size": page_size
        }

        response = requests.get(url, params)
        result = response.json()
        status = result.get("status")
        message = result.get("message")

        if status != 0:
            raise Exception(message)

        data = result.get("results", [])

        if not data:
            break

        all_results.extend(data)
        page_num += 1

        # 每次请求后休眠20秒
        time.sleep(20)

    return all_results

def save_results_to_json(base_dir, region, key, results):
    # 创建以 region 命名的文件夹
    region_dir = os.path.join(base_dir, region)
    os.makedirs(region_dir, exist_ok=True)
    
    # 保存结果到 JSON 文件
    json_file = os.path.join(region_dir, f"{key}.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    base_dir = "csv/untreated"  # 修改为实际的根目录路径
    regions = ["珠海市"]  # 要查询的城市
    keys = ["舞蹈", "钢琴", "古筝", "美术", "书法", "口才"]  # 要查询的多个关键字
    
    for region in regions:
        for key in keys:
            print(f"region: {region}, key: {key}")
            try:
                results = baidu_map_search(region, key)
                save_results_to_json(base_dir, region, key, results)
                print(f"Data saved to {os.path.join(base_dir, region, key)}.json")
            except Exception as e:
                print(f"An error occurred for keyword '{key}': {e}")
            print("====================")
