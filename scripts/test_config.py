"""
测试配置文件
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings


def test_basic_config():
    """测试基础配置"""
    print("=== MusicFun 配置测试 ===\n")
    
    # 测试项目基础配置
    print(f"1. 项目信息:")
    print(f"   项目名称: {settings.project_name}")
    print(f"   版本: {settings.version}")
    print(f"   调试模式: {settings.debug}")
    
    # 测试路径配置
    print(f"\n2. 路径配置:")
    print(f"   项目根目录: {settings.base_dir}")
    print(f"   源码目录: {settings.src_dir}")
    print(f"   配置目录: {settings.config_dir}")
    print(f"   数据目录: {settings.data_dir}")
    print(f"   日志目录: {settings.log_dir}")
    
    # 测试目录是否存在
    print(f"\n3. 目录检查:")
    for name, path in [
        ("数据目录", settings.data_dir),
        ("日志目录", settings.log_dir),
        ("导出目录", settings.export_dir),
        ("备份目录", settings.backup_dir),
    ]:
        exists = "存在" if path.exists() else "不存在"
        print(f"   {name}: {path} ({exists})")
    
    # 测试平台配置
    print(f"\n4. 平台配置:")
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
    print(f"\n5. 存储配置:")
    print(f"   存储格式: {settings.storage.format.value}")
    print(f"   数据库URL: {settings.storage.database_url}")
    print(f"   数据目录: {settings.storage.data_dir}")
    print(f"   导出目录: {settings.storage.export_dir}")
    print(f"   备份目录: {settings.storage.backup_dir}")
    print(f"   自动备份: {settings.storage.auto_backup}")
    
    # 测试日志配置
    print(f"\n6. 日志配置:")
    print(f"   日志级别: {settings.log.level.value}")
    print(f"   日志目录: {settings.log.log_dir}")
    print(f"   日志文件: {settings.log.log_file}")
    print(f"   错误日志: {settings.log.error_file}")
    print(f"   最大文件: {settings.log.max_file_size}")
    print(f"   备份数量: {settings.log.backup_count}")
    print(f"   轮转周期: {settings.log.rotation}")
    print(f"   控制台输出: {settings.log.console_output}")
    print(f"   文件输出: {settings.log.file_output}")
    
    # 测试环境变量
    print(f"\n7. 环境变量测试:")
    import os
    env_vars = [
        "DEBUG",
        "NETEASE_COOKIES",
        "NETEASE_PROXY",
        "SPIDER_PROXY",
        "DATABASE_URL",
        "LOG_LEVEL",
    ]
    
    for env_var in env_vars:
        value = os.getenv(f"MUSICFUN_{env_var}")
        if value:
            preview = value[:50] + "..." if len(value) > 50 else value
            print(f"   MUSICFUN_{env_var}: {preview}")
        else:
            print(f"   MUSICFUN_{env_var}: 未设置")
    
    print(f"\n=== 配置测试完成 ===")
    return True


def test_yaml_save_load():
    """测试YAML配置保存和加载"""
    print(f"\n=== YAML配置测试 ===")
    
    # 保存配置到YAML
    yaml_file = settings.config_dir / "test_settings.yaml"
    settings.save_to_yaml(yaml_file)
    print(f"1. 配置已保存到: {yaml_file}")
    
    # 从YAML加载配置
    from config.settings import Settings
    loaded_settings = Settings.load_from_yaml(yaml_file)
    print(f"2. 配置已从YAML加载")
    
    # 验证加载的配置
    print(f"3. 验证加载的配置:")
    print(f"   项目名称: {loaded_settings.project_name}")
    print(f"   版本: {loaded_settings.version}")
    print(f"   平台数量: {len(loaded_settings.platforms)}")
    
    # 清理测试文件
    if yaml_file.exists():
        yaml_file.unlink()
        print(f"4. 测试文件已清理")
    
    print(f"\n=== YAML测试完成 ===")
    return True


if __name__ == "__main__":
    try:
        test_basic_config()
        test_yaml_save_load()
        print(f"\n所有测试通过！")
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
