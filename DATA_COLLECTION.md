# 天气数据采集功能说明

## 概述

本项目已添加网络数据采集功能，可以从和风天气API获取实时和历史天气数据，而不是仅使用本地预下载的数据。

## 数据来源

使用**和风天气API**作为数据源，提供以下功能：
- 实时天气数据
- 天气预报数据
- 历史天气数据

## 准备工作

### 1. 获取API密钥

1. 访问 [和风天气开发者平台](https://dev.qweather.com/)
2. 注册账号并登录
3. 创建应用，获取API密钥（Key）

### 2. 安装依赖

确保已安装所有必要的依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：使用单独的采集脚本

使用 `collect_data.py` 脚本可以单独采集数据：

```bash
# 使用API密钥直接采集
python collect_data.py YOUR_API_KEY

# 采集指定日期范围的数据
python collect_data.py YOUR_API_KEY 2023-12-01 2023-12-31
```

### 方法二：在数据处理流程中集成采集

使用 `main.py` 脚本，可以在数据处理流程中集成网络采集：

```bash
# 使用API采集数据并处理
python main.py --use-api --api-key YOUR_API_KEY

# 使用API采集指定日期范围的数据并处理
python main.py --use-api --api-key YOUR_API_KEY --start-date 2023-12-01 --end-date 2023-12-31
```

### 方法三：使用环境变量

可以将API密钥设置为环境变量，避免在命令行中暴露：

```bash
# Windows PowerShell
$env:QWEATHER_API_KEY = "YOUR_API_KEY"

# Windows CMD
set QWEATHER_API_KEY=YOUR_API_KEY

# Linux/macOS
export QWEATHER_API_KEY=YOUR_API_KEY

# 然后执行命令
python main.py --use-api
```

## 功能说明

### 采集范围

- **默认采集范围**：最近7天的历史数据 + 未来3天的预报数据
- **可自定义范围**：通过 `--start-date` 和 `--end-date` 参数指定

### 数据存储

采集的数据将存储在 `data/cities_weather/cities_weather/` 目录下，与原有本地数据格式保持一致：
- 按城市分类存储
- 按年月命名的CSV文件
- GBK编码，确保中文显示正常

### 增量更新

采集器会自动检测现有数据，避免重复采集相同日期的数据。

## 代码结构

```
Weather_Analysis/
├── collector/                  # 数据采集模块
│   └── weather_api_collector.py  # 天气API采集器
├── data/                      # 数据存储目录
│   └── cities_weather/        # 城市天气数据
├── collect_data.py            # 数据采集主脚本
├── main.py                    # 数据处理主脚本（已集成采集功能）
└── test_collector.py          # 采集器测试脚本
```

## API限制

和风天气API有免费额度限制：
- 免费版：每天1000次调用
- 请合理规划采集频率和范围

## 注意事项

1. 请遵守和风天气API的使用条款
2. 避免频繁调用API，建议设置适当的时间间隔
3. 历史数据查询有时间限制，具体以API文档为准
4. 部分功能可能需要付费版API支持

## 测试

可以使用 `test_collector.py` 脚本测试采集功能：

```bash
# 设置环境变量后执行
python test_collector.py
```

## 集成到现有系统

采集功能已集成到现有数据处理流程中，可以无缝切换使用本地数据或API数据：

```python
from main import WeatherDataPipeline

# 使用本地数据
pipeline = WeatherDataPipeline()
pipeline.run_pipeline()

# 使用API数据
pipeline = WeatherDataPipeline()
pipeline.run_pipeline(use_api=True, api_key="YOUR_API_KEY")
```
