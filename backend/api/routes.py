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
from neo4j import GraphDatabase
from db.neo4j_db import Neo4jDB  # 导入 Neo4jDB 类

api_bp = Blueprint('api', __name__)

# 数据库连接
DATABASE_URL = "sqlite:///qa_pairs.db"  # 使用 SQLite 数据库
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

# 创建 Neo4jDB 实例
neo4j_db = Neo4jDB()

# 添加查询语句定义
# 用户和组织数据查询
user_query = """
SELECT DISTINCT 
    u."USER_NO", u."USER_NAME", 
    o."ORG_NO", o."ORG_NAME",
    r."SYSTEM_NO", r."SYSTEM_NAME"
FROM "XYCS"."UMS_USER" u
JOIN "XYCS"."UMS_USER_ORG_RELATE" uor ON u."USER_NO" = uor."USER_NO"
JOIN "XYCS"."UMS_ORG" o ON uor."ORG_NO" = o."ORG_NO"
LEFT JOIN "XYCS"."RMS_SYSTEM" r ON o."SYSTEM_NO" = r."SYSTEM_NO"
WHERE ROWNUM <= 20
"""

# 发文数据查询
dispatch_query = """
SELECT 
    d."ID", d."SUBJECT", d."DOC_TYPE",
    d."DRAFT_USER_NO", d."ATDO_READER"
FROM "XYCS"."EGOV_DISPATCH" d
WHERE d."DRAFT_USER_NO" IS NOT NULL
"""

# 收文数据查询
receival_query = """
SELECT 
    r."ID", r."SUBJECT", r."DOC_TYPE",
    r."DRAFT_USER_NO", r."ATDO_READER"
FROM "XYCS"."EGOV_RECEIVAL" r
WHERE r."DRAFT_USER_NO" IS NOT NULL
"""

# 添加意见数据查询
opinion_query = """
SELECT DISTINCT
    o."ID", 
    DBMS_LOB.SUBSTR(o."OPINION_CONTENT", 4000, 1) as "OPINION_CONTENT",
    o."DOC_ID",
    o."OPINION_USER_NO", 
    o."CREATE_TIME"
FROM "XYCS"."EGOV_OPINION" o
WHERE EXISTS (
    -- 检查用户是否在公文的办理人中
    SELECT 1 
    FROM (
        SELECT "ID", "ATDO_READER"
        FROM "XYCS"."EGOV_DISPATCH"
        UNION ALL
        SELECT "ID", "ATDO_READER"
        FROM "XYCS"."EGOV_RECEIVAL"
    ) docs
    WHERE docs."ID" = o."DOC_ID"
    AND docs."ATDO_READER" LIKE '%' || o."OPINION_USER_NO" || '%'
)
AND o."OPINION_USER_NO" IS NOT NULL
AND o."DOC_ID" IS NOT NULL
AND o."OPINION_CONTENT" IS NOT NULL
"""

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
        
        # 检查 Q_Info 表中是已存在相同内容
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
        raise Exception("数据连接失败")

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
            raise Exception("数据库连失败")

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

            # 获文种分布统计
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
                    "name": "公文换",
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

@api_bp.route('/init-knowledge-graph', methods=['GET'])
def init_knowledge_graph():
    """初始化知识图谱数据"""
    print("开始初始化知识图谱...")
    neo4j_db = None
    try:
        cursor, conn = _connDB()
        if cursor is None or conn is None:
            raise Exception("数据库连接失败")

        try:
            # 获取用户和组织数据
            print("执行用户查询...")
            cursor.execute(user_query)
            user_data = cursor.fetchall()
            print(f"获取到 {len(user_data)} 条用户数据")

            # 获取发文数据
            print("执行发文查询...")
            cursor.execute(dispatch_query)
            dispatch_data = cursor.fetchall()
            print(f"获取到 {len(dispatch_data)} 条发文数据")

            # 获取收文数据
            print("执行收文查询...")
            cursor.execute(receival_query)
            receival_data = cursor.fetchall()
            print(f"获取到 {len(receival_data)} 条收文数据")

            # 获取意见数据
            print("执行意见查询...")
            cursor.execute(opinion_query)
            opinion_data = cursor.fetchall()
            print(f"获取到 {len(opinion_data)} 条意见数据")

            # 初始化Neo4j图谱
            print("初始化Neo4j连接...")
            neo4j_db = Neo4jDB()
            neo4j_db.connect()
            neo4j_db.clear_graph()

            # 创建节点和关系
            print("开始创建节点和关系...")
            
            # 创建用户和组织节点及关系
            for row in user_data:
                user_no, user_name, org_no, org_name, system_no, system_name = row
                print(f"处理用户数据: {user_name}")
                
                neo4j_db.create_user_node(user_no, user_name)
                neo4j_db.create_org_node(org_no, org_name)
                neo4j_db.create_user_org_relation(user_no, org_no)
                
                if system_no and system_name:
                    neo4j_db.create_system_node(system_no, system_name)
                    neo4j_db.create_org_system_relation(org_no, system_no)

            # 创建发文节点和关系
            for row in dispatch_data:
                doc_id, subject, doc_type, draft_user_no, atdo_reader = row
                print(f"处理发文数据: {subject}")
                
                try:
                    # 创建发文节点
                    neo4j_db.create_dispatch_doc_node(doc_id, subject, doc_type)
                    
                    # 创建用户起草关系
                    if draft_user_no:
                        neo4j_db.create_user_draft_dispatch(draft_user_no, doc_id)
                    
                except Exception as e:
                    print(f"处理发文数据失败: {e}")

            # 创建收文节点和关系
            for row in receival_data:
                doc_id, subject, doc_type, draft_user_no, atdo_reader = row
                print(f"处理收文数据: {subject}")
                
                try:
                    # 创建收文节点
                    neo4j_db.create_receival_doc_node(doc_id, subject, doc_type)
                    
                    # 创建用户登记关系
                    if draft_user_no:
                        neo4j_db.create_user_register_receival(draft_user_no, doc_id)
                    
                except Exception as e:
                    print(f"处理收文数据失败: {e}")
                    print(f"详细信息 - 文档ID: {doc_id}, 登记人: {draft_user_no}")

            # 创建意见节点和关系
            for row in opinion_data:
                opinion_id, content, doc_id, user_no, create_time = row
                print(f"处理意见数据: {opinion_id}")
                
                try:
                    # 检查用户是否在公文的办理人中
                    cursor.execute("""
                        SELECT "ATDO_READER"
                        FROM (
                            SELECT "ID", "ATDO_READER"
                            FROM "XYCS"."EGOV_DISPATCH"
                            UNION ALL
                            SELECT "ID", "ATDO_READER"
                            FROM "XYCS"."EGOV_RECEIVAL"
                        ) docs
                        WHERE docs."ID" = :doc_id
                    """, {'doc_id': doc_id})
                    
                    atdo_reader = cursor.fetchone()
                    if not atdo_reader:
                        print(f"跳过意见 {opinion_id}，找不到对应的公文 {doc_id}")
                        continue

                    # 解析 ATDO_READER 并检查用户是否在其中
                    try:
                        atdo_data = json.loads(atdo_reader[0])
                        user_in_atdo = any(
                            handler.get('readerNo') == user_no 
                            for handler in atdo_data
                        )
                        
                        if not user_in_atdo:
                            print(f"跳过意见 {opinion_id}，用户 {user_no} 不在公文办理人中")
                            continue
                            
                    except json.JSONDecodeError:
                        print(f"解析 ATDO_READER 失败: {atdo_reader[0]}")
                        continue

                    # 处理意见内容
                    if content:
                        content = content.strip()
                        if content:
                            content = content[:1000] + '...' if len(content) > 1000 else content
                            print(f"意见内容: {content[:100]}...")
                        else:
                            content = '无内容'
                    else:
                        content = '无内容'

                    # 创建意见节点
                    neo4j_db.create_opinion_node(opinion_id, content, create_time)
                    print(f"创建意见节点成功: {opinion_id}")
                    
                    # 创建用户填写意见的关系
                    neo4j_db.create_user_write_opinion_relation(user_no, opinion_id)
                    print(f"创建用户-意见关系成功: {user_no} -> {opinion_id}")
                    
                    # 创建意见属于公文的关系
                    neo4j_db.create_opinion_belong_doc_relation(opinion_id, doc_id)
                    print(f"创建意见-公文关系成功: {opinion_id} -> {doc_id}")
                        
                except Exception as e:
                    print(f"处理意见数据失败: {e}")
                    print(f"详细信息 - 意见ID: {opinion_id}, 用户: {user_no}, 文档ID: {doc_id}")

            print("知识图谱初始化完成")
            return jsonify({"message": "知识图谱初始化成功"}), 200

        finally:
            close_connection(cursor, conn)
            if neo4j_db:
                neo4j_db.close()

    except Exception as e:
        print(f"初始化知识图谱失败: {e}")
        if neo4j_db:
            neo4j_db.close()
        return jsonify({
            "error": "初始化知识图谱失败",
            "details": str(e)
        }), 500

@api_bp.route('/knowledge-graph', methods=['GET'])
def get_knowledge_graph():
    """获取知识图谱数据"""
    print("开始获取知识图谱数据...")
    try:
        neo4j_db = Neo4jDB()
        neo4j_db.connect()
        
        try:
            # 获取节点和关系
            nodes = neo4j_db.get_all_nodes()
            relationships = neo4j_db.get_all_relationships()
            
            response_data = {
                'nodes': nodes,
                'links': relationships
            }
            return jsonify(response_data), 200

        finally:
            neo4j_db.close()
            print("Neo4j连接已关闭")

    except Exception as e:
        print(f"获取知识图谱数据失败: {e}")
        return jsonify({
            "error": "获取知识图谱数据失败",
            "details": str(e)
        }), 500

def extract_handlers(atdo_reader):
    """从ATDO_READER字段提取办理人工号"""
    if not atdo_reader:
        return []
    try:
        # 解析JSON字符串
        handlers_data = json.loads(atdo_reader)
        # 提取所有办理人的工号
        handlers = []
        for handler in handlers_data:
            if handler.get('type') == 'user' and handler.get('readerNo'):
                handlers.append({
                    'user_no': handler['readerNo'],
                    'user_name': handler['readName'],
                    'org_no': handler['readOrgNo'],
                    'state': handler['stateName'],
                    'create_time': handler['createTime']
                })
        print(f"提取到的办理人信息: {handlers}")
        return handlers
    except json.JSONDecodeError as e:
        print(f"解析ATDO_READER失败: {e}")
        return []
    except Exception as e:
        print(f"处理办理人信息失败: {e}")
        return []