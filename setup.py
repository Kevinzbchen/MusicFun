"""
项目安装配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README.md 内容
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "MusicFun - 音乐平台数据爬虫项目"

# 读取 requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = []

setup(
    name="musicfun",
    version="1.0.0",
    author="MusicFun Team",
    author_email="",
    description="多平台音乐数据爬虫项目",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(include=["src", "src.*", "config", "config.*"]),
    package_dir={
        "": ".",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
            "pre-commit>=3.5.0",
        ],
        "full": [
            "aiohttp>=3.9.0",
            "httpx>=0.25.0",
            "sqlalchemy>=2.0.0",
            "openpyxl>=3.1.2",
            "cryptography>=41.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "musicfun=src.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
