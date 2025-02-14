import unittest
import json
import subprocess
import os
import pandas as pd

class TestCalculateAverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ 在测试前创建测试 CSV 文件 """
        cls.script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本目录
        cls.test_csv = os.path.join(cls.script_dir, "test_data.csv")

        data = {
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50]
        }
        df = pd.DataFrame(data)
        df.to_csv(cls.test_csv, index=False)

    @classmethod
    def tearDownClass(cls):
        """ 测试完成后清理文件 """
        if os.path.exists(cls.test_csv):
            os.remove(cls.test_csv)
        
        output_json = os.path.join(cls.script_dir, "output.json")
        if os.path.exists(output_json):
            os.remove(output_json)

    def test_calculate_avg(self):
        """ 测试 `calculate_avg.py` 计算正确的平均值 """
        column_name = "A"
        expected_avg = 3.0  # (1+2+3+4+5) / 5 = 3.0

        script_path = os.path.join(self.script_dir, "calculate_avg.py")

        # 执行 `calculate_avg.py`
        subprocess.run(["python", script_path, self.test_csv, column_name], check=True, cwd=self.script_dir)

        # 读取 output.json 并验证结果
        output_json = os.path.join(self.script_dir, "output.json")
        with open(output_json, "r") as f:
            result = json.load(f)
        
        self.assertEqual(result["column"], column_name)
        self.assertAlmostEqual(result["average"], expected_avg, places=2)

if __name__ == "__main__":
    unittest.main()
