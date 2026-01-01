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

def test_collector():
    """测试天气数据采集器"""
    try:
        # 获取API密钥
        api_key = os.environ.get('QWEATHER_API_KEY')
        if not api_key:
            logger.error("请设置环境变量QWEATHER_API_KEY")
            return False
        
        # 创建采集器实例
        logger.info("创建天气数据采集器实例...")
        collector = WeatherDataCollector(api_key=api_key)
        
        # 测试获取城市列表
        logger.info("测试加载城市列表...")
        cities = collector.load_cities()
        logger.info(f"加载了 {len(cities)} 个城市")
        
        # 测试获取城市坐标
        logger.info("测试加载城市坐标...")
        city_coords = collector.load_city_coordinates()
        logger.info(f"加载了 {len(city_coords)} 个城市的坐标")
        
        # 测试获取Location ID
        logger.info("测试获取Location ID...")
        test_city = "北京"
        location_id = collector.get_location_id(test_city)
        if location_id:
            logger.info(f"{test_city} 的Location ID是: {location_id}")
        else:
            logger.warning(f"无法获取 {test_city} 的Location ID")
        
        # 测试获取天气预报数据
        logger.info("测试获取天气预报数据...")
        if location_id:
            forecast_data = collector.get_forecast_weather(location_id)
            if forecast_data:
                logger.info(f"获取到 {len(forecast_data)} 天的天气预报数据")
                logger.info(f"明天的天气: {forecast_data[0]['textDay']}, 最高温: {forecast_data[0]['tempMax']}°C, 最低温: {forecast_data[0]['tempMin']}°C")
            else:
                logger.warning("无法获取天气预报数据")
        
        logger.info("测试完成")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    test_collector()
