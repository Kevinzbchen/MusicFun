# MusicFun - 音乐平台数据爬虫项目

MusicFun 是一个多平台音乐数据爬虫项目，旨在从各大音乐平台收集和分析音乐数据。目前支持网易云音乐，未来将扩展支持更多音乐平台。

## 🎯 项目特性

- **多平台支持**: 目前支持网易云音乐，架构设计支持快速扩展其他平台
- **模块化设计**: 清晰的代码结构，易于维护和扩展
- **异步支持**: 使用 asyncio 和 aiohttp 实现高性能异步爬取
- **数据验证**: 使用 Pydantic 进行数据验证和序列化
- **完整日志**: 使用 Loguru 提供详细的日志记录
- **配置管理**: 支持环境变量和配置文件管理

## 📁 项目结构

```
MusicFun/
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── core/              # 核心模块
│   │   ├── __init__.py
│   │   ├── base_crawler.py    # 基础爬虫类
│   │   ├── config.py          # 配置管理
│   │   ├── logger.py          # 日志配置
│   │   └── models.py          # 数据模型
│   ├── platforms/         # 各平台爬虫
│   │   ├── __init__.py
│   │   └── netease/       # 网易云音乐
│   │       ├── __init__.py
│   │       ├── crawler.py     # 爬虫实现
│   │       ├── api.py         # API 接口
│   │       └── models.py      # 平台特定模型
│   ├── utils/             # 工具函数
│   │   ├── __init__.py
│   │   ├── http_client.py     # HTTP 客户端
│   │   ├── rate_limiter.py    # 速率限制
│   │   └── data_processor.py  # 数据处理
│   └── storage/           # 数据存储
│       ├── __init__.py
│       ├── database.py        # 数据库操作
│       └── file_storage.py    # 文件存储
├── tests/                 # 测试目录
├── config/                # 配置文件
│   ├── default.yaml      # 默认配置
│   └── development.yaml  # 开发环境配置
├── scripts/              # 脚本目录
├── data/                 # 数据目录（git忽略）
├── logs/                 # 日志目录（git忽略）
├── requirements.txt      # 依赖包列表
├── .env.example          # 环境变量示例
├── .gitignore           # Git忽略文件
└── README.md            # 项目说明
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.8+，然后安装依赖：

```bash
# 克隆项目
git clone <repository-url>
cd MusicFun

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制环境变量示例文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置必要的环境变量。

### 3. 运行示例

```python
# 示例代码：运行网易云音乐爬虫
from src.platforms.netease.crawler import NeteaseCrawler

async def main():
    crawler = NeteaseCrawler()
    # 获取热门歌曲
    songs = await crawler.get_hot_songs(limit=10)
    for song in songs:
        print(f"{song.title} - {song.artist}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 📦 依赖说明

主要依赖包及其用途：

| 包名 | 版本 | 用途 |
|------|------|------|
| requests | >=2.31.0 | HTTP 请求库 |
| beautifulsoup4 | >=4.12.2 | HTML 解析 |
| pandas | >=2.1.0 | 数据处理和分析 |
| pydantic | >=2.4.0 | 数据验证和序列化 |
| loguru | >=0.7.2 | 日志记录 |
| aiohttp | >=3.9.0 | 异步 HTTP 客户端 |
| python-dotenv | >=1.0.0 | 环境变量管理 |
| tenacity | >=8.2.0 | 重试机制 |

完整依赖列表请查看 [requirements.txt](./requirements.txt)。

## 🔧 配置说明

项目支持多种配置方式：

1. **环境变量**: 通过 `.env` 文件配置
2. **YAML 配置文件**: 在 `config/` 目录下
3. **代码配置**: 在 `src/core/config.py` 中定义

### 主要配置项

```yaml
# config/default.yaml
debug: false
log_level: "INFO"

netease:
  base_url: "https://music.163.com"
  api_url: "https://music.163.com/api"
  timeout: 30
  retry_times: 3

http:
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  proxy: null
  verify_ssl: true

storage:
  database_url: "sqlite:///data/music.db"
  export_format: "json"  # json, csv, excel
```

## 📊 数据模型

项目使用 Pydantic 定义数据模型，确保数据的一致性和验证：

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Song(BaseModel):
    """歌曲信息"""
    id: str
    title: str
    artist: str
    album: Optional[str] = None
    duration: Optional[int] = None  # 时长（秒）
    play_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    release_date: Optional[datetime] = None
    platform: str  # 平台标识，如 "netease"
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
```

## 🧪 测试

运行测试：

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_netease.py

# 生成测试覆盖率报告
pytest --cov=src tests/
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 flake8 进行代码检查
- 使用 mypy 进行类型检查

```bash
# 格式化代码
black src/

# 排序导入
isort src/

# 代码检查
flake8 src/

# 类型检查
mypy src/
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本项目仅用于学习和研究目的。请遵守各音乐平台的服务条款，不要过度请求以免对服务器造成压力。开发者不对使用本项目造成的任何问题负责。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 参与讨论

---

**Happy Crawling! 🎵**
