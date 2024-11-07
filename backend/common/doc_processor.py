from docx import Document
import re

def process_docx(file_path):
    """处理 docx 文档，提取标题和内容"""
    doc = Document(file_path)
    sections = []
    current_section = None

    for paragraph in doc.paragraphs:
        # 检查段落的样式是否是标题
        if paragraph.style.name.startswith('Heading'):
            # 如果有上一个部分，保存它
            if current_section:
                sections.append(current_section)
            # 创建新的部分
            current_section = {
                'title': paragraph.text.strip(),
                'level': int(paragraph.style.name[-1]),  # 获取标题级别
                'content': []
            }
        elif current_section is not None:
            # 如果有内容，添加到当前部分
            if paragraph.text.strip():
                current_section['content'].append(paragraph.text.strip())
        else:
            # 如果还没有标题但有内容，创建一个无标题的部分
            if paragraph.text.strip():
                current_section = {
                    'title': '无标题',
                    'level': 0,
                    'content': [paragraph.text.strip()]
                }

    # 添加最后一个部分
    if current_section:
        sections.append(current_section)

    return sections 