import unittest
import json
import subprocess
import os
import pandas as pd

class TestCalculateAverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ 在测试前创建测试 CSV 文件 """
        cls.test_csv = "test_data.csv"
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
        if os.path.exists("output.json"):
            os.remove("output.json")

    def test_calculate_avg(self):
        """ 测试 `calculate_avg.py` 计算正确的平均值 """
        column_name = "A"
        expected_avg = 3.0  # (1+2+3+4+5) / 5 = 3.0

        # 执行 `calculate_avg.py`
        subprocess.run(["python", "calculate_avg.py", self.test_csv, column_name], check=True)

        # 读取 output.json 并验证结果
        with open("output.json", "r") as f:
            result = json.load(f)
        
        self.assertEqual(result["column"], column_name)
        self.assertAlmostEqual(result["average"], expected_avg, places=2)

if __name__ == "__main__":
    unittest.main()
