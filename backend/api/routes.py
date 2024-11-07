from flask import Blueprint, request, jsonify
import requests
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.qa_model import QAPair, QInfo, Base
from db.db import _connDB, insert_qa_pair  # 导入数据库连接函数和插入函数
import uuid
from datetime import datetime
from db.db import close_connection, execute_query, get_template_by_type
from common.doc_processor import process_docx
import os
import json

api_bp = Blueprint('api', __name__)

# 数据库连接
DATABASE_URL = "sqlite:///qa_pairs.db"  # 使用 SQLite 数据库
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@api_bp.route('/generate', methods=['POST'])
def generate_qa():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        count = data.get('count', 10)
        
        # 调用本地 FastAPI 端点
        response = requests.post(
            "http://localhost:8000/model/generate",
            json={"prompt": prompt, "count": count}
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": "Model API error",
                "details": response.text
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}) 

@api_bp.route('/save', methods=['POST'])
def save_qa():
    try:
        data = request.get_json()
        print(f"接收到的保存请求数据: {data}")  # 调试输出
        qa_list = data.get('qaList', [])
        q_content = data.get('qContent', '')  # 从请求中获取左侧输入框内容
        
        # 检查 Q_Info 表中是否已存在相同内容
        if is_qinfo_exists(q_content):
            return jsonify({"message": "内容已存在，请不要重复操作！"}), 200  # 返回提示信息
        
        # 先保存到 Q_Info 表
        q_id = insert_qinfo(q_content)  # 保存到 Q_Info 表并获取 ID
        print(f"保存的 Q_Info ID: {q_id}")  # 调试输出
        
        # 保存到 QA_INFO 表
        for qa in qa_list:
            insert_qa_pair(qa['question'], qa['answer'], q_id)  # 使用返回的 ID
            print(f"成功插入: {qa['question']} - {qa['answer']}")  # 调试输出
        
        return jsonify({"message": "问答对已保存"}), 200
    except Exception as e:
        print(f"保存失败: {e}")  # 调试输出
        return jsonify({
            "error": "保存失败",
            "details": str(e)
        }), 500

def insert_qinfo(q_content):
    """插入问答内容到 Q_Info 表并返回 ID"""
    insert_sql = """
    INSERT INTO "XYCS"."Q_INFO" ("ID", "Q_CONTENT")
    VALUES (:id, :q_content)
    """
    id = str(uuid.uuid4())[:16]  # 生成唯一ID
    params = {
        'id': id,
        'q_content': q_content
    }
    execute_query(insert_sql, params)
    return id  # 返回插入的 ID

def insert_qa_pair(question, answer, q_id, draft_user_name='jin'):
    """插入问答对到 QA_INFO 表"""
    insert_sql = """
    INSERT INTO "XYCS"."QA_INFO" ("ID", "Q_ID", "QUESTION", "ANSWER", "DRAFT_USER_NAME", "DRAFT_DATE")
    VALUES (:id, :q_id, :question, :answer, :draft_user_name, CURRENT_TIMESTAMP)
    """
    id = str(uuid.uuid4())[:16]  # 生成唯一ID
    params = {
        'id': id,
        'q_id': q_id,
        'question': question,
        'answer': answer,
        'draft_user_name': draft_user_name
    }
    execute_query(insert_sql, params)

def is_qa_exists(question, answer):
    """检查问答对是否已存在"""
    cursor, conn = _connDB()
    if cursor is None or conn is None:
        raise Exception("数据库连接失败")

    query = """
    SELECT COUNT(*) FROM "XYCS"."QA_INFO" 
    WHERE "QUESTION" = :question AND "ANSWER" = :answer
    """
    print(f"执行查询: {query}，参数: {{'question': {question}, 'answer': {answer}}}")  # 调试输出
    cursor.execute(query, {'question': question, 'answer': answer})
    count = cursor.fetchone()[0]
    
    close_connection(cursor, conn)  # 关闭连接
    return count > 0  # 如果存在，返回 True

def is_qinfo_exists(q_content):
    """检查 Q_Info 表中是否已存在相同内容"""
    cursor, conn = _connDB()
    if cursor is None or conn is None:
        raise Exception("数据库连接失败")

    query = """
    SELECT COUNT(*) FROM "XYCS"."Q_INFO" 
    WHERE "Q_CONTENT" = :q_content
    """
    cursor.execute(query, {'q_content': q_content})
    count = cursor.fetchone()[0]
    
    close_connection(cursor, conn)  # 关闭连接
    return count > 0  # 如果存在，返回 True

@api_bp.route('/process-doc', methods=['POST'])
def process_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        if not file.filename.endswith('.docx'):
            return jsonify({'error': '只支持 .docx 文件'}), 400

        # 保存文件
        temp_path = 'temp.docx'
        file.save(temp_path)

        # 处理文档
        sections = process_docx(temp_path)

        # 删除临时文件
        os.remove(temp_path)

        return jsonify({
            'message': '文档处理成功',
            'sections': sections
        }), 200

    except Exception as e:
        return jsonify({
            'error': '处理文档失败',
            'details': str(e)
        }), 500

@api_bp.route('/save-template', methods=['POST'])
def save_template():
    try:
        data = request.get_json()
        required_fields = ['subject', 'type', 'content']
        
        # 验证必填字段
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "error": f"缺少必填字段: {field}"
                }), 400

        # 验证 JSON 格式
        try:
            if isinstance(data['content'], str):
                json.loads(data['content'])
        except json.JSONDecodeError:
            return jsonify({
                "error": "模板内容必须是有效的 JSON 格式"
            }), 400

        cursor, conn = _connDB()
        if cursor is None or conn is None:
            raise Exception("数据库连接失败")

        try:
            # 检查是否存在相同名称的模板
            check_sql = """
            SELECT COUNT(*) FROM "XYCS"."QA_TEMPLATE" 
            WHERE "SUBJECT" = :subject AND "TYPE" = :type
            """
            cursor.execute(check_sql, {
                'subject': data['subject'], 
                'type': data['type']
            })
            count = cursor.fetchone()[0]
            
            if count > 0:
                return jsonify({
                    "message": "已存在相同名称的模板！"
                }), 400

            # 插入新模板
            insert_sql = """
            INSERT INTO "XYCS"."QA_TEMPLATE" 
            ("ID", "SUBJECT", "TYPE", "CONTENT", "DRAFT_USER_NAME", "DRAFT_DATE")
            VALUES (:id, :subject, :type, :content, :draft_user_name, CURRENT_TIMESTAMP)
            """
            
            template_id = str(uuid.uuid4())[:16]
            params = {
                'id': template_id,
                'subject': data['subject'],
                'type': data['type'],
                'content': data['content'],
                'draft_user_name': data.get('draft_user_name', 'jin')
            }
            
            cursor.execute(insert_sql, params)
            conn.commit()

            return jsonify({
                "message": "模板保存成功",
                "template_id": template_id
            }), 200

        finally:
            close_connection(cursor, conn)

    except Exception as e:
        return jsonify({
            "error": "保存失败",
            "details": str(e)
        }), 500

@api_bp.route('/templates/<template_type>', methods=['GET'])
def get_templates(template_type):
    """获取指定类型的模板列表"""
    try:
        templates = get_template_by_type(template_type)
        return jsonify({
            "templates": templates
        }), 200
    except Exception as e:
        return jsonify({
            "error": "获取模板列表失败",
            "details": str(e)
        }), 500