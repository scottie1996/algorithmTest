import pandas as pd
import sys
import json

def calculate_average(csv_file, column_name):
    df = pd.read_csv(csv_file)
    if column_name not in df.columns:
        raise ValueError(f"列 {column_name} 不存在")
    avg_value = df[column_name].mean()
    
    result = {"column": column_name, "average": avg_value}
    with open("output.json", "w") as f:
        json.dump(result, f)
    
    print("计算完成，结果已保存到 output.json")

if __name__ == "__main__":
    input_csv = sys.argv[1]
    column_name = sys.argv[2]
    calculate_average(input_csv, column_name)
