import requests
import csv
import time
import os

def save_to_csv(file_path, data, fieldnames):  # 保存数据到 CSV 文件
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                'name': row.get('name', ''),
                'address': row.get('address', ''),
                'province': row.get('province', ''),
                'city': row.get('city', ''),
                'area': row.get('area', ''),
                'telephone': row.get('telephone', ''),
                'tag': row.get('detail_info', {}).get('tag', ''),
                # 'label': row.get('detail_info', {}).get('label', '')
            })

def baidu_map_search(region, key): # 百度地图API查询
    apk_key = "IVKytPOUvPgnV1IZIZDHgS0iBtKCndNp" # 百度地图API密钥
    url = "http://api.map.baidu.com/place/v2/search" # 百度地图API地址

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

if __name__ == '__main__':
    base_dir = "csv/untreated"  # 修改为实际的根目录路径
    regions = ["广州市"]  # 要查询的城市
    keys = ["舞蹈", "钢琴", "古筝", "美术", "书法", "口才"]  # 要查询的多个关键字
    
    for region in regions:
        for key in keys:
            print(f"region: {region}, key: {key}")
            try:
                results = baidu_map_search(region, key)

                # 创建以 region 命名的文件夹
                region_dir = os.path.join(base_dir, region)
                os.makedirs(region_dir, exist_ok=True)

                csv_file = os.path.join(region_dir, f"{key}.csv")
                fieldnames = ['name', 'address', 'province', 'city', 'area', 'telephone', 'tag']
                save_to_csv(csv_file, results, fieldnames)

                print(f"Data saved to {csv_file}")
            except Exception as e:
                print(f"An error occurred for keyword '{key}': {e}")
            print("====================")
