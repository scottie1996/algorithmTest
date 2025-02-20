import os
import json
import xml.etree.ElementTree as ET

OPERATORS_DIR = "operators"
OUTPUT_JSON_FILE = "operators_list.json"

def parse_operator_xml(operator_name):
    xml_file = os.path.join(OPERATORS_DIR, operator_name, f"{operator_name}.xml")

    if not os.path.exists(xml_file):
        print(f"❌ XML file not found: {xml_file}")
        return None

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取基础信息
    operator_info = {
        "name": root.get("id"),
        "version": root.get("version"),
        "description": root.findtext("description", ""),
        "help": root.findtext("help", "").strip(),
        "requirements": [],
        "inputs": [],
        "outputs": []
    }

    # 提取基础镜像
    container_elem = root.find("container/docker")
    if container_elem is not None:
        operator_info["base_image"] = container_elem.get("image", "python:latest")
    else:
        operator_info["base_image"] = "python:latest"

    # 提取依赖
    requirements_elem = root.find("requirements")
    if requirements_elem is not None:
        for req in requirements_elem.findall("requirement"):
            operator_info["requirements"].append(req.text.strip())

    # 提取输入参数
    inputs_elem = root.find("inputs")
    if inputs_elem is not None:
        for param in inputs_elem.findall("param"):
            operator_info["inputs"].append({
                "name": param.get("name"),
                "type": param.get("type"),
                "format": param.get("format", ""),
                "label": param.get("label", ""),
                "help": param.get("help", "")
            })

    # 提取输出参数
    outputs_elem = root.find("outputs")
    if outputs_elem is not None:
        for output in outputs_elem.findall("data"):
            operator_info["outputs"].append({
                "name": output.get("name"),
                "format": output.get("format", ""),
                "label": output.get("label", "")
            })

    return operator_info

def generate_operators_list():
    operators = []

    # 遍历所有 operators 目录
    for operator_name in os.listdir(OPERATORS_DIR):
        operator_path = os.path.join(OPERATORS_DIR, operator_name)
        if os.path.isdir(operator_path):
            operator_data = parse_operator_xml(operator_name)
            if operator_data:
                operators.append(operator_data)

    # 写入 JSON 文件
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(operators, f, indent=4, ensure_ascii=False)

    print(f"✅ Successfully generated {OUTPUT_JSON_FILE}")

if __name__ == "__main__":
    generate_operators_list()
