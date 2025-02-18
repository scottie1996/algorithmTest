import os
import yaml
import json

OPERATORS_DIR = "operators"
OUTPUT_FILE = "operators_list.json"

def get_operator_info(yaml_path):
    """解析 operator.yaml，获取算子名称和版本"""
    with open(yaml_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return {
            "name": data.get("operatorName"),
            "version": data.get("version"),
            "description": data.get("operatorDescription", ""),
            "author": data.get("author", {}).get("name", ""),
        }

def update_operator_list():
    """遍历 operators 目录，更新 operators_list.json"""
    operators = []
    
    for operator in os.listdir(OPERATORS_DIR):
        yaml_path = os.path.join(OPERATORS_DIR, operator, "operator.yaml")
        if os.path.exists(yaml_path):
            operators.append(get_operator_info(yaml_path))

    # 按算子名称排序
    operators.sort(key=lambda x: x["name"])

    # 写入 JSON 文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(operators, file, indent=4, ensure_ascii=False)

    print(f"✅ 算子列表已更新：{OUTPUT_FILE}")

if __name__ == "__main__":
    update_operator_list()
