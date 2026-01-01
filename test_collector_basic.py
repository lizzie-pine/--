import os
import sys
import logging
from pathlib import Path
from collector.weather_api_collector import WeatherDataCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_collector_basic():
    """测试天气数据采集器的基本功能，不调用API"""
    try:
        # 创建一个临时API密钥用于测试
        api_key = "test_key"
        
        # 创建采集器实例
        logger.info("创建天气数据采集器实例...")
        collector = WeatherDataCollector(api_key=api_key)
        
        # 测试获取城市列表
        logger.info("测试加载城市列表...")
        cities = collector.load_cities()
        logger.info(f"加载了 {len(cities)} 个城市")
        logger.info(f"前5个城市: {cities['city_name_simple'].head(5).tolist()}")
        
        # 测试获取城市坐标
        logger.info("测试加载城市坐标...")
        city_coords = collector.load_city_coordinates()
        logger.info(f"加载了 {len(city_coords)} 个城市的坐标")
        logger.info(f"部分城市坐标示例: {list(city_coords.items())[:3]}")
        
        # 测试日期处理功能
        logger.info("测试日期处理功能...")
        from datetime import datetime
        test_date = datetime.now()
        weekday = collector.get_weekday(test_date)
        logger.info(f"今天是: {weekday}")
        
        # 测试文件路径设置
        logger.info("测试文件路径设置...")
        logger.info(f"数据目录: {collector.data_dir}")
        logger.info(f"天气数据目录: {collector.weather_dir}")
        logger.info(f"城市文件: {collector.city_file}")
        
        logger.info("基本功能测试完成")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_collector_basic()
