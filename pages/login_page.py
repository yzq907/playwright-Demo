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
        
        # 等待页面跳转或响应
        self.logger.info("等待登录响应...")
        try:
            # 等待页面跳转到登录后的页面（最多等待10秒）
            self.page.wait_for_url("**/menuController/**", timeout=10000)
            self.logger.info("检测到页面跳转，登录可能成功")
        except:
            # 如果没有跳转，可能登录失败，继续执行
            self.logger.debug("未检测到页面跳转，可能登录失败")
        
        self.logger.info("登录操作执行完成")
    
    def get_error_message(self):
        """获取登录失败时的错误提示信息"""
        self.logger.info("获取错误提示信息")
        
        # 尝试多种常见的错误提示定位器
        error_selectors = [
            ".error-message",
            ".alert-error",
            ".error",
            "[role='alert']",
            ".message-error",
            ".login-error",
            ".tips-error",
            ".msg-error"
        ]
        
        for selector in error_selectors:
            try:
                error_element = self.page.locator(selector)
                if error_element.is_visible(timeout=1000):
                    error_text = error_element.inner_text()
                    self.logger.info(f"找到错误提示: {error_text}")
                    return error_text
            except:
                continue
        
        # 如果没有找到错误提示元素，尝试查找包含错误关键字的文本
        error_keywords = ["错误", "失败", "无效", "用户名", "密码", "error", "invalid", "failed"]
        for keyword in error_keywords:
            try:
                error_element = self.page.get_by_text(keyword, exact=False)
                if error_element.is_visible(timeout=1000):
                    error_text = error_element.inner_text()
                    self.logger.info(f"找到错误提示: {error_text}")
                    return error_text
            except:
                continue
        
        self.logger.warning("未找到错误提示信息")
        return None
    
    def is_login_successful(self):
        """检查登录是否成功"""
        self.logger.info("检查登录是否成功")
        
        # 检查是否跳转到登录后的页面
        current_url = self.page.url
        self.logger.debug(f"当前URL: {current_url}")
        
        # 成功登录后会跳转到包含 menuController 的页面
        if "menuController" in current_url:
            self.logger.info("登录成功")
            return True
        
        # 或者检查是否仍在登录页面
        if "/ztna-manager/" in current_url and "menuController" not in current_url:
            self.logger.info("仍在登录页面，登录可能失败")
            return False
        
        return False