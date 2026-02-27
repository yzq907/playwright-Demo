# 日志模块使用说明

## 功能特性

- ✅ 同时输出到控制台和文件
- ✅ 详细的日志格式（包含时间、模块、级别、文件名、行号、函数名）
- ✅ 自动按日期分割日志文件
- ✅ 日志文件自动轮转（最大10MB，保留5个备份）
- ✅ 支持自定义日志级别和输出目录
- ✅ 提供装饰器记录函数调用和执行时间

## 日志格式

```
2026-02-27 17:17:45 - pages.login_page - INFO - [login_page.py:18] - navigate() - 导航到登录页面: http://10.10.27.171:7070/ztna-manager/
```

格式说明：
- `2026-02-27 17:17:45` - 时间戳
- `pages.login_page` - 模块名称
- `INFO` - 日志级别
- `[login_page.py:18]` - 文件名和行号
- `navigate()` - 函数名
- `导航到登录页面...` - 日志消息

## 基本使用

### 1. 在测试文件中使用

```python
from utils.logger import get_logger

def test_example(logger):
    logger.info("这是一条普通信息")
    logger.debug("这是一条调试信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
```

### 2. 在页面对象中使用

```python
from utils.logger import get_logger

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.logger = get_logger(__name__)
        self.logger.info("LoginPage 初始化完成")
    
    def navigate(self):
        self.logger.info("导航到登录页面")
        self.page.goto("/login")
```

### 3. 使用装饰器

#### 记录函数调用

```python
from utils.logger import log_function_call

@log_function_call
def my_function(arg1, arg2):
    pass
```

#### 记录执行时间

```python
from utils.logger import log_execution_time

@log_execution_time
def slow_function():
    import time
    time.sleep(2)
```

## 高级使用

### 1. 自定义日志记录器

```python
from utils.logger import Logger
import logging

logger = Logger.get_logger(
    name="custom_logger",
    level=logging.DEBUG,
    log_dir="logs",
    log_file="custom.log"
)
```

### 2. 设置日志级别

```python
from utils.logger import Logger
import logging

# 设置所有日志记录器的级别为 DEBUG
Logger.set_level(logging.DEBUG)
```

### 3. 日志级别说明

- `DEBUG` - 调试信息，详细信息
- `INFO` - 一般信息
- `WARNING` - 警告信息
- `ERROR` - 错误信息
- `CRITICAL` - 严重错误

## 日志文件

- 日志文件位置：`logs/` 目录
- 文件命名：`app_YYYYMMDD.log`（例如：`app_20260227.log`）
- 文件大小：最大 10MB
- 备份文件：保留最近 5 个备份

## 在项目中已集成的模块

- ✅ `conftest.py` - 提供 logger fixture
- ✅ `tests/test_login.py` - 测试文件中使用日志
- ✅ `pages/login_page.py` - 页面对象中使用日志

## 示例输出

```
2026-02-27 17:17:45 - test_valid_login[chromium] - INFO - [test_login.py:8] - test_valid_login() - 开始执行登录测试
2026-02-27 17:17:45 - pages.login_page - INFO - [login_page.py:13] - __init__() - LoginPage 初始化完成
2026-02-27 17:17:45 - test_valid_login[chromium] - INFO - [test_login.py:11] - test_valid_login() - 导航到登录页面
2026-02-27 17:17:45 - pages.login_page - INFO - [login_page.py:18] - navigate() - 导航到登录页面: http://10.10.27.171:7070/ztna-manager/
2026-02-27 17:17:46 - pages.login_page - INFO - [login_page.py:20] - navigate() - 登录页面加载完成
2026-02-27 17:17:46 - test_valid_login[chromium] - INFO - [test_login.py:15] - test_valid_login() - 使用用户名: sysadmin 进行登录
2026-02-27 17:17:46 - pages.login_page - INFO - [login_page.py:24] - login() - 开始登录操作，用户名: sysadmin
2026-02-27 17:17:47 - pages.login_page - INFO - [login_page.py:35] - login() - 登录操作执行完成
2026-02-27 17:17:47 - test_valid_login[chromium] - INFO - [test_login.py:18] - test_valid_login() - 登录操作完成
2026-02-27 17:17:47 - test_valid_login[chromium] - INFO - [test_login.py:21] - test_valid_login() - 验证登录后是否跳转到仪表盘
```

## 注意事项

1. 日志文件会自动创建，无需手动创建
2. 日志文件会自动轮转，不会无限增长
3. 在测试中使用 `logger` fixture 时，会自动使用测试名称作为日志记录器名称
4. 建议在关键步骤添加日志，便于问题排查
