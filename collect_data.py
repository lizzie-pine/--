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

def main():
    """
    天气数据采集主脚本
    """
    try:
        # 检查是否提供了API密钥
        if len(sys.argv) < 2:
            api_key = os.environ.get('QWEATHER_API_KEY')
            if not api_key:
                print("Usage: python collect_data.py <API_KEY> [start_date] [end_date]")
                print("Or set QWEATHER_API_KEY environment variable")
                sys.exit(1)
        else:
            api_key = sys.argv[1]
        
        # 解析日期参数
        start_date = None
        end_date = None
        
        if len(sys.argv) >= 4:
            start_date = sys.argv[2]
            end_date = sys.argv[3]
        
        # 创建采集器实例
        collector = WeatherDataCollector(api_key=api_key)
        
        if start_date and end_date:
            # 采集指定日期范围的历史数据
            logger.info(f"Collecting historical data from {start_date} to {end_date}")
            collector.collect_historical_data(start_date, end_date)
        else:
            # 默认采集最近7天的历史数据和未来3天的预报数据
            from datetime import datetime, timedelta
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            logger.info(f"Collecting historical data from {start_date} to {end_date}")
            collector.collect_historical_data(start_date, end_date)
            
            logger.info("Collecting forecast data for the next 3 days")
            collector.collect_forecast_data()
        
        logger.info("Data collection completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data collection: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
