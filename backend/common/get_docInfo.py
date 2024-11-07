from docx import Document
import os
from collections import defaultdict
from typing import List, Dict, Any

class DocxStructureReader:
    def __init__(self):
        self.document_structure = []
        # 标题样式名称映射
        self.heading_styles = {
            'Heading 1': 1,
            'Heading 2': 2,
            'Heading 3': 3,
            '标题 1': 1,
            '标题 2': 2,
            '标题 3': 3
        }
    
    def read_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """
        读取Word文档并解析其结构
        
        Args:
            file_path (str): Word文档的路径
        
        Returns:
            List[Dict[str, Any]]: 包含文档结构的列表
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            doc = Document(file_path)
            current_section = None
            current_content = []
            
            for paragraph in doc.paragraphs:
                # 检查段落是否是标题
                heading_level = self._get_heading_level(paragraph)
                
                if heading_level:  # 如果是标题
                    # 如果之前有未处理的段落，先保存
                    if current_section:
                        self.document_structure.append({
                            'type': 'heading',
                            'level': current_section['level'],
                            'text': current_section['heading'],
                            'content': {
                                'type': 'content',
                                'text': '\n'.join(current_content)
                            } if current_content else None
                        })
                    
                    # 开始新的段落
                    current_section = {
                        'level': heading_level,
                        'heading': paragraph.text.strip()
                    }
                    current_content = []
                
                elif current_section and paragraph.text.strip():  # 如果不是标题且内容不为空
                    current_content.append(paragraph.text.strip())
            
            # 处理最后一个段落
            if current_section:
                self.document_structure.append({
                    'type': 'heading',
                    'level': current_section['level'],
                    'text': current_section['heading'],
                    'content': {
                        'type': 'content',
                        'text': '\n'.join(current_content)
                    } if current_content else None
                })
            
            return self.document_structure
            
        except Exception as e:
            print(f"读取文档时出错: {str(e)}")
            return []
    
    def _get_heading_level(self, paragraph) -> int:
        """
        获取段落的标题级别
        
        Args:
            paragraph: 文档段落对象
        
        Returns:
            int: 标题级别（1-3），如果不是标题返回0
        """
        if paragraph.style.name in self.heading_styles:
            return self.heading_styles[paragraph.style.name]
        return 0
    
    def print_structure(self):
        """
        打印文档结构，清晰区分标题和内容
        """
        for section in self.document_structure:
            # 打印标题
            indent = '  ' * (section['level'] - 1)
            heading_marks = '#' * section['level']
            print(f"\n{indent}[标题 {section['level']}级] {heading_marks} {section['text']}")
            
            # 打印内容
            if section['content']:
                print(f"{indent}[内容]\n{indent}{section['content']['text']}")
            else:
                print(f"{indent}[内容] 该标题下没有内容")
    
    def export_to_markdown(self, output_path: str):
        """
        将文档结构导出为Markdown格式
        
        Args:
            output_path (str): 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for section in self.document_structure:
                # 写入标题
                indent = '  ' * (section['level'] - 1)
                heading_marks = '#' * section['level']
                f.write(f"\n{heading_marks} {section['text']}\n")
                
                # 写入内容
                if section['content']:
                    f.write(f"\n{section['content']['text']}\n")

def main():
    # 使用示例
    reader = DocxStructureReader()
    
    # 替换为您的文档路径
    docx_path = '关键技术设计.docx'
    
    try:
        structure = reader.read_docx(docx_path)
        if structure:
            print("文档结构解析结果：")
            reader.print_structure()
            
            # 导出为Markdown文件（可选）
            reader.export_to_markdown('output.md')
            print("\n文档已导出为 output.md")
        else:
            print("未能解析出文档结构。")
    
    except Exception as e:
        print(f"处理文档时发生错误: {str(e)}")

if __name__ == '__main__':
    main()