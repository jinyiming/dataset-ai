import json
import requests
from typing import List, Dict
import re
from pprint import pprint
from sqlalchemy import  Column, Integer, String, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class QAPair(Base):
    __tablename__ = 'QA_INFO'
    
    id = Column(CHAR(16), primary_key=True, default=lambda: str(uuid.uuid4()))
    q_id = Column(CHAR(16), nullable=False)
    question = Column(String(5000), nullable=False)
    answer = Column(String(5000), nullable=False)
    draft_user_name = Column(String(64), default='jin')
    draft_date = Column(TIMESTAMP, nullable=False)

class QInfo(Base):
    __tablename__ = 'Q_Info'
    
    id = Column(CHAR(16), primary_key=True, default=lambda: str(uuid.uuid4()))
    q_content = Column(String(5000), nullable=False)



class QAModel:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "qwen2"
        self.fomat = "json"

    def _generate_prompt(self, user_prompt: str, count: int) -> str:
        return f"""
        请生成{count}个问答对，必须严格按照以下JSON格式返回，不要包含任何其他内容：
        {{
            "qa_pairs": [
                {{
                    "question": "问题1",
                    "answer": "答案1"
                }},
                {{
                    "question": "问题2",
                    "answer": "答案2"
                }}
            ]
        }}
        注意：所有字符串必须使用双引号，不能使用单引号。
        
        用户提示：{user_prompt}
        """

    def _fix_json_string(self, json_str: str) -> str:
        """
        修复不完整或格式错误的JSON字符串
        """
        try:
            # 1. 清理前缀和后缀的非JSON内容
            json_start = json_str.find('{')
            json_end = json_str.rfind('}')
            if json_start == -1 or json_end == -1:
                return "{}"
            json_str = json_str[json_start:json_end + 1]

            # 2. 替换所有单引号为双引号
            json_str = json_str.replace("'", '"')

            # 3. 修复键的引号
            json_str = re.sub(r'([{,]\s*)(\w+)(:)', r'\1"\2"\3', json_str)

            # 4. 修复字符串值的引号
            def fix_string_values(match):
                key = match.group(1)
                value = match.group(2)
                # 如果值没有被引号包围，添加双引号
                if not (value.startswith('"') and value.endswith('"')):
                    value = f'"{value}"'
                return f'{key}:{value}'

            json_str = re.sub(r'"(\w+)":\s*([^,}\]]+)', fix_string_values, json_str)

            # 5. 确保JSON结构完整
            if not json_str.endswith('}'):
                json_str += '}'
            if '"qa_pairs"' in json_str and not json_str.endswith(']}'):
                json_str += ']}'

            # 6. 修复可能的多余逗号
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

            # 7. 修复转义字符
            json_str = json_str.replace('\\"', '"')
            json_str = json_str.replace('\\n', ' ')

            # 8. 验证并格式化JSON
            try:
                parsed = json.loads(json_str)
                return json.dumps(parsed, ensure_ascii=False)
            except json.JSONDecodeError as e:
                print(f"JSON格式化失败: {e}")
                return json_str

        except Exception as e:
            print(f"JSON修复过程出错: {e}")
            return json_str

    def generate(self, prompt: str, count: int) -> List[Dict[str, str]]:
        try:
            request_data = {
                "model": self.model,
                "prompt": self._generate_prompt(prompt, count),
                "format": "json",
                "stream": False
            }

            response = requests.post(self.api_url, json=request_data)
            response.raise_for_status()
            
            result = response.json()
            print("原始响应:")
            pprint(result)
            
            generated_text = result.get('response', '')
            print(f"\n生成的文本:\n{generated_text}")
            
            try:
                # 尝试修复和解析JSON
                # fixed_json = self._fix_json_string(generated_text)
                # print(f"\n修复后的JSON:\n{fixed_json}")
                
                qa_data = json.loads(generated_text)
                qa_pairs = qa_data.get('qa_pairs', [])
                
                # 验证和清理数据
                cleaned_pairs = []
                for pair in qa_pairs[:count]:
                    if isinstance(pair, dict) and 'question' in pair and 'answer' in pair:
                        # 清理和规范化文本
                        question = str(pair['question']).strip()
                        answer = str(pair['answer']).strip()
                        
                        # 确保问题以问号结束
                        if not question.endswith('?') and not question.endswith('？'):
                            question += '？'
                        
                        # 确保答案正确结束
                        if not answer.endswith('.') and not answer.endswith('。'):
                            answer += '。'
                            
                        cleaned_pairs.append({
                            'question': question,
                            'answer': answer
                        })
                
                if cleaned_pairs:
                    return cleaned_pairs
                else:
                    print("清理后的数据为空，使用后备响应")
                    return self._generate_fallback_response(count)
                    
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}\n生成的文本: {generated_text}")
                print(f"尝试修复后的JSON: {generated_text}")
                return self._generate_fallback_response(count)
                
        except requests.RequestException as e:
            print(f"API请求错误: {str(e)}")
            return self._generate_fallback_response(count)
        except Exception as e:
            print(f"未预期的错误: {str(e)}")
            return self._generate_fallback_response(count)

    def _generate_fallback_response(self, count: int) -> List[Dict[str, str]]:
        """
        当API调用失败时生成后备响应
        """
        fallback_responses = [
            {
                "question": "什么是Python?",
                "answer": "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。"
            },
            {
                "question": "Python的主要特点是什么?",
                "answer": "Python的主要特点包括：易学易用、可读性强、丰富的库支持、跨平台等。"
            }
        ]
        
        result = []
        for i in range(count):
            if i < len(fallback_responses):
                result.append(fallback_responses[i])
            else:
                result.append({
                    "question": f"示例问题 {i + 1}?",
                    "answer": f"这是示例问题 {i + 1} 的�����答案。"
                })
        return result

