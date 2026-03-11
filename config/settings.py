"""
测试配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """测试配置类"""
    
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:7070")
    
    # 浏览器配置
    BROWSER_TIMEOUT = 30000
    NAVIGATION_TIMEOUT = 30000
    ELEMENT_TIMEOUT = 10000
    
    # 截图配置
    SCREENSHOT_DIR = "screenshots"
    SCREENSHOT_FULL_PAGE = True
    
    # Allure配置
    ALLURE_RESULTS_DIR = "allure-results"
    
    @classmethod
    def get_base_url(cls):
        """获取基础URL"""
        return cls.BASE_URL