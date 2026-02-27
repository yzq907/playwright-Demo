import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


class Logger:
    _loggers = {}
    
    @staticmethod
    def get_logger(name=None, level=logging.INFO, log_dir='logs', log_file=None):
        """
        获取日志记录器
        
        Args:
            name: 日志记录器名称，默认使用调用模块名
            level: 日志级别，默认为 INFO
            log_dir: 日志目录，默认为 'logs'
            log_file: 日志文件名，默认为 'app_{日期}.log'
        
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        if name is None:
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'root')
        
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        if log_file is None:
            log_file = f"app_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = RotatingFileHandler(
            filename=log_path / log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        Logger._loggers[name] = logger
        return logger
    
    @staticmethod
    def set_level(level):
        """
        设置所有日志记录器的日志级别
        
        Args:
            level: 日志级别 (logging.DEBUG, logging.INFO, etc.)
        """
        for logger in Logger._loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)


def get_logger(name=None, level=logging.INFO):
    """
    便捷函数：获取日志记录器
    
    Args:
        name: 日志记录器名称，默认使用调用模块名
        level: 日志级别，默认为 INFO
    
    Returns:
        logging.Logger: 配置好的日志记录器
    
    Usage:
        from utils.logger import get_logger
        
        logger = get_logger(__name__)
        logger.info("这是一条信息")
        logger.debug("这是一条调试信息")
        logger.warning("这是一条警告")
        logger.error("这是一条错误")
    """
    return Logger.get_logger(name=name, level=level)


def log_function_call(func):
    """
    装饰器：记录函数调用的日志
    
    Usage:
        @log_function_call
        def my_function(arg1, arg2):
            pass
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.info(f"调用函数: {func.__name__}(), 参数: args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"函数 {func.__name__}() 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__}() 执行失败: {str(e)}", exc_info=True)
            raise
    return wrapper


def log_execution_time(func):
    """
    装饰器：记录函数执行时间
    
    Usage:
        @log_execution_time
        def my_function():
            pass
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.info(f"开始执行函数: {func.__name__}()")
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"函数 {func.__name__}() 执行完成，耗时: {execution_time:.2f}秒")
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"函数 {func.__name__}() 执行失败，耗时: {execution_time:.2f}秒, 错误: {str(e)}", exc_info=True)
            raise
    return wrapper
