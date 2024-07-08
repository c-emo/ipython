import os
import pandas as pd
import requests
import time

def save_to_excel(file_path, datas, lab):
    # 准备一个空的列表，用于存储符合条件的数据
    filtered_data = []

    # 遍历 JSON 数据
    for data in datas:
        detail_info = data.get('detail_info', {})
        label = detail_info.get('label', '')
        
        # 判断条件，如果 label 包含 '培训'，则将数据加入 filtered_data 列表
        if lab in label:
            filtered_data.append({
                'name': data.get('name', ''),
                'address': data.get('address', ''),
                'province': data.get('province', ''),
                'city': data.get('city', ''),
                'area': data.get('area', ''),
                'telephone': data.get('telephone', ''),
                'tag': detail_info.get('tag', ''),
                'label': label,
            })

    # 将符合条件的数据转换为 DataFrame
    df = pd.DataFrame(filtered_data)

    # 将数据写入 Excel 文件
    df.to_excel(file_path, index=False)

def baidu_map_search(region, key):
    apk_key = "IVKytPOUvPgnV1IZIZDHgS0iBtKCndNp"
    url = "http://api.map.baidu.com/place/v2/search"

    all_results = []
    page_num = 0
    page_size = 20

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

        time.sleep(20)

    return all_results

if __name__ == '__main__':
    output_dir = "exl_file/test"  # 修改为实际的输出文件夹路径
    regions = ["广州市"]
    keys = { # 要查询的关键字及类型  类型 ：[关键字]
        "培训": ["舞蹈", "钢琴", "古筝", "美术", "书法", "口才"]
    }
    for region in regions:
        for lab, values in keys.items():
            region_dir = os.path.join(output_dir, region)
            os.makedirs(region_dir, exist_ok=True)
            for value in values:
                print(f"region: {region}, key: {value}")
                try:
                    results = baidu_map_search(region, value)
                    excel_file = os.path.join(region_dir, f"{value}.xlsx")
                    save_to_excel(excel_file, results, lab)
                    print(f"Data saved to {excel_file}")
                except Exception as e:
                    print(f"An error occurred for keyword '{value}': {e}")
                print("====================")