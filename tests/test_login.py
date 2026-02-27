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
    logger.info("验证登录后是否跳转到仪表盘")
    expect(page).to_have_url("/ztna-manager/menuController/queryMenus.do")
    logger.info("登录测试通过")