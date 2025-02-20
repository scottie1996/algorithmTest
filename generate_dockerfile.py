import os
import xmltodict
import sys

def generate_dockerfile(operator_name):
    # 定义 XML 文件路径和 Dockerfile 路径
    xml_file_path = f"operators/{operator_name}/{operator_name}.xml"
    dockerfile_path = f"operators/{operator_name}/Dockerfile"

    # 检查文件是否存在
    if not os.path.isfile(xml_file_path):
        raise FileNotFoundError(f"{xml_file_path} not found!")

    # 解析 XML 文件
    with open(xml_file_path, 'r') as xml_file:
        xml_content = xmltodict.parse(xml_file.read())
    
    # 提取基础镜像和其他信息
    base_image = xml_content['tool']['container']['docker']['@image']
    cmd_command = xml_content['tool']['command']
    
    # 处理 CMD 命令（如果有）
    if cmd_command and '[CDATA[' in cmd_command:
        cmd_command = cmd_command.replace('[CDATA[', '').replace(']]', '')
    cmd_command_list = cmd_command.split()

    # 生成 Dockerfile 内容
    dockerfile_content = f"""
    # Generated Dockerfile for {operator_name}
    FROM {base_image}

    # 设置工作目录
    WORKDIR /app

    # 复制算子文件
    COPY . /app

    # 安装必要的依赖
    RUN pip install -r requirements.txt

    # 设置容器启动时运行的命令
    CMD ["{'", "','".join(cmd_command_list)}"]
    """

    # 写入 Dockerfile 文件
    with open(dockerfile_path, 'w') as dockerfile:
        dockerfile.write(dockerfile_content)
    
    print(f"Dockerfile for {operator_name} has been generated at {dockerfile_path}")


# 从命令行获取算子名称并生成 Dockerfile
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_dockerfile.py <operator_name>")
        sys.exit(1)
    
    operator_name = sys.argv[1]
    generate_dockerfile(operator_name)
