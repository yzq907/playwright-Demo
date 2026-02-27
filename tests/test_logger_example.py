from utils.logger import get_logger, log_function_call, log_execution_time, Logger
import logging


def basic_usage():
    """基本使用示例"""
    logger = get_logger(__name__)
    
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")


@log_function_call
def function_with_decorator(username, password):
    """使用装饰器记录函数调用"""
    print(f"登录用户: {username}")


@log_execution_time
def slow_function():
    """使用装饰器记录执行时间"""
    import time
    time.sleep(2)
    return "执行完成"


def custom_logger():
    """自定义日志记录器"""
    logger = Logger.get_logger(
        name="custom_logger",
        level=logging.DEBUG,
        log_dir="logs",
        log_file="custom.log"
    )
    
    logger.debug("自定义日志记录器的调试信息")
    logger.info("自定义日志记录器的普通信息")


def set_log_level():
    """设置日志级别"""
    logger = get_logger(__name__)
    
    logger.info("这是 INFO 级别的日志")
    
    Logger.set_level(logging.DEBUG)
    logger.debug("现在可以看到 DEBUG 级别的日志了")


if __name__ == "__main__":
    print("=" * 50)
    print("1. 基本使用")
    print("=" * 50)
    basic_usage()
    
    print("\n" + "=" * 50)
    print("2. 使用装饰器记录函数调用")
    print("=" * 50)
    function_with_decorator("admin", "password123")
    
    print("\n" + "=" * 50)
    print("3. 使用装饰器记录执行时间")
    print("=" * 50)
    result = slow_function()
    print(f"函数返回: {result}")
    
    print("\n" + "=" * 50)
    print("4. 自定义日志记录器")
    print("=" * 50)
    custom_logger()
    
    print("\n" + "=" * 50)
    print("5. 设置日志级别")
    print("=" * 50)
    set_log_level()
