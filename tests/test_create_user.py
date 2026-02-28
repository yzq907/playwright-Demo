import pytest
from playwright.sync_api import expect
from pages.user_page import UserPage
from utils.logger import get_logger


def test_create_user_after_login(logged_in_page, logger):
    """测试登录后创建用户 - 使用module级别登录fixture"""
    logger.info("开始执行登录后创建用户测试")
    
    # 第二步：导航到用户管理模块
    logger.info("第一步：导航到用户管理模块")
    user_page = UserPage(logged_in_page)
    user_page.navigate_to_user_module()
    
    # 第三步：点击添加用户按钮
    logger.info("第二步：点击添加用户按钮")
    user_page.click_add_user()
    
    # 第四步：填写用户信息
    logger.info("第三步：填写用户信息")
    new_user_data = {
        "username": "testuser001",
        "real_name": "testuser001",
        "password": "Test@123456"
    }
    user_page.fill_user_info(**new_user_data)
    
    # 第五步：保存用户
    logger.info("第四步：保存用户信息")
    user_page.save_user()
    
    # 第六步：等待保存完成
    logger.info("第五步：等待保存完成")
    user_page.wait_for_save_complete()
    
    logger.info("测试成功，用户创建流程完成")


def test_create_user_with_fixture(logged_in_page, logger):
    """使用 fixture 数据创建用户 - 使用module级别登录fixture"""
    logger.info("开始执行使用 fixture 数据创建用户测试")
    
    # 创建用户（使用完整流程）
    user_page = UserPage(logged_in_page)
    new_user_data = {
        "username": "testuser002",
        "real_name": "testuser002",
        "password": "Auto@123456"
    }
    
    logger.info("使用完整流程创建用户")
    user_page.create_user(new_user_data)
    
    logger.info("测试成功，用户创建完成")


def test_create_user_minimal_info(logged_in_page, logger):
    """测试只填写必要信息创建用户 - 使用module级别登录fixture"""
    logger.info("开始执行最小信息创建用户测试")
    
    # 创建用户（只填写必要信息）
    user_page = UserPage(logged_in_page)
    user_page.navigate_to_user_module()
    user_page.click_add_user()
    
    minimal_user_data = {
        "username": "testuser003",
        "real_name": "testuser003",
        "password": "Min@123456"
    }
    
    logger.info("只填写必要信息创建用户")
    user_page.fill_user_info(**minimal_user_data)
    user_page.save_user()
    user_page.wait_for_save_complete()
    
    logger.info("测试成功，最小信息用户创建完成")
