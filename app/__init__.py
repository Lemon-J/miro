"""
Flask 应用工厂
"""

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """
    Flask 应用工厂函数

    所有初始化逻辑集中在这里：
    - 加载配置
    - 启用 CORS
    - 注册请求日志钩子
    - 注册蓝图（后续添加）
    - 注册健康检查
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 中文 JSON 直接显示
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # 初始化日志
    logger = setup_logger('myapp')
    logger.info("=" * 50)
    logger.info("后端服务启动中...")
    logger.info("=" * 50)

    # 启用 CORS（允许前端跨域访问 /api/*）
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 请求日志钩子
    @app.before_request
    def log_request():
        req_logger = get_logger('myapp.request')
        req_logger.debug(f"请求: {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        req_logger = get_logger('myapp.request')
        req_logger.debug(f"响应: {response.status_code}")
        return response

    # ---- 健康检查 ----
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'my-backend'}

    # ---- 注册蓝图 ----
    from .api import test_bp
    app.register_blueprint(test_bp, url_prefix='/api/test')
    # 后续添加: graph_bp, simulation_bp, report_bp

    logger.info("后端服务启动完成")

    return app
