import requests
import json
import os
import time
import pdb

def baidu_map_search(region, key):
    apk_key = "736baea75580692cbee833afe7cee5f8"
    url = "https://restapi.amap.com/v5/place/text"
    all_results = []
    page_num = 0 # page_num 的取值1-100
    page_size = 25  # page_size 的取值1-25

    while True:
        params = {
            "keywords": key,
            "types": "141400",
            "key": apk_key,
            "city_limit": "true",
            "output": "json",
            "region": region,
            "page_num": page_num,
            "page_size": page_size
        }

        response = requests.get(url, params)
        result = response.json()
        status = result.get("status")
        message = result.get("message")

        pdb.set_trace()

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
    base_dir = "高德/json/untreated"  # 修改为实际的根目录路径
    regions = ["珠海市"]  # 要查询的城市
    keys = ["舞蹈", "钢琴", "古筝", "美术", "书法", "口才"]  # 要查询的多个关键字
    
    for region in regions:
        for key in keys:
            print(f"region: {region}, key: {key}")
            try:
                results = baidu_map_search(region, key)
                pdb.set_trace()
                save_results_to_json(base_dir, region, key, results)
                print(f"Data saved to {os.path.join(base_dir, region, key)}.json")
            except Exception as e:
                print(f"An error occurred for keyword '{key}': {e}")
            print("====================")
