import dmPython
import logging
import uuid
import yaml
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_db_config():
    """加载数据库配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'database.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f'加载数据库配置失败: {e}')
        raise

def _connDB():
    """连接达梦数据库"""
    try:
        config = load_db_config()['dameng']
        conn = dmPython.connect(
            user=config['user'],
            password=config['password'],
            server=config['host'],
            port=config['port'],
            autoCommit=config['autocommit']
        )
        cursor = conn.cursor()
        logging.info('达梦数据库连接成功！')
        return cursor, conn
    except Exception as e:
        logging.error(f'达梦数据库连接异常：{e}')
        return None, None

def close_connection(cursor, conn):
    """关闭数据库连接"""
    if cursor:
        cursor.close()
        logging.info('数据库游标已关闭。')
    if conn:
        conn.close()
        logging.info('数据库连接已关闭。')

def execute_query(query, params=None):
    """执行数据库查询"""
    cursor, conn = _connDB()
    if cursor is None or conn is None:
        raise Exception("数据库连接失败")

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        logging.info('查询执行成功。')
        return params['id']
    except Exception as e:
        logging.error(f'查询执行失败: {e}')
        raise
    finally:
        close_connection(cursor, conn)

def insert_qa_pair(id, question, answer, draft_user_name='jin'):
    """插入问答对到数据库"""
    insert_sql = """
    INSERT INTO "XYCS"."QA_INFO" ("ID", "Q_ID", "QUESTION", "ANSWER", "DRAFT_USER_NAME", "DRAFT_DATE")
    VALUES (:id, :q_id, :question, :answer, :draft_user_name, CURRENT_TIMESTAMP)
    """
    params = {
        'id': id,
        'q_id': q_id,
        'question': question,
        'answer': answer,
        'draft_user_name': draft_user_name
    }
    execute_query(insert_sql, params)

def save_template(template_data):
    """保存模板到数据库"""
    insert_sql = """
    INSERT INTO "XYCS"."QA_TEMPLATE" 
    ("ID", "SUBJECT", "TYPE", "CONTENT", "DRAFT_USER_NAME", "DRAFT_DATE")
    VALUES (:id, :subject, :type, :content, :draft_user_name, CURRENT_TIMESTAMP)
    """
    
    template_id = str(uuid.uuid4())[:16]
    params = {
        'id': template_id,
        'subject': template_data['subject'],
        'type': template_data['type'],
        'content': template_data['content'],
        'draft_user_name': template_data.get('draft_user_name', 'jin')
    }
    
    return execute_query(insert_sql, params)

def get_template_by_type(template_type):
    """根据类型获取模板列表"""
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
        
        return [{
            'id': t[0],
            'subject': t[1],
            'type': t[2],
            'content': t[3],
            'draft_user_name': t[4],
            'draft_date': t[5]
        } for t in templates]
    finally:
        close_connection(cursor, conn)

