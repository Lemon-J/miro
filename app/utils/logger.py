"""
日志配置
文件 + 控制台双输出，文件按日期轮转
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


def _ensure_logs_dir():
    """确保日志目录存在"""
    logs_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def _ensure_utf8_stdout():
    """Windows 下强制标准输出使用 UTF-8"""
    if sys.platform == 'win32':
        os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# 启动时立即修复 Windows 编码
_ensure_utf8_stdout()

# 已创建的 logger 缓存（避免重复创建 handler）
_loggers = {}


def setup_logger(name: str = 'myapp', level=logging.DEBUG) -> logging.Logger:
    """
    创建并配置一个 logger

    - 控制台：INFO 级别，简洁格式
    - 文件：DEBUG 级别，详细格式，10MB 轮转保留 5 个
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # 日志格式
    file_fmt = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_fmt = logging.Formatter('[%(levelname)s] %(message)s')

    # 文件 handler — 按日期命名，10MB 轮转
    logs_dir = _ensure_logs_dir()
    today = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(logs_dir, f'myapp_{today}.log')

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_fmt)

    # 控制台 handler — 只输出 INFO 以上
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _loggers[name] = logger
    return logger


def get_logger(name: str = 'myapp') -> logging.Logger:
    """获取 logger，如果不存在则自动创建"""
    if name in _loggers:
        return _loggers[name]
    return setup_logger(name)
