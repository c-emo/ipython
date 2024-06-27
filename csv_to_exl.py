import os
import shutil
import pandas as pd

def csv_to_excel(csv_file, excel_file):
    df = pd.read_csv(csv_file, encoding='utf-8')
    filtered_df = df[df['tag'].str.contains('教育培训|培训机构|运动健身', na=False)]
    # filtered_df = df[df['label'].str.contains('培训', na=False)]
    filtered_df.to_excel(excel_file, index=False)

def process_city_directory(city_dir, output_base_dir, processed_base_dir):
    city_name = os.path.basename(city_dir)
    
    # 创建输出目录和已处理目录的城市子目录
    output_city_dir = os.path.join(output_base_dir, city_name)
    processed_city_dir = os.path.join(processed_base_dir, city_name)
    os.makedirs(output_city_dir, exist_ok=True)
    os.makedirs(processed_city_dir, exist_ok=True)
    
    # 遍历城市目录中的所有 CSV 文件
    for filename in os.listdir(city_dir):
        if filename.endswith(".csv"):
            csv_file = os.path.join(city_dir, filename)
            excel_file = os.path.join(output_city_dir, os.path.splitext(filename)[0] + ".xlsx")
            
            print(f"Converting file: {csv_file} to {excel_file}")
            try:
                csv_to_excel(csv_file, excel_file)
                print(f"Data saved to {excel_file}")
                
                processed_file = os.path.join(processed_city_dir, filename)
                shutil.move(csv_file, processed_file)
                print(f"Moved processed file to {processed_file}")
            except Exception as e:
                print(f"An error occurred while processing '{csv_file}': {e}")
            print("====================")

    # 删除处理完的城市目录
    try:
        shutil.rmtree(city_dir)
        print(f"Deleted directory: {city_dir}")
    except Exception as e:
        print(f"An error occurred while deleting directory '{city_dir}': {e}")

def process_all_cities(input_base_dir, output_base_dir, processed_base_dir):
    for city_name in os.listdir(input_base_dir):
        city_dir = os.path.join(input_base_dir, city_name)
        if os.path.isdir(city_dir):
            process_city_directory(city_dir, output_base_dir, processed_base_dir)

if __name__ == '__main__':
    input_base_dir = "csv/untreated"  # 修改为实际的未处理文件夹路径
    output_base_dir = "exl_file/csv"    # 修改为实际的输出文件夹路径
    processed_base_dir = "csv/processed"  # 修改为实际的已处理文件夹路径
    # 调用方法遍历文件处理csv data
    process_all_cities(input_base_dir, output_base_dir, processed_base_dir)
