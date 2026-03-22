"""
简单配置测试
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings

print("=== MusicFun 配置测试 ===")
print()

# 测试项目基础配置
print("1. 项目信息:")
print(f"   项目名称: {settings.project_name}")
print(f"   版本: {settings.version}")
print(f"   调试模式: {settings.debug}")

# 测试路径配置
print("\n2. 路径配置:")
print(f"   项目根目录: {settings.base_dir}")
print(f"   源码目录: {settings.src_dir}")
print(f"   配置目录: {settings.config_dir}")
print(f"   数据目录: {settings.data_dir}")
print(f"   日志目录: {settings.log_dir}")

# 测试目录是否存在
print("\n3. 目录检查:")
for name, path in [
    ("数据目录", settings.data_dir),
    ("日志目录", settings.log_dir),
    ("导出目录", settings.export_dir),
    ("备份目录", settings.backup_dir),
]:
    exists = "存在" if path.exists() else "不存在"
    print(f"   {name}: {path} ({exists})")

# 测试平台配置
print("\n4. 平台配置:")
for platform_name, platform_config in settings.platforms.items():
    print(f"   {platform_name.upper()}:")
    print(f"     启用: {platform_config.enabled}")
    print(f"     基础URL: {platform_config.base_url}")
    print(f"     API URL: {platform_config.api_url}")
    print(f"     超时: {platform_config.timeout}s")
    print(f"     重试次数: {platform_config.retry_times}")
    print(f"     请求间隔: {platform_config.request_delay}s")
    
    if platform_config.cookies:
        cookie_preview = platform_config.cookies[:50] + "..." if len(platform_config.cookies) > 50 else platform_config.cookies
        print(f"     Cookie: {cookie_preview}")
    else:
        print(f"     Cookie: 未设置")

# 测试存储配置
print("\n5. 存储配置:")
print(f"   存储格式: {settings.storage.format.value}")
print(f"   数据库URL: {settings.storage.database_url}")
print(f"   数据目录: {settings.storage.data_dir}")
print(f"   导出目录: {settings.storage.export_dir}")
print(f"   备份目录: {settings.storage.backup_dir}")
print(f"   自动备份: {settings.storage.auto_backup}")

# 测试日志配置
print("\n6. 日志配置:")
print(f"   日志级别: {settings.log.level.value}")
print(f"   日志目录: {settings.log.log_dir}")
print(f"   日志文件: {settings.log.log_file}")
print(f"   错误日志: {settings.log.error_file}")
print(f"   最大文件: {settings.log.max_file_size}")
print(f"   备份数量: {settings.log.backup_count}")
print(f"   轮转周期: {settings.log.rotation}")
print(f"   控制台输出: {settings.log.console_output}")
print(f"   文件输出: {settings.log.file_output}")

print("\n=== 配置测试完成 ===")
print("\n所有配置加载成功！")
