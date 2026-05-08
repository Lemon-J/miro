"""
后端启动入口
"""

import os
import sys

# Windows 控制台 UTF-8 编码（必须在所有 import 之前）
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config


def main():
    """主函数"""
    # 验证配置（当前 LLM 和 ZEP 未配置会报警告，不影响启动）
    errors = Config.validate()
    if errors:
        print("配置警告（部分功能将不可用）:")
        for err in errors:
            print(f"  - {err}")
        print()

    # 创建应用
    app = create_app()

    # 获取运行参数
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = Config.DEBUG

    # 启动服务
    print(f"服务地址: http://{host}:{port}")
    print(f"健康检查: http://localhost:{port}/health")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    main()
