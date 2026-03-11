# conftest.py
import pytest
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.logger import get_logger, Logger
from pages.login_page import LoginPage
import allure

# 全局 fixture 可以在这里定义，但 pytest-playwright 已经提供了 `browser`、`context`、`page` 等 fixture

@pytest.fixture(scope="session")
def base_url():
    """返回基础 URL，供测试使用"""
    return os.getenv("BASE_URL", "http://10.10.27.171:7070")

@pytest.fixture(scope="module")
def page_module(browser, base_url):
    """Module级别的page fixture，用于module级别的登录fixture"""
    page = browser.new_page()
    page.set_default_navigation_timeout(30000)
    page.set_default_timeout(10000)
    page.base_url = base_url
    yield page
    page.close()

@pytest.fixture
def page(page, base_url):
    """扩展 page fixture，设置基础 URL"""
    page.set_default_navigation_timeout(30000)
    page.context.set_default_timeout(10000)
    # 可以将 base_url 存储到 page 对象上
    page.base_url = base_url
    return page

@pytest.fixture(scope="module")
def logged_in_page(page_module, user_data):
    """
    Module级别的登录fixture
    在每个测试模块运行前执行一次登录，该模块的所有测试共享登录状态
    避免测试代码中重复编写登录逻辑
    适用于需要登录后执行的测试用例
    """
    logger = get_logger("login_fixture")
    logger.info("执行module级别登录")
    
    login_page = LoginPage(page_module)
    login_page.navigate()
    
    user = user_data["valid_user"]
    logger.info(f"使用用户名: {user['username']} 进行登录")
    login_page.login(user["username"], user["password"])
    
    # 验证登录成功
    assert login_page.is_login_successful(), "登录失败"
    logger.info("登录成功，返回已登录的page对象")
    
    yield page_module
    
    # 如果需要，可以在这里添加登出逻辑
    # logger.info("执行登出操作")

@pytest.fixture(scope="module")
def user_data():
    with open("data/users.json") as f:
        return json.load(f)

@pytest.fixture
def logger(request):
    """提供日志记录器 fixture"""
    return get_logger(request.node.name)


def take_screenshot(page, test_name, outcome="passed"):
    """
    截图辅助函数
    
    Args:
        page: Playwright page对象
        test_name: 测试用例名称
        outcome: 测试结果 (passed/failed)
    
    Returns:
        str: 截图文件路径
    """
    try:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = test_name.replace("/", "_").replace("\\", "_").replace("::", "_").replace("[", "_").replace("]", "_")
        filename = f"{safe_test_name}_{outcome}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        page.screenshot(path=filepath, full_page=True)
        print(f"\n截图已保存: {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"\n截图失败: {e}")
        return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子函数，在每个测试执行完成后触发
    用于截图和记录测试结果
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        test_name = item.nodeid
        
        try:
            page = None
            
            if "page" in item.funcargs:
                page = item.funcargs["page"]
            elif "logged_in_page" in item.funcargs:
                page = item.funcargs["logged_in_page"]
            
            if page:
                outcome_str = "passed" if report.passed else "failed"
                screenshot_path = take_screenshot(page, test_name, outcome_str)
                
                if screenshot_path:
                    try:
                        allure.attach.file(
                            screenshot_path,
                            name=f"{outcome_str}_screenshot",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception as e:
                        print(f"\n附加截图到Allure报告失败: {e}")
                
        except Exception as e:
            print(f"\n截图钩子执行失败: {e}")