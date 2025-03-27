import json
import requests
from typing import List, Dict, Optional
import re
from pprint import pprint
from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from openai import OpenAI
from enum import Enum

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

class ModelType(Enum):
    DEEPSEEK_API = "deepseek_api"
    OLLAMA_LOCAL = "ollama_local"

class QAModel:
    def __init__(self, model_type: ModelType = ModelType.OLLAMA_LOCAL):
        self.model_type = model_type
        
        # DeepSeek API 配置
        self.client = OpenAI(
            api_key="sk-46a9f09bca724f6fba4eeef28d0030ba", 
            base_url="https://api.deepseek.com"
        ) if model_type == ModelType.DEEPSEEK_API else None
        
        # Ollama 本地配置
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "deepseek-r1:7b"

    def _generate_prompt(self, user_prompt: str, count: int) -> str:
        return f"""你是一个问答生成助手。请根据用户提示生成{count}个问答对。

严格要求：
1. 必须使用以下JSON格式返回
2. 不要包含任何其他内容或解释
3. 所有字符串必须使用双引号
4. JSON必须完全符合以下格式，不能有任何变化

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

用户提示：{user_prompt}"""

    def _fix_json_string(self, json_str: str) -> str:
        """移除所有<think>标签及其内容"""
        try:
            print("\n=== JSON提取开始 ===")
            print(f"1. 原始输入:\n{json_str}")
            
            # 移除所有<think>标签及其内容
            json_str = re.sub(r'<think>.*?</think>', '', json_str, flags=re.DOTALL)
            
            print(f"\n2. 移除标签后的内容:\n{json_str}")
            return json_str.strip()  # 移除首尾空白字符
                
        except Exception as e:
            print(f"\nJSON提取过程出错: {e}")
            return json_str

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """调用 Ollama 本地模型"""
        try:
            request_data = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=request_data)
            
            if response.status_code != 200:
                print(f"API 错误响应: {response.text}")
                return None
            
            response_data = response.json()
            generated_text = response_data.get('response', '')
            
            if not generated_text:
                print("警告：API 返回的响应内容为空")
                return None
            
            # 只提取JSON部分
            extracted_json = self._fix_json_string(generated_text)
            print(f"\n提取的JSON内容:\n{extracted_json}")
            
            try:
                # 验证JSON是否有效7dbf1325-50cd-4f21-8918-241d69aad40f
                # json.loads(extracted_json)
                return extracted_json
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                return None
                
        except Exception as e:
            print(f"调用过程出错: {str(e)}")
            return None

    def _call_deepseek(self, prompt: str) -> Optional[str]:
        """调用 DeepSeek API"""
        try:
            messages = [
                {"role": "system", "content": "你是一个帮助生成问答对的助手。请严格按照指定的 JSON 格式返回结果。"},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek API 调用失败: {str(e)}")
            return None

    def generate(self, prompt: str, count: int) -> List[Dict[str, str]]:
        try:
            print(f"\n开始生成问答对...")
            print(f"模型类型: {self.model_type.value}")
            print(f"请求生成数量: {count}")
            
            full_prompt = self._generate_prompt(prompt, count)
            print(f"\n完整提示词:\n{full_prompt}")
            
            # 根据选择的模型类型调用相应的 API
            if self.model_type == ModelType.OLLAMA_LOCAL:
                print("\n使用 Ollama 本地模型...")
                generated_text = self._call_ollama(full_prompt)
            else:
                print("\n使用 DeepSeek API...")
                generated_text = self._call_deepseek(full_prompt)

            if not generated_text:
                print("\n没有获取到模型返回内容，使用后备响应")
                return self._generate_fallback_response(count)

            print(f"\n----------------s成功获取模型返回内容:\n{generated_text}")
            
            try:
                qa_data = json.loads(generated_text)
                qa_pairs = qa_data.get('qa_pairs', [])
                
                # 验证和清理数据
                cleaned_pairs = []
                for pair in qa_pairs[:count]:
                    if isinstance(pair, dict) and 'question' in pair and 'answer' in pair:
                        question = str(pair['question']).strip()
                        answer = str(pair['answer']).strip()
                        
                        if not question.endswith('?') and not question.endswith('？'):
                            question += '？'
                        
                        if not answer.endswith('.') and not answer.endswith('。'):
                            answer += '。'
                            
                        cleaned_pairs.append({
                            'question': question,
                            'answer': answer
                        })
                
                if cleaned_pairs:
                    return cleaned_pairs
                
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                
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
                    "answer": f"这是示例问题 {i + 1} 的答案。"
                })
        return result
