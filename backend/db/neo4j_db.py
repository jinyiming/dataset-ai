from neo4j import GraphDatabase
import logging
import yaml
import os

def load_db_config():
    """加载数据库配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'database.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f'加载数据库配置失败: {e}')
        raise

class Neo4jDB:
    def __init__(self):
        self._driver = None
        self._config = None
        try:
            self._config = load_db_config()['neo4j']
            logging.info('Neo4j配置加载成功')
        except Exception as e:
            logging.error(f'加载Neo4j配置失败: {e}')
            raise

    def connect(self):
        """连接Neo4j数据库"""
        try:
            print(f"尝试连接Neo4j数据库... URI: {self._config['uri']}")
            self._driver = GraphDatabase.driver(
                self._config['uri'],
                auth=(self._config['user'], self._config['password'])
            )
            # 测试连接
            with self._driver.session() as session:
                result = session.run("RETURN 1")
                result.single()
            print("Neo4j数据库连接成功!")
            return self._driver
        except Exception as e:
            print(f"Neo4j数据库连接失败: {e}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self._driver:
            self._driver.close()
            logging.info("Neo4j数据库连接已关闭")

    def clear_graph(self):
        """清空图谱数据"""
        try:
            with self._driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                logging.info("图谱数据已清空")
        except Exception as e:
            logging.error(f"清空图谱数据失败: {e}")
            raise

    def create_document_node(self, doc_id, subject, doc_type):
        """创建文档节点"""
        try:
            with self._driver.session() as session:
                session.run("""
                    CREATE (d:Document {
                        id: $doc_id,
                        title: $subject,
                        type: $doc_type
                    })
                """, doc_id=doc_id, subject=subject, doc_type=doc_type)
                logging.info(f"创建档节点成功: {subject}")
        except Exception as e:
            logging.error(f"创建文档节点失败: {e}")
            raise

    def create_department_relation(self, dept_name, doc_id, relation_type):
        """创建部门关系"""
        try:
            with self._driver.session() as session:
                # 根据关系类型选择对应的查询语句
                if relation_type == 'SENT':
                    query = """
                        MERGE (dept:Department {name: $dept_name})
                        WITH dept
                        MATCH (d:Document {id: $doc_id})
                        CREATE (dept)-[:SENT]->(d)
                    """
                elif relation_type == 'RECEIVED':
                    query = """
                        MERGE (dept:Department {name: $dept_name})
                        WITH dept
                        MATCH (d:Document {id: $doc_id})
                        CREATE (dept)-[:RECEIVED]->(d)
                    """
                else:
                    raise ValueError(f"不支持的关系类型: {relation_type}")

                session.run(query, dept_name=dept_name, doc_id=doc_id)
                logging.info(f"创建部门关系成功: {dept_name} -{relation_type}-> {doc_id}")
        except Exception as e:
            logging.error(f"创建部门关系失败: {e}")
            raise

    def create_file_type_relation(self, file_type, doc_id):
        """创建文件类型关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MERGE (ft:FileType {name: $file_type})
                    WITH ft
                    MATCH (d:Document {id: $doc_id})
                    CREATE (d)-[:IS_TYPE]->(ft)
                """, file_type=file_type, doc_id=doc_id)
                logging.info(f"创建文件类型关系成功: {doc_id} -IS_TYPE-> {file_type}")
        except Exception as e:
            logging.error(f"创建文件类型关系失败: {e}")
            raise

    def get_all_nodes(self):
        """获取所有节点"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (n)
                    RETURN DISTINCT
                        ID(n) as id,
                        CASE
                            WHEN 'User' IN labels(n) THEN n.name
                            WHEN 'Organization' IN labels(n) THEN n.name
                            WHEN 'Document' IN labels(n) THEN n.title
                            WHEN 'System' IN labels(n) THEN n.name
                            WHEN 'Opinion' IN labels(n) THEN 
                                CASE 
                                    WHEN n.content IS NULL THEN '无内容'
                                    ELSE substring(n.content, 0, 20)
                                END
                            ELSE '未命名'
                        END as label,
                        labels(n)[0] as type,
                        properties(n) as properties
                """)
                
                nodes = []
                for record in result:
                    node_data = {
                        'id': str(record['id']),
                        'label': record['label'] or '未命名',
                        'type': record['type'].lower(),
                        'properties': record['properties']
                    }
                    nodes.append(node_data)
                
                print(f"从Neo4j获取到 {len(nodes)} 个节点")
                return nodes
        except Exception as e:
            print(f"获取节点失败: {e}")
            raise

    def get_all_relationships(self):
        """获取所有关系"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (a)-[r]->(b)
                    RETURN 
                        ID(a) as source,
                        ID(b) as target,
                        type(r) as type
                """)
                
                relationships = []
                for record in result:
                    rel_data = {
                        'source': str(record['source']),
                        'target': str(record['target']),
                        'type': record['type']
                    }
                    relationships.append(rel_data)
                
                print(f"从Neo4j获取到 {len(relationships)} 个关系")
                return relationships
        except Exception as e:
            print(f"获取关系失败: {e}")
            raise

    def create_user_node(self, user_no, user_name):
        """创建用户节点"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MERGE (u:User {user_no: $user_no})
                    ON CREATE SET u.name = $user_name
                    RETURN u
                """, user_no=user_no, user_name=user_name)
                logging.info(f"创建用户节点成功: {user_name}")
                return result.single()['u']
        except Exception as e:
            logging.error(f"创建用户节点失败: {e}")
            raise

    def create_org_node(self, org_no, org_name):
        """创建组织节点"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MERGE (o:Organization {
                        org_no: $org_no,
                        name: $org_name
                    })
                """, org_no=org_no, org_name=org_name)
                logging.info(f"创建组织节点成功: {org_name}")
        except Exception as e:
            logging.error(f"创建组织节点失败: {e}")
            raise

    def create_system_node(self, system_no, system_name):
        """创建系统节点"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MERGE (s:System {
                        system_no: $system_no,
                        name: $system_name
                    })
                """, system_no=system_no, system_name=system_name)
                logging.info(f"创建系统节点成功: {system_name}")
        except Exception as e:
            logging.error(f"创建系统节点失败: {e}")
            raise

    def create_user_org_relation(self, user_no, org_no):
        """创建用户-组织关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (u:User {user_no: $user_no})
                    MATCH (o:Organization {org_no: $org_no})
                    MERGE (u)-[:BELONGS_TO {label: '属于'}]->(o)
                """, user_no=user_no, org_no=org_no)
                logging.info(f"创建用户-组织关系成功: {user_no} -> {org_no}")
        except Exception as e:
            logging.error(f"创建用户-组织关系失败: {e}")
            raise

    def create_org_system_relation(self, org_no, system_no):
        """创建组织-系统关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (o:Organization {org_no: $org_no})
                    MATCH (s:System {system_no: $system_no})
                    MERGE (o)-[:HAS_ACCESS]->(s)
                """, org_no=org_no, system_no=system_no)
                logging.info(f"创建组织-系统关系成功: {org_no} -> {system_no}")
        except Exception as e:
            logging.error(f"创建组织-系统关系失败: {e}")
            raise

    def get_user_colleagues(self, user_no):
        """获取用户的同事（同部门）"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (u1:User {user_no: $user_no})-[:BELONGS_TO]->(o:Organization)
                    <-[:BELONGS_TO]-(u2:User)
                    WHERE u1 <> u2
                    RETURN u2.name as colleague_name, o.org_name as department
                """, user_no=user_no)
                return [(record['colleague_name'], record['department']) 
                        for record in result]
        except Exception as e:
            logging.error(f"获取用户同事失败: {e}")
            raise

    def get_user_systems(self, user_no):
        """获取用户可访问的系统"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (u:User {user_no: $user_no})-[:BELONGS_TO]->
                          (o:Organization)-[:HAS_ACCESS]->(s:System)
                    RETURN s.name as system_name
                """, user_no=user_no)
                return [record['system_name'] for record in result]
        except Exception as e:
            logging.error(f"获取用户系统失败: {e}")
            raise

    def create_unit_node(self, unit_name):
        """创建单位节点"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MERGE (u:Unit {
                        name: $unit_name
                    })
                """, unit_name=unit_name)
                logging.info(f"创建单位节点成功: {unit_name}")
        except Exception as e:
            logging.error(f"创建单位节点失败: {e}")
            raise

    def create_department_node(self, org_no, org_name):
        """创建部门节点"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MERGE (d:Department {
                        org_no: $org_no,
                        name: $org_name
                    })
                """, org_no=org_no, org_name=org_name)
                logging.info(f"创建部门节点成功: {org_name}")
        except Exception as e:
            logging.error(f"创建部门节点失败: {e}")
            raise

    def create_dept_unit_relation(self, org_no, unit_name):
        """创建部门属于单位的关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (d:Department {org_no: $org_no})
                    MATCH (u:Unit {name: $unit_name})
                    MERGE (d)-[:BELONGS_TO]->(u)
                """, org_no=org_no, unit_name=unit_name)
                logging.info(f"创建部门-单位关系成功: {org_no} -> {unit_name}")
        except Exception as e:
            logging.error(f"创建部门-单位关系失败: {e}")
            raise

    def create_user_dept_relation(self, user_no, org_no):
        """创建用户属于部门的关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (u:User {user_no: $user_no})
                    MATCH (d:Department {org_no: $org_no})
                    MERGE (u)-[:BELONGS_TO]->(d)
                """, user_no=user_no, org_no=org_no)
                logging.info(f"创建用户-部门关系成功: {user_no} -> {org_no}")
        except Exception as e:
            logging.error(f"创建用户-部门关系失败: {e}")
            raise

    def create_unit_system_relation(self, unit_name, system_no):
        """创建单位访问系统的关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (u:Unit {name: $unit_name})
                    MATCH (s:System {system_no: $system_no})
                    MERGE (u)-[:HAS_ACCESS]->(s)
                """, unit_name=unit_name, system_no=system_no)
                logging.info(f"创建单位-系统关系成功: {unit_name} -> {system_no}")
        except Exception as e:
            logging.error(f"创建单位-系统关系失败: {e}")
            raise

    def create_colleague_relation(self, user1_no, user2_no):
        """创建同事关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (u1:User {user_no: $user1_no})
                    MATCH (u2:User {user_no: $user2_no})
                    MERGE (u1)-[:IS_COLLEAGUE]->(u2)
                    MERGE (u2)-[:IS_COLLEAGUE]->(u1)
                """, user1_no=user1_no, user2_no=user2_no)
                logging.info(f"创建同事关系成功: {user1_no} <-> {user2_no}")
        except Exception as e:
            logging.error(f"创建同事关系失败: {e}")
            raise

    def create_dispatch_doc_node(self, doc_id, subject, doc_type):
        """创建发文节点"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MERGE (d:Document {id: $doc_id})
                    ON CREATE SET 
                        d.title = $subject,
                        d.type = $doc_type,
                        d.category = 'dispatch'
                    RETURN d
                """, doc_id=doc_id, subject=subject, doc_type=doc_type)
                logging.info(f"创建发文节点成功: {subject}")
                return result.single()['d']
        except Exception as e:
            logging.error(f"创建发文节点失败: {e}")
            raise

    def create_receival_doc_node(self, doc_id, subject, doc_type):
        """创建收文节点"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MERGE (d:Document {id: $doc_id})
                    ON CREATE SET 
                        d.title = $subject,
                        d.type = $doc_type,
                        d.category = 'receival'
                    RETURN d
                """, doc_id=doc_id, subject=subject, doc_type=doc_type)
                logging.info(f"创建收文节点成: {subject}")
                return result.single()['d']
        except Exception as e:
            logging.error(f"创建收文节点失败: {e}")
            raise

    def create_user_draft_dispatch(self, user_no, doc_id):
        """创建用户起草发文关系"""
        try:
            with self._driver.session() as session:
                # 先确保节点存在
                session.run("""
                    MATCH (u:User {user_no: $user_no})
                    MATCH (d:Document {id: $doc_id})
                    WITH u, d
                    MERGE (u)-[r:DRAFTED]->(d)
                    SET r.label = '起草'
                """, user_no=user_no, doc_id=doc_id)
                logging.info(f"创建用户起草发文关系成功: {user_no} -> {doc_id}")
        except Exception as e:
            logging.error(f"创建用户起草发文关系失败: {e}")
            # 添加更详细的错误信息
            logging.error(f"节点信息 - user_no: {user_no}, doc_id: {doc_id}")
            # 检查节点是否存在
            try:
                with self._driver.session() as session:
                    user_exists = session.run("""
                        MATCH (u:User {user_no: $user_no}) 
                        RETURN COUNT(u) as count
                    """, user_no=user_no).single()['count'] > 0
                    
                    doc_exists = session.run("""
                        MATCH (d:Document {id: $doc_id}) 
                        RETURN COUNT(d) as count
                    """, doc_id=doc_id).single()['count'] > 0
                    
                    logging.error(f"节点存在检查 - User exists: {user_exists}, Document exists: {doc_exists}")
            except Exception as check_error:
                logging.error(f"节点检查失败: {check_error}")
            raise

    def create_user_register_receival(self, user_no, doc_id):
        """创建用户登记收文关系"""
        try:
            with self._driver.session() as session:
                # 先检查节点是否存在
                check_query = """
                MATCH (u:User {user_no: $user_no})
                MATCH (d:Document {id: $doc_id})
                RETURN count(*) as count
                """
                result = session.run(check_query, user_no=user_no, doc_id=doc_id)
                count = result.single()['count']
                
                if count > 0:
                    # 创建关系
                    session.run("""
                        MATCH (u:User {user_no: $user_no})
                        MATCH (d:Document {id: $doc_id})
                        MERGE (u)-[r:REGISTERED]->(d)
                        SET r.label = '登记'
                    """, user_no=user_no, doc_id=doc_id)
                    logging.info(f"创建用户登记收文关系成功: {user_no} -> {doc_id}")
                else:
                    logging.warning(f"找不到用户或收文节点: user_no={user_no}, doc_id={doc_id}")
                    # 添加节点详细信息日志
                    user_exists = session.run("""
                        MATCH (u:User {user_no: $user_no}) 
                        RETURN COUNT(u) as count
                    """, user_no=user_no).single()['count'] > 0
                    
                    doc_exists = session.run("""
                        MATCH (d:Document {id: $doc_id}) 
                        RETURN COUNT(d) as count
                    """, doc_id=doc_id).single()['count'] > 0
                    
                    logging.info(f"节点存在检查 - User exists: {user_exists}, Document exists: {doc_exists}")
        except Exception as e:
            logging.error(f"创建用户登记收文关系失败: {e}")
            logging.error(f"详细信息 - user_no: {user_no}, doc_id: {doc_id}")
            raise

    def create_dept_process_doc(self, org_no, doc_id):
        """创建部门办理公文关系"""
        try:
            with self._driver.session() as session:
                session.run("""
                    MATCH (o:Organization {org_no: $org_no})
                    MATCH (d:Document {id: $doc_id})
                    MERGE (o)-[:PROCESSED]->(d)
                """, org_no=org_no, doc_id=doc_id)
                logging.info(f"创建部门办理公文关系成功: {org_no} -> {doc_id}")
        except Exception as e:
            logging.error(f"创建部门办理公文关系失败: {e}")
            raise

    def create_user_handle_doc_relation(self, handler_info, doc_id):
        """创建用户办理公文关系"""
        try:
            with self._driver.session() as session:
                # 创建办理关系，包含办理状态和时间信息
                session.run("""
                    MATCH (u:User {user_no: $user_no})
                    MATCH (d:Document {id: $doc_id})
                    MERGE (u)-[r:HANDLED]->(d)
                    SET r.state = $state,
                        r.create_time = $create_time,
                        r.label = '办理'
                """, 
                user_no=handler_info['user_no'],
                doc_id=doc_id,
                state=handler_info['state'],
                create_time=handler_info['create_time']
                )
                logging.info(f"创建用户办理关系成功: {handler_info['user_no']} -> {doc_id} ({handler_info['state']})")
        except Exception as e:
            logging.error(f"创建用户办理关系失败: {e}")
            raise

    def create_opinion_node(self, opinion_id, content, create_time):
        """创建意见节点"""
        try:
            with self._driver.session() as session:
                # 处理 create_time
                if hasattr(create_time, 'strftime'):
                    create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')
                
                # 处理 content
                if content and isinstance(content, str):
                    content = content.strip()
                    if not content:
                        content = '无内容'
                else:
                    content = '无内容'

                result = session.run("""
                    MERGE (o:Opinion {id: $opinion_id})
                    SET o.content = $content,
                        o.create_time = $create_time,
                        o.label = $content  // 设置 label 为意见内容的前20个字符
                    RETURN o
                """, 
                opinion_id=opinion_id,
                content=content,
                create_time=create_time
                )
                logging.info(f"创建意见节点成功: {opinion_id}")
                logging.info(f"意见内容: {content[:100]}...")
                return result.single()['o']
        except Exception as e:
            logging.error(f"创建意见节点失败: {e}")
            raise

    def create_user_write_opinion_relation(self, user_no, opinion_id):
        """创建用户填写意见关系"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (u:User {user_no: $user_no})
                    MATCH (o:Opinion {id: $opinion_id})
                    MERGE (u)-[r:WROTE]->(o)
                    SET r.label = '填写'
                    RETURN r
                """, user_no=user_no, opinion_id=opinion_id)
                if result.single():
                    logging.info(f"创建用户填写意见关系成功: {user_no} -> {opinion_id}")
                else:
                    logging.warning(f"未能创建用户填写意见关系: {user_no} -> {opinion_id}")
        except Exception as e:
            logging.error(f"创建用户填写意见关系失败: {e}")
            raise

    def create_opinion_belong_doc_relation(self, opinion_id, doc_id):
        """创建意见属于公文关系"""
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (o:Opinion {id: $opinion_id})
                    MATCH (d:Document {id: $doc_id})
                    MERGE (o)-[r:BELONGS_TO]->(d)
                    SET r.label = '属于'
                    RETURN r
                """, opinion_id=opinion_id, doc_id=doc_id)
                if result.single():
                    logging.info(f"创建意见属于公文关系成功: {opinion_id} -> {doc_id}")
                else:
                    logging.warning(f"未能创建意见属于公文关系: {opinion_id} -> {doc_id}")
        except Exception as e:
            logging.error(f"创建意见属于公文关系失败: {e}")
            raise