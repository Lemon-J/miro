"""
测试蓝图
用于验证服务是否正常工作
"""

from flask import Blueprint, jsonify
from ..config import Config
from ..utils import LLMClient, FileParser, split_text_into_chunks

test_bp = Blueprint('test', __name__)


@test_bp.route('/ping', methods=['GET'])
def ping():
    """健康检查"""
    return jsonify({"message": "pong"})


@test_bp.route('/config', methods=['GET'])
def show_config():
    """查看当前配置（不暴露密钥）"""
    return jsonify({
        "llm_model": Config.LLM_MODEL_NAME,
        "llm_base_url": Config.LLM_BASE_URL,
        "llm_configured": bool(Config.LLM_API_KEY),
        "zep_configured": bool(Config.ZEP_API_KEY),
        "debug": Config.DEBUG,
    })


@test_bp.route("/llm_chat",methods=['GET'])
def test_llm_chat():
    llm = LLMClient()
    res =  llm.chat(messages=[{'role':'user','content':'你好,这是测试消息'}])
    print(res)
    return jsonify({"message": res})


@test_bp.route('/file_parser/<path:file_path>', methods=['GET'])
def test_file_parser(file_path: str):
    """测试文件解析"""

    file_content = FileParser.extract_text(file_path)

    print(file_content)

    content_chunk_list = split_text_into_chunks(text= file_content, chunk_size=1000, overlap=50)
    
    return jsonify({"chunks": content_chunk_list})
    