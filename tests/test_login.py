# tests/test_login.py
import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from utils.logger import get_logger

def test_valid_login(page, user_data, logger):
    logger.info("开始执行登录测试")
    
    login_page = LoginPage(page)
    logger.info("导航到登录页面")
    login_page.navigate()
    
    user = user_data["valid_user"]
    logger.info(f"使用用户名: {user['username']} 进行登录")
    
    login_page.login(user["username"], user["password"])
    logger.info("登录操作完成")
    
    # 断言登录后跳转到仪表盘
    logger.info("验证登录后是否跳转正确页面")
    expect(page).to_have_url("/ztna-manager/menuController/queryMenus.do")
    logger.info("测试成功，用户登录成功")

def test_invalid_login(page, user_data, logger):
    logger.info("开始执行登录失败测试")
    
    login_page = LoginPage(page)
    logger.info("导航到登录页面")
    login_page.navigate()
    
    user = user_data["invalid_user"]
    logger.info(f"使用无效用户名: {user['username']} 进行登录")
    
    login_page.login(user["username"], user["password"])
    logger.info("登录操作完成")
    
    # 等待页面响应
    page.wait_for_timeout(1000)
    
    # 检查登录是否失败
    is_success = login_page.is_login_successful()
    
    if is_success:
        logger.error("预期登录失败，但实际登录成功")
        pytest.fail("使用无效凭据不应该登录成功")
    else:
        logger.info("确认登录失败，符合预期")
        
        # 获取错误提示信息
        error_message = login_page.get_error_message()
        
        if error_message:
            logger.info(f"页面显示错误提示: {error_message}")
            # 断言错误提示包含相关信息（支持中英文）
            error_keywords = ["错误", "失败", "无效", "error", "invalid", "failed", "incorrect"]
            assert any(keyword in error_message.lower() for keyword in error_keywords), \
                f"错误提示应该包含相关关键字，实际内容: {error_message}"
        else:
            logger.warning("未找到明确的错误提示信息")
            # 如果没有找到错误提示，至少验证仍在登录页面
            current_url = page.url
            assert "/ztna-manager/" in current_url and "menuController" not in current_url, \
                f"登录失败后应该仍在登录页面，当前URL: {current_url}"
        
        logger.info("测试成功，验证了登录失败场景")