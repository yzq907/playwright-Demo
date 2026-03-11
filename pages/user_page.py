from playwright.sync_api import Page, expect
from utils.logger import get_logger
import time


class UserPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(__name__)
        
        # 主页面中的定位器（导航用）
        self.user_menu = page.get_by_text("用户", exact=True)
        self.user_menu_img = page.locator("img[title='用户']")
        
        # 创建 iframe 定位器（所有表单操作都在 iframe 中）
        self.iframe_locator = page.frame_locator("iframe#mainframe")
        
        # 在 iframe 中的定位器
        self.add_user_button = self.iframe_locator.locator("#addChildrenMemberbtn")
        self.add_button_text = self.iframe_locator.get_by_text("添加", exact=True)
        
        # 用户信息表单定位器
        self.username_input = self.iframe_locator.locator("#strusername_")
        self.real_name_input = self.iframe_locator.locator("#struserdes")
        self.password_input = self.iframe_locator.locator("#strpwd")
        self.auto_generate_pwd_checkbox = self.iframe_locator.locator("#autopsw")
        
        # 保存按钮定位器
        self.save_button = self.iframe_locator.locator(".l-btn-text.save_icon")
        self.save_button_text = self.iframe_locator.get_by_text("保存", exact=True)
        
        self.logger.info("UserPage 初始化完成")
    
    def navigate_to_user_module(self):
        """导航到用户管理模块（在主页面中）"""
        self.logger.info("导航到用户管理模块")
        
        # 尝试多种方式定位用户管理菜单（在主页面中）
        try:
            # 方式1：通过文本查找
            self.logger.debug("尝试通过文本查找用户菜单")
            self.user_menu.click(timeout=5000)
        except:
            try:
                # 方式2：通过图片标题查找
                self.logger.debug("尝试通过图片标题查找用户菜单")
                self.user_menu_img.click(timeout=5000)
            except:
                # 方式3：通过 URL 直接导航
                self.logger.debug("尝试直接导航到用户管理页面")
                self.page.goto(f"{self.page.base_url}/ztna-manager/userController/toList.do")
        
        # 等待页面加载
        self.logger.info("等待用户管理页面加载")
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.logger.info("用户管理页面加载完成")
        
        # 额外等待，确保 iframe 加载
        self.logger.debug("等待 iframe 加载")
        self.page.wait_for_timeout(2000)   
    
    def click_add_user(self):
        """点击添加用户按钮（在 iframe 中）"""
        self.logger.info("点击添加用户按钮")
        
        # 尝试确保iframe已加载，但不阻塞操作
        try:
            self.logger.debug("检查iframe状态")
            iframe = self.page.frame("mainframe")
            if iframe:
                self.logger.info("iframe已就绪")
            else:
                self.logger.warning("iframe未找到，但继续尝试操作")
        except Exception as e:
            self.logger.warning(f"iframe检查失败: {str(e)}，继续尝试操作")
        
        # 尝试多种方式点击添加按钮
        success = False
        
        # 方式1：通过iframe_locator直接查找
        try:
            self.logger.debug("方式1：通过iframe_locator查找添加按钮")
            self.add_user_button.wait_for(state="visible", timeout=20000)
            self.logger.info("找到添加按钮，准备点击")
            
            # 滚动到元素
            self.add_user_button.scroll_into_view_if_needed()
            
            # 点击
            self.add_user_button.click()
            self.logger.info("方式1：成功点击添加按钮")
            success = True
        except Exception as e:
            self.logger.warning(f"方式1失败: {str(e)}")
        
        # 方式2：通过文本点击
        if not success:
            try:
                self.logger.debug("方式2：尝试通过文本点击添加按钮")
                self.add_button_text.wait_for(state="visible", timeout=15000)
                self.add_button_text.click()
                self.logger.info("方式2：通过文本成功点击添加按钮")
                success = True
            except Exception as e:
                self.logger.warning(f"方式2失败: {str(e)}")
        
        # 方式3：直接通过iframe对象定位
        if not success:
            try:
                self.logger.debug("方式3：尝试通过iframe直接定位")
                iframe = self.page.frame("mainframe")
                if iframe:
                    add_btn = iframe.locator("#addChildrenMemberbtn")
                    add_btn.wait_for(state="visible", timeout=15000)
                    add_btn.click()
                    self.logger.info("方式3：通过iframe直接定位成功点击添加按钮")
                    success = True
                else:
                    self.logger.warning("方式3：iframe未找到")
            except Exception as e:
                self.logger.warning(f"方式3失败: {str(e)}")
        
        # 方式4：使用JavaScript强制点击
        if not success:
            try:
                self.logger.debug("方式4：尝试使用JavaScript点击")
                iframe = self.page.frame("mainframe")
                if iframe:
                    iframe.evaluate("""() => {
                        const btn = document.querySelector('#addChildrenMemberbtn');
                        if (btn) btn.click();
                    }""")
                    self.logger.info("方式4：JavaScript点击成功")
                    success = True
                else:
                    self.logger.warning("方式4：iframe未找到")
            except Exception as e:
                self.logger.warning(f"方式4失败: {str(e)}")
        
        if not success:
            self.logger.error("所有点击添加按钮的方式都失败")
            raise Exception("未找到添加用户按钮")
        
        # 等待表单加载
        self.logger.info("等待用户表单加载")
        self.page.wait_for_timeout(2000)
        
        # 等待用户名输入框出现
        try:
            self.iframe_locator.wait_for_selector("#strusername_", timeout=10000)
            self.logger.info("用户表单已加载")
        except:
            self.logger.warning("未找到用户名输入框，可能表单未正确加载")
    
    def fill_user_info(self, username, real_name=None, password=None):
        """填写用户基本信息（在 iframe 中）"""
        self.logger.info(f"填写用户信息：用户名={username}, 姓名={real_name}")
        
        try:
            # 填写用户名
            if username:
                self.logger.debug("填写用户名")
                self.username_input.fill(username)
            
            # 填写真实姓名
            if real_name:
                self.logger.debug("填写真实姓名")
                self.real_name_input.fill(real_name)
            
            # 填写密码
            if password:
                self.logger.debug("填写密码")
                self.password_input.fill(password)
            
            self.logger.info("用户信息填写完成")
        except Exception as e:
            self.logger.error(f"填写表单失败: {str(e)}")
            raise
    
    def save_user(self):
        """保存用户信息（在 iframe 中）"""
        self.logger.info("点击保存按钮")
        
        try:
            # 在 iframe 中定位保存按钮
            # 尝试通过 class 查找
            try:
                self.logger.debug("尝试通过 class 查找保存按钮")
                self.save_button.wait_for(state="visible", timeout=5000)
                self.logger.info("通过 class 找到保存按钮")
                self.save_button.click()
            except:
                # 尝试通过文本查找
                self.logger.debug("尝试通过文本查找保存按钮")
                self.save_button_text.wait_for(state="visible", timeout=5000)
                self.save_button_text.click()
            
            self.logger.info("保存按钮点击成功")
        except Exception as e:
            self.logger.error(f"点击保存按钮失败: {str(e)}")
            raise
    
    def wait_for_save_complete(self):
        """等待保存完成"""
        self.logger.info("等待保存操作完成")
        
        # 等待可能的加载动画或提示消失
        self.page.wait_for_timeout(2000)
        
        # 检查是否有成功提示
        try:
            success_message = self.iframe_locator.get_by_text("成功", exact=False)
            if success_message.is_visible(timeout=3000):
                self.logger.info("检测到保存成功提示")
        except:
            self.logger.debug("未检测到明确的成功提示")
        
        self.logger.info("保存操作完成")
    
    def create_user(self, user_data):
        """创建用户的完整流程"""
        self.logger.info("开始创建用户流程")
        
        self.navigate_to_user_module()
        self.click_add_user()
        self.fill_user_info(
            username=user_data.get("username"),
            real_name=user_data.get("real_name"),
            password=user_data.get("password")
        )
        self.save_user()
        self.wait_for_save_complete()
        
        self.logger.info("用户创建流程完成")
