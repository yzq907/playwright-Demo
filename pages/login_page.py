# pages/login_page.py
from playwright.sync_api import Page
from utils.logger import get_logger

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(__name__)
        # 定位器
        self.username_input = page.locator("#stroperatorname")
        self.password_input = page.locator("#strpwd")
        self.login_button = page.locator("#submitButtom")
        self.logger.info("LoginPage 初始化完成")

    def navigate(self):
        """导航到登录页面（路径为 /ztna-manager/）"""
        url = f"{self.page.base_url}/ztna-manager/"
        self.logger.info(f"导航到登录页面: {url}")
        self.page.goto(url)
        self.logger.info("登录页面加载完成")

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.logger.info(f"开始登录操作，用户名: {username}")
        
        self.logger.debug("输入用户名")
        self.username_input.fill(username)
        
        self.logger.debug("输入密码")
        self.password_input.fill(password)
        
        self.logger.debug("点击登录按钮")
        self.login_button.click()
        
        self.logger.info("登录操作执行完成")