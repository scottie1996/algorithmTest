from typing import List

def process_tiff(input_path: str, output_prefix: str, file_name: str, ext: str) -> List[str]:
    """
    处理 CBF 文件的入口函数（伪代码框架）

    :param input_path: 原始 CBF 文件路径
    :param output_prefix: 输出目录
    :param file_name: 原始文件名（不含后缀）
    :param ext: 扩展名（应为 .cbf）
    :return: 生成的文件路径列表
    """
    # 这里应包含读取、解析、转换逻辑
    print(f"处理 tiff 文件: {input_path}")
    
    # 模拟输出
    output_file = f"{output_prefix}/{file_name}_processed.csv"
    return [output_file]
