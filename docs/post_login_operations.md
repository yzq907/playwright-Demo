# 登录后操作测试使用说明

## 概述

本示例演示了如何在 Playwright 测试中实现"登录后才能操作"的场景。完整的流程包括：
1. 登录系统
2. 导航到用户管理模块
3. 点击添加用户按钮
4. 填写用户信息
5. 保存用户

## 文件结构

```
pages/
├── login_page.py      # 登录页面对象
└── user_page.py       # 用户管理页面对象

tests/
└── test_create_user.py # 创建用户测试用例
```

## 核心功能

### 1. LoginPage - 登录页面对象

**关键方法：**
- `navigate()` - 导航到登录页面
- `login(username, password)` - 执行登录操作（包含等待逻辑）
- `is_login_successful()` - 检查登录是否成功
- `get_error_message()` - 获取登录失败的错误提示

**改进点：**
- 登录后自动等待页面跳转（`wait_for_url`）
- 支持多种方式定位错误提示
- 详细的日志记录

### 2. UserPage - 用户管理页面对象

**关键方法：**
- `navigate_to_user_module()` - 导航到用户管理模块
- `click_add_user()` - 点击添加用户按钮
- `fill_user_info(username, real_name, password)` - 填写用户信息
- `save_user()` - 保存用户信息
- `wait_for_save_complete()` - 等待保存完成
- `create_user(user_data)` - 完整的创建用户流程

**定位器（根据实际HTML）：**
```python
# 用户菜单
self.user_menu = page.get_by_text("用户", exact=True)
self.user_menu_img = page.locator("img[title='用户']")

# 添加按钮
self.add_user_button = page.locator("#addChildrenMemberbtn")

# 表单字段
self.username_input = page.locator("#strusername_")
self.real_name_input = page.locator("#struserdes")
self.password_input = page.locator("#strpwd")

# 保存按钮
self.save_button = page.locator(".l-btn-text.save_icon")
```

## 测试用例示例

### test_create_user_after_login - 完整流程测试

```python
def test_create_user_after_login(page, user_data, logger):
    # 第一步：登录
    login_page = LoginPage(page)
    login_page.navigate()
    user = user_data["valid_user"]
    login_page.login(user["username"], user["password"])
    assert login_page.is_login_successful(), "登录失败，无法继续测试"
    
    # 第二步：导航到用户管理模块
    user_page = UserPage(page)
    user_page.navigate_to_user_module()
    
    # 第三步：点击添加用户按钮
    user_page.click_add_user()
    
    # 第四步：填写用户信息
    new_user_data = {
        "username": "testuser001",
        "real_name": "测试用户",
        "password": "Test@123456"
    }
    user_page.fill_user_info(**new_user_data)
    
    # 第五步：保存用户
    user_page.save_user()
    
    # 第六步：等待保存完成
    user_page.wait_for_save_complete()
```

### test_create_user_with_fixture - 使用 fixture 数据

```python
def test_create_user_with_fixture(page, user_data, logger):
    # 登录
    login_page = LoginPage(page)
    login_page.navigate()
    user = user_data["valid_user"]
    login_page.login(user["username"], user["password"])
    
    # 创建用户（使用完整流程）
    user_page = UserPage(page)
    new_user_data = {
        "username": "testuser002",
        "real_name": "自动化测试用户",
        "password": "Auto@123456"
    }
    user_page.create_user(new_user_data)
```

## 运行测试

### 运行单个测试
```bash
pytest tests/test_create_user.py::test_create_user_after_login --headed -v
```

### 运行所有创建用户测试
```bash
pytest tests/test_create_user.py --headed -v
```

### 使用主程序运行
```bash
python main.py --headed
```

## 关键要点

### 1. 登录后的等待

登录后需要等待页面跳转：
```python
# 在 login() 方法中
self.page.wait_for_url("**/menuController/**", timeout=10000)
```

### 2. 页面加载等待

导航到新页面后需要等待加载完成：
```python
# 等待网络空闲
self.page.wait_for_load_state("networkidle", timeout=10000)
```

### 3. 多种定位方式

为了提高稳定性，使用多种定位方式：
```python
try:
    # 方式1：通过ID
    self.add_user_button.click()
except:
    try:
        # 方式2：通过文本
        self.add_button_text.click()
    except:
        # 方式3：直接导航
        self.page.goto(url)
```

### 4. 详细的日志

每个步骤都有详细的日志记录：
```python
logger.info("第一步：登录系统")
logger.info("第二步：导航到用户管理模块")
logger.info("第三步：点击添加用户按钮")
```

## 测试数据

### users.json
```json
{
  "valid_user": {
    "username": "sysadmin",
    "password": "Emm@2025"
  },
  "invalid_user": {
    "username": "wrong",
    "password": "wrongpass"
  }
}
```

### 测试用例中的用户数据
```python
new_user_data = {
    "username": "testuser001",
    "real_name": "测试用户",
    "password": "Test@123456"
}
```

## 扩展建议

### 1. 添加更多测试场景
- 测试必填字段验证
- 测试用户名重复
- 测试密码强度验证
- 测试编辑用户
- 测试删除用户

### 2. 使用数据驱动测试
```python
@pytest.mark.parametrize("user_data", [
    {"username": "user1", "real_name": "用户1", "password": "Pass@123"},
    {"username": "user2", "real_name": "用户2", "password": "Pass@456"},
])
def test_create_multiple_users(page, user_data, logger):
    # 测试逻辑
```

### 3. 使用 Faker 生成测试数据
```python
from faker import Faker

fake = Faker()
new_user_data = {
    "username": fake.user_name(),
    "real_name": fake.name(),
    "password": fake.password()
}
```

## 常见问题

### 1. 元素定位失败
- 检查元素是否在 iframe 中
- 检查元素是否动态加载
- 增加等待时间

### 2. 页面加载超时
- 增加 `wait_for_load_state` 的超时时间
- 检查网络连接
- 使用 `--headed` 模式查看实际情况

### 3. 登录后操作失败
- 确认登录成功（使用 `is_login_successful()`）
- 检查是否有权限限制
- 确认页面 URL 正确

## 总结

本示例展示了如何在 Playwright 中实现需要登录的操作流程：
- ✅ 登录验证
- ✅ 页面导航
- ✅ 表单填写
- ✅ 数据保存
- ✅ 详细的日志记录
- ✅ 稳定的元素定位
