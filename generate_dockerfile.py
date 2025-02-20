import os
import sys

# 默认基础镜像
DEFAULT_BASE_IMAGE = "python:3.8-slim"

def generate_dockerfile(operator_name, base_image=DEFAULT_BASE_IMAGE):
    """
    生成指定算子的 Dockerfile
    :param operator_name: 算子名称（即 operators 目录下的子目录名）
    :param base_image: 运行环境的基础镜像，默认为 Python 3.8 Slim 版
    """
    
    # 指定算子的目录路径
    operator_dir = f"operators/{operator_name}"
    
    # 检查算子目录是否存在
    if not os.path.exists(operator_dir):
        print(f"❌ Error: Operator directory '{operator_dir}' not found.")
        sys.exit(1)

    # Dockerfile 目标路径
    dockerfile_path = os.path.join(operator_dir, "Dockerfile")

    # 这里可以根据不同的算子设置不同的启动命令
    cmd_command_list = ["python", "main.py"]  # 假设默认启动 main.py

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
    
    # 打印 Dockerfile 内容（用于 GitHub Actions 方便查看）
    print("\n==== Generated Dockerfile ====")
    print(dockerfile_content)
    print("================================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python generate_dockerfile.py <operator_name>")
        sys.exit(1)

    operator_name = sys.argv[1]
    generate_dockerfile(operator_name)
