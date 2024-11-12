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
            print(f"成功入: {qa['question']} - {qa['answer']}")  # 调试输出
        
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
            return jsonify({'error': '没有文件'}), 400

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
        cursor, conn = _connDB()
        if cursor is None or conn is None:
            raise Exception("数据库连接失败")

        try:
            query = """
            SELECT "ID", "SUBJECT", "TYPE", "CONTENT", "DRAFT_USER_NAME", "DRAFT_DATE"
            FROM "XYCS"."QA_TEMPLATE"
            WHERE "TYPE" = :type
            ORDER BY "DRAFT_DATE" DESC
            """
            cursor.execute(query, {'type': template_type})
            templates = cursor.fetchall()
            
            result = [{
                'id': t[0],
                'subject': t[1],
                'type': t[2],
                'content': t[3],  # 确保 content 字段正确返回
                'draft_user_name': t[4],
                'draft_date': t[5].strftime('%Y-%m-%d %H:%M:%S') if t[5] else None
            } for t in templates]

            print(f"获取到的模板: {result}")  # 添加调试日志
            return jsonify({
                "templates": result
            }), 200
        finally:
            close_connection(cursor, conn)
    except Exception as e:
        print(f"获取模板失败: {e}")  # 添加调试日志
        return jsonify({
            "error": "获取模板列表失败",
            "details": str(e)
        }), 500

@api_bp.route('/file-stats', methods=['GET'])
def get_file_stats():
    """获取文件统计数据"""
    try:
        # 获取筛选参数
        file_type = request.args.get('fileType', '')  # 文件类型
        system = request.args.get('system', '')       # 系统编码
        format = request.args.get('format', '')       # 文件格式
        module = request.args.get('module', '')       # 模块
        start_date = request.args.get('startDate')    # 开始日期
        end_date = request.args.get('endDate')        # 结束日期

        cursor, conn = _connDB()
        if cursor is None or conn is None:
            raise Exception("数据库连接失败")

        try:
            # 构建基础条件
            conditions = ['"STATUS" != \'已删\'']
            params = {}
            
            # 添加筛选条件
            if file_type:
                conditions.append('"TYPE" = :file_type')
                params['file_type'] = file_type

            if system:
                conditions.append('"SYSTEM_NO" = :system')
                params['system'] = system

            if format:
                conditions.append('"FILE_SUFFIX" = :format')
                params['format'] = format

            if module:
                conditions.append('"MODULE_ID" = :module')
                params['module'] = module

            # 添加时间范围条件
            if start_date:
                conditions.append('TRUNC("CREATE_TIME") >= TO_DATE(:start_date, \'YYYY-MM-DD\')')
                params['start_date'] = start_date
            if end_date:
                conditions.append('TRUNC("CREATE_TIME") <= TO_DATE(:end_date, \'YYYY-MM-DD\')')
                params['end_date'] = end_date

            where_clause = ' AND '.join(conditions)

            # 获取总文件数和总大小
            count_query = f"""
            SELECT COUNT(*), COALESCE(SUM("FILE_SIZE"), 0)
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            """
            cursor.execute(count_query, params)
            total_files, total_size = cursor.fetchone()

            # 获取本月新增
            monthly_query = f"""
            SELECT COUNT(*)
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            AND "CREATE_TIME" >= TRUNC(CURRENT_DATE, 'MM')
            """
            cursor.execute(monthly_query, params)
            monthly_new = cursor.fetchone()[0]

            # 获取文件类型分布
            type_query = f"""
            SELECT "TYPE", COUNT(*) as count
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            GROUP BY "TYPE"
            ORDER BY count DESC
            """
            cursor.execute(type_query, params)
            type_distribution = [
                {"name": row[0] or '未知类型', "value": row[1]}
                for row in cursor.fetchall()
            ]

            # 获取系统使用情况
            system_query = f"""
            SELECT "SYSTEM_NO", COUNT(*) as count
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            GROUP BY "SYSTEM_NO"
            ORDER BY count DESC
            """
            cursor.execute(system_query, params)
            system_stats = [
                {"name": row[0] or '未知系统', "value": row[1]}
                for row in cursor.fetchall()
            ]

            # 获取文件格式分布
            format_query = f"""
            SELECT "FILE_SUFFIX", COUNT(*) as count
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            GROUP BY "FILE_SUFFIX"
            ORDER BY count DESC
            """
            cursor.execute(format_query, params)
            format_distribution = [
                {"name": row[0] or '未知格式', "value": row[1]}
                for row in cursor.fetchall()
            ]

            # 获取模块使用统计
            module_query = f"""
            SELECT 
                COALESCE("MODULE_ID", '未知模块') as module_name,
                COUNT(*) as count
            FROM "XYCS"."EGOV_ATT_DATA"
            WHERE {where_clause}
            GROUP BY "MODULE_ID"
            ORDER BY count DESC
            """
            cursor.execute(module_query, params)
            module_stats = [
                {"name": row[0], "value": row[1]}
                for row in cursor.fetchall()
            ]

            response_data = {
                "totalFiles": total_files,
                "totalSize": total_size,
                "monthlyNew": monthly_new,
                "typeDistribution": type_distribution,
                "systemStats": system_stats,
                "formatDistribution": format_distribution,
                "moduleStats": module_stats
            }

            return jsonify(response_data), 200

        finally:
            close_connection(cursor, conn)

    except Exception as e:
        print(f"获取文件统计数据失败: {e}")
        return jsonify({
            "error": "获取统计数据失败",
            "details": str(e)
        }), 500

@api_bp.route('/document-stats', methods=['GET'])
def get_document_stats():
    print("接收到公文统计请求")  # 添加调试日志
    try:
        # 获取筛选参数
        doc_type = request.args.get('docType', '')
        module = request.args.get('module', '')

        cursor, conn = _connDB()
        if cursor is None or conn is None:
            raise Exception("数据库连接失败")

        try:
            # 构建基础条件
            conditions = []
            params = {}
            
            if doc_type:
                conditions.append('"DOC_TYPE" = :doc_type')
                params['doc_type'] = doc_type

            where_clause = ' AND '.join(conditions) if conditions else '1=1'

            # 获取文件标题分类统计（根据标题关键字分类）
            subject_query = f"""
            WITH combined_data AS (
                SELECT "SUBJECT" FROM "XYCS"."EGOV_DISPATCH_DATA" WHERE {where_clause}
                UNION ALL
                SELECT "SUBJECT" FROM "XYCS"."EGOV_RECEIVAL_DATA" WHERE {where_clause}
                UNION ALL
                SELECT "SUBJECT" FROM "XYCS"."EGOV_EX_DOC_DATA" WHERE {where_clause}
            )
            SELECT 
                CASE 
                    WHEN "SUBJECT" LIKE '%通知%' THEN '通知'
                    WHEN "SUBJECT" LIKE '%通告%' THEN '通告'
                    WHEN "SUBJECT" LIKE '%通报%' THEN '通报'
                    WHEN "SUBJECT" LIKE '%请示%' THEN '请示'
                    WHEN "SUBJECT" LIKE '%函%' THEN '函'
                    WHEN "SUBJECT" LIKE '%纪要%' THEN '纪要'
                    WHEN "SUBJECT" LIKE '%决议%' THEN '决议'
                    WHEN "SUBJECT" LIKE '%决定%' THEN '决定'
                    WHEN "SUBJECT" LIKE '%公告%' THEN '公告'
                    ELSE '其他'
                END as doc_category,
                COUNT(*) as count
            FROM combined_data
            GROUP BY 
                CASE 
                    WHEN "SUBJECT" LIKE '%通知%' THEN '通知'
                    WHEN "SUBJECT" LIKE '%通告%' THEN '通告'
                    WHEN "SUBJECT" LIKE '%通报%' THEN '通报'
                    WHEN "SUBJECT" LIKE '%请示%' THEN '请示'
                    WHEN "SUBJECT" LIKE '%函%' THEN '函'
                    WHEN "SUBJECT" LIKE '%纪要%' THEN '纪要'
                    WHEN "SUBJECT" LIKE '%决议%' THEN '决议'
                    WHEN "SUBJECT" LIKE '%决定%' THEN '决定'
                    WHEN "SUBJECT" LIKE '%公告%' THEN '公告'
                    ELSE '其他'
                END
            ORDER BY count DESC
            """
            cursor.execute(subject_query, params)
            subject_stats = [
                {"name": row[0], "value": row[1]}
                for row in cursor.fetchall()
            ]

            # 获取文种分布统计
            category_query = f"""
            WITH combined_data AS (
                SELECT "DOC_TYPE" as type_field FROM "XYCS"."EGOV_DISPATCH_DATA" WHERE {where_clause}
                UNION ALL
                SELECT "FILE_CATEGORY" as type_field FROM "XYCS"."EGOV_RECEIVAL_DATA" WHERE {where_clause}
                UNION ALL
                SELECT "DOC_TYPE" as type_field FROM "XYCS"."EGOV_EX_DOC_DATA" WHERE {where_clause}
            )
            SELECT 
                COALESCE(type_field, '未知文种') as category,
                COUNT(*) as count
            FROM combined_data
            GROUP BY type_field
            ORDER BY count DESC
            """
            cursor.execute(category_query, params)
            category_stats = [
                {"name": row[0] or '未知文种', "value": row[1]}
                for row in cursor.fetchall()
            ]

            # 获取模块统计
            module_stats = [
                {
                    "name": "发文",
                    "value": cursor.execute(
                        f'SELECT COUNT(*) FROM "XYCS"."EGOV_DISPATCH_DATA" WHERE {where_clause}',
                        params
                    ).fetchone()[0]
                },
                {
                    "name": "收文",
                    "value": cursor.execute(
                        f'SELECT COUNT(*) FROM "XYCS"."EGOV_RECEIVAL_DATA" WHERE {where_clause}',
                        params
                    ).fetchone()[0]
                },
                {
                    "name": "公文交换",
                    "value": cursor.execute(
                        f'SELECT COUNT(*) FROM "XYCS"."EGOV_EX_DOC_DATA" WHERE {where_clause}',
                        params
                    ).fetchone()[0]
                }
            ]

            # 获取TOP10统计
            top_stats = {
                "subject": subject_stats[:10],
                "category": category_stats[:10]
            }

            # 计算总数
            total_docs = sum(stat["value"] for stat in module_stats)

            response_data = {
                "totalDocs": total_docs,
                "moduleStats": module_stats,
                "subjectStats": subject_stats,
                "categoryStats": category_stats,
                "topStats": top_stats
            }

            # print("返回公文统计数据:", response_data)  # 添加调试日志
            return jsonify(response_data), 200

        finally:
            close_connection(cursor, conn)

    except Exception as e:
        print(f"处理公文统计数据失败: {e}")  # 添加错误日志
        return jsonify({
            "error": "获取统计数据失败",
            "details": str(e)
        }), 500