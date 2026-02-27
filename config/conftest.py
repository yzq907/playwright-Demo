# conftest.py
import pytest
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# 全局 fixture 可以在这里定义，但 pytest-playwright 已经提供了 `browser`、`context`、`page` 等 fixture
# 我们可以通过钩子函数设置默认的浏览器启动参数

def pytest_setup_options():
    """设置浏览器启动选项（可选）"""
    return {
        "headless": False,   # 默认无头模式，这里可以设为 False 方便调试
        "slow_mo": 500,       # 减慢操作速度（毫秒）
    }

@pytest.fixture(scope="session")
def base_url():
    """返回基础 URL，供测试使用"""
    return os.getenv("BASE_URL", "http://localhost:3000")

@pytest.fixture
def page(page, base_url):
    """扩展 page fixture，设置基础 URL"""
    page.set_default_navigation_timeout(30000)
    page.context.set_default_timeout(10000)
    # 可以将 base_url 存储到 page 对象上
    page.base_url = base_url
    return page