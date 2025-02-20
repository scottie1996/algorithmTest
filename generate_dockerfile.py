import os
import sys
import xml.etree.ElementTree as ET

# 默认基础镜像
DEFAULT_BASE_IMAGE = "python:3.8"

def parse_xml_config(operator_name):
    """
    解析 XML 获取基础镜像和启动命令
    :param operator_name: 算子名称（即 operators 目录下的子目录名）
    :return: (base_image, cmd_command)
    """
    xml_path = f"operators/{operator_name}/{operator_name}.xml"
    
    # 检查 XML 文件是否存在
    if not os.path.exists(xml_path):
        print(f"❌ Error: XML file '{xml_path}' not found.")
        sys.exit(1)
    
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 解析基础镜像
    container = root.find("container/docker")
    base_image = container.get("image") if container is not None else DEFAULT_BASE_IMAGE

    # 解析启动命令
    command = root.find("command")
    if command is not None and command.text:
        cmd_command = command.text.strip().replace("\n", " ").split()
    else:
        cmd_command = ["python", "main.py"]  # 默认执行 main.py

    return base_image, cmd_command

def generate_dockerfile(operator_name):
    """
    根据 XML 配置生成 Dockerfile
    :param operator_name: 算子名称
    """
    operator_dir = f"operators/{operator_name}"

    if not os.path.exists(operator_dir):
        print(f"❌ Error: Operator directory '{operator_dir}' not found.")
        sys.exit(1)

    # 获取 XML 解析的值
    base_image, cmd_command_list = parse_xml_config(operator_name)

    # Dockerfile 路径
    dockerfile_path = os.path.join(operator_dir, "Dockerfile")

    # 生成 Dockerfile 内容
    dockerfile_content = f"""\
# Generated Dockerfile for {operator_name}
FROM {base_image}

# 设置工作目录
WORKDIR /app

# 复制算子文件
COPY . /app

# 安装必要的依赖
RUN pip install -r requirements.txt

# 设置容器启动时运行的命令
CMD [{", ".join(f'"{cmd}"' for cmd in cmd_command_list)}]
"""

    # 写入 Dockerfile
    with open(dockerfile_path, "w", encoding="utf-8") as f:
        f.write(dockerfile_content)

    print(f"✅ Dockerfile for {operator_name} generated successfully at {dockerfile_path}")
    
    # 打印 Dockerfile 内容
    print("\n==== Generated Dockerfile ====")
    print(dockerfile_content)
    print("================================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python generate_dockerfile.py <operator_name>")
        sys.exit(1)

    operator_name = sys.argv[1]
    generate_dockerfile(operator_name)
