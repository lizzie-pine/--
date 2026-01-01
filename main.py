import logging
import sys
from pathlib import Path
from processor.process_daily_data import WeatherDataProcessor
from processor.process_monthly_data import MonthlyDataProcessor
from processor.process_yearly_data import YearlyDataProcessor
from processor.process_province_data import ProvinceDataProcessor
from processor.process_statistic_data import StatisticsProcessor
from processor.process_comfort_cities import ComfortCitiesProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeatherDataPipeline:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.database_dir = self.base_dir / 'database'
        
        self.database_dir.mkdir(exist_ok=True)
        
        # 只初始化不需要依赖文件的处理器
        self.daily_processor = WeatherDataProcessor()

    def collect_data_from_api(self, api_key, start_date=None, end_date=None):
        """从API采集天气数据
        
        Args:
            api_key: 和风天气API密钥
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            
        Returns:
            采集的数据量
        """
        from collector.weather_api_collector import WeatherDataCollector
        
        try:
            logger.info("Starting data collection from API...")
            collector = WeatherDataCollector(api_key=api_key)
            
            collected_count = 0
            
            if start_date and end_date:
                # 采集指定日期范围的历史数据
                logger.info(f"Collecting historical data from {start_date} to {end_date}")
                collected_count += collector.collect_historical_data(start_date, end_date)
            else:
                # 默认采集最近7天的历史数据和未来3天的预报数据
                from datetime import datetime, timedelta
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                
                logger.info(f"Collecting historical data from {start_date} to {end_date}")
                collected_count += collector.collect_historical_data(start_date, end_date)
                
                logger.info("Collecting forecast data for the next 3 days")
                collected_count += collector.collect_forecast_data()
            
            logger.info(f"Data collection from API completed. Collected {collected_count} records")
            return collected_count
        except Exception as e:
            logger.error(f"Error collecting data from API: {e}")
            raise

    def run_pipeline(self, use_api=False, api_key=None, start_date=None, end_date=None):
        """运行完整的数据处理流水线
        
        Args:
            use_api: 是否使用API采集数据
            api_key: 和风天气API密钥
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Starting data processing pipeline...")
            
            # 如果启用API采集，先采集数据
            if use_api:
                if not api_key:
                    raise ValueError("API key is required when use_api is True")
                self.collect_data_from_api(api_key, start_date, end_date)

            # 1. 处理每日数据
            logger.info("Processing daily data...")
            daily_df = self.daily_processor.process_data()

            # 2. 处理月度数据 - 此时daily_data.csv已经创建完成
            logger.info("Processing monthly data...")
            from processor.process_monthly_data import MonthlyDataProcessor
            monthly_processor = MonthlyDataProcessor()
            monthly_df = monthly_processor.process_monthly_data()

            # 3. 处理年度数据
            logger.info("Processing yearly data...")
            from processor.process_yearly_data import YearlyDataProcessor
            yearly_processor = YearlyDataProcessor()
            yearly_df = yearly_processor.process_yearly_data()

            # 4. 处理省份数据
            logger.info("Processing province data...")
            from processor.process_province_data import ProvinceDataProcessor
            province_processor = ProvinceDataProcessor()
            province_df = province_processor.process_province_data()

            # 5. 处理统计数据
            logger.info("Processing statistics data...")
            from processor.process_statistic_data import StatisticsProcessor
            statistics_processor = StatisticsProcessor()
            statistics_processor.calculate_monthly_stats()

            # 6. 处理舒适城市数据
            logger.info("Processing comfort cities data...")
            from processor.process_comfort_cities import ComfortCitiesProcessor
            comfort_processor = ComfortCitiesProcessor()
            comfort_cities = comfort_processor.process_comfort_cities()

            logger.info("Data processing pipeline completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="China Cities Weather Analysis System")
    parser.add_argument("--use-api", action="store_true", help="Use API to collect weather data")
    parser.add_argument("--api-key", type=str, help="API key for weather data service")
    parser.add_argument("--start-date", type=str, help="Start date for data collection (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date for data collection (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    try:
        pipeline = WeatherDataPipeline()
        pipeline.run_pipeline(
            use_api=args.use_api,
            api_key=args.api_key,
            start_date=args.start_date,
            end_date=args.end_date
        )
        logger.info("Pipeline execution completed successfully")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        exit(1)
