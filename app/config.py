"""
配置管理
从 .env 文件加载配置，所有配置项集中管理
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件（项目根目录）
_project_root = os.path.join(os.path.dirname(__file__), '..')
_env_path = os.path.join(_project_root, '.env')

if os.path.exists(_env_path):
    load_dotenv(_env_path, override=True)
else:
    load_dotenv(override=True)


class Config:
    """Flask 配置类"""

    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    # JSON 配置 — 中文直接显示，不转义为 \uXXXX
    JSON_AS_ASCII = False

    # LLM 配置
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')

    # Zep 配置
    ZEP_API_KEY = os.environ.get('ZEP_API_KEY')

    # 文件上传配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(_project_root, 'uploads')
    UPLOAD_FOLDER_DEL = os.path.join(_project_root, 'del_peoject')

    ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt', 'markdown'}

    # 文本处理配置
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 50

    @classmethod
    def validate(cls) -> list:
        """验证必要配置，返回错误列表（空 = 通过）"""
        errors = []
        if not cls.LLM_API_KEY:
            errors.append("LLM_API_KEY 未配置")
        if not cls.ZEP_API_KEY:
            errors.append("ZEP_API_KEY 未配置")
        return errors
