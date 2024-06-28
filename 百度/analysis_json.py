import os
import json
import shutil
import pandas as pd

def json_to_excel(json_file, excel_file):
    # 打开 JSON 文件并加载数据
    with open(json_file, 'r', encoding='utf-8') as file:
        datas = json.load(file)
        
    # 准备一个空的列表，用于存储符合条件的数据
    filtered_data = []

    # 遍历 JSON 数据
    for data in datas:
        detail_info = data.get('detail_info', {})
        label = detail_info.get('label', '')
        
        # 判断条件，如果 label 包含 '培训'，则将数据加入 filtered_data 列表
        if '培训' in label:
            filtered_data.append({
                'name': data.get('name', ''),
                'address': data.get('address', ''),
                'province': data.get('province', ''),
                'city': data.get('city', ''),
                'area': data.get('area', ''),
                'telephone': data.get('telephone', ''),
                'label': label,
            })

    # 将符合条件的数据转换为 DataFrame
    df = pd.DataFrame(filtered_data)

    # 将数据写入 Excel 文件
    df.to_excel(excel_file, index=False)
       

def process_city_directory(city_dir, output_base_dir, processed_base_dir):
    city_name = os.path.basename(city_dir)
    
    # 创建输出目录和已处理目录的城市子目录
    output_city_dir = os.path.join(output_base_dir, city_name)
    processed_city_dir = os.path.join(processed_base_dir, city_name)
    os.makedirs(output_city_dir, exist_ok=True)
    os.makedirs(processed_city_dir, exist_ok=True)
    
    # 遍历城市目录中的所有 JSON 文件
    for filename in os.listdir(city_dir):
        if filename.endswith(".json"):
            json_file = os.path.join(city_dir, filename)
            excel_file = os.path.join(output_city_dir, os.path.splitext(filename)[0] + ".xlsx")
            
            print(f"Converting file: {json_file} to {excel_file}")
            try:
                json_to_excel(json_file, excel_file)
                print(f"Data saved to {excel_file}")
                
                processed_file = os.path.join(processed_city_dir, filename)
                shutil.move(json_file, processed_file)
                print(f"Moved processed file to {processed_file}")
            except Exception as e:
                print(f"An error occurred while processing '{json_file}': {e}")
            print("====================")

    # 删除处理完的城市目录
    try:
        shutil.rmtree(city_dir)
        print(f"Deleted directory: {city_dir}")
    except Exception as e:
        print(f"An error occurred while deleting directory '{city_dir}': {e}")

def process_all_cities(input_base_dir, output_base_dir, processed_base_dir): # 遍历所有城市目录
    for city_name in os.listdir(input_base_dir): # 遍历每个城市目录
        city_dir = os.path.join(input_base_dir, city_name) # 获取城市目录
        if os.path.isdir(city_dir): # 判断是否为目录
            process_city_directory(city_dir, output_base_dir, processed_base_dir) # 处理城市目录

if __name__ == '__main__':
    input_base_dir = "百度/json/untreated"  # 修改为实际的未处理文件夹路径
    output_base_dir = "百度/exl_file/json"    # 修改为实际的输出文件夹路径
    processed_base_dir = "百度/json/processed"  # 修改为实际的已处理文件夹路径
    # 调用方法遍历文件处理csv data
    process_all_cities(input_base_dir, output_base_dir, processed_base_dir)
