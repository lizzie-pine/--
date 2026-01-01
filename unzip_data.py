import zipfile
import os
import sys

zip_file_path = 'data/cities_weather.zip'
extract_path = 'data/cities_weather'

if not os.path.exists(extract_path):
    os.makedirs(extract_path)

try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 处理中文文件名乱码问题
        for file_info in zip_ref.infolist():
            # 对文件名进行编码转换
            if sys.platform.startswith('win'):
                # Windows系统使用gbk编码
                file_info.filename = file_info.filename.encode('cp437').decode('gbk')
            else:
                # Linux系统使用utf-8编码
                file_info.filename = file_info.filename.encode('cp437').decode('utf-8')
            # 提取文件
            zip_ref.extract(file_info, extract_path)
    print(f"Successfully extracted {zip_file_path} to {extract_path} with correct encoding")
except Exception as e:
    print(f"Error extracting file: {e}")
    sys.exit(1)