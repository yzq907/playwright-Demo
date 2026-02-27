# conftest.py
import pytest
import os
import json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.logger import get_logger, Logger

# 全局 fixture 可以在这里定义，但 pytest-playwright 已经提供了 `browser`、`context`、`page` 等 fixture

@pytest.fixture(scope="session")
def base_url():
    """返回基础 URL，供测试使用"""
    return os.getenv("BASE_URL", "http://10.10.27.171:7070")

@pytest.fixture
def page(page, base_url):
    """扩展 page fixture，设置基础 URL"""
    page.set_default_navigation_timeout(30000)
    page.context.set_default_timeout(10000)
    # 可以将 base_url 存储到 page 对象上
    page.base_url = base_url
    return page

@pytest.fixture
def user_data():
    with open("data/users.json") as f:
        return json.load(f)

@pytest.fixture
def logger(request):
    """提供日志记录器 fixture"""
    return get_logger(request.node.name)
