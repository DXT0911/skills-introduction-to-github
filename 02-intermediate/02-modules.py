# =============================================================
# 第12节：模块与包（Modules and Packages）
# =============================================================
# 模块是一个 .py 文件，包含可复用的代码。
# 包是一个包含 __init__.py 的目录，用于组织多个模块。
# =============================================================

# -------------------------------------------------------
# 1. 导入标准库模块
# -------------------------------------------------------
print("--- 导入模块 ---")

# 导入整个模块
import math
print(math.pi)              # 3.141592653589793
print(math.sqrt(16))        # 4.0
print(math.ceil(3.2))       # 4
print(math.floor(3.8))      # 3
print(math.log(100, 10))    # 2.0

# 导入特定函数/变量
from math import sqrt, pi
print(sqrt(25))             # 5.0
print(pi)                   # 3.141592653589793

# 导入并重命名
import math as m
from math import factorial as fact
print(m.cos(0))             # 1.0
print(fact(5))              # 120

# -------------------------------------------------------
# 2. 常用标准库
# -------------------------------------------------------
print("\n--- 常用标准库 ---")

# random - 随机数
import random
print(random.random())                      # [0.0, 1.0) 的随机浮点数
print(random.randint(1, 10))               # 1-10 的随机整数
print(random.choice(["a", "b", "c"]))      # 随机选择一个元素
lst = [1, 2, 3, 4, 5]
random.shuffle(lst)                         # 就地随机排列
print(lst)
print(random.sample(range(100), 5))        # 不重复地随机选 5 个

# os - 操作系统接口
import os
print("\nos 模块：")
print(os.getcwd())                          # 当前工作目录
print(os.path.exists("/tmp"))               # 路径是否存在
print(os.path.join("folder", "file.txt"))  # 拼接路径
print(os.path.basename("/a/b/c.txt"))       # c.txt
print(os.path.dirname("/a/b/c.txt"))        # /a/b
print(os.path.splitext("file.txt"))         # ('file', '.txt')

# sys - 系统相关
import sys
print("\nsys 模块：")
print(sys.version)                          # Python 版本
print(sys.platform)                         # 操作系统平台
print(sys.path[:2])                         # 模块搜索路径（前两个）

# datetime - 日期时间
from datetime import datetime, date, timedelta
print("\ndatetime 模块：")
now = datetime.now()
print(now)
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # 格式化
today = date.today()
print(today)
print(today + timedelta(days=7))            # 一周后

# json - JSON 数据处理
import json
print("\njson 模块：")
data = {"name": "Alice", "age": 25, "hobbies": ["reading", "coding"]}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)
parsed = json.loads(json_str)
print(parsed["name"])

# collections - 高级数据结构
from collections import Counter, defaultdict, OrderedDict, deque
print("\ncollections 模块：")

# Counter - 计数器
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
print(counter)                              # Counter({'apple': 3, ...})
print(counter.most_common(2))              # 最常见的 2 个

# defaultdict - 带默认值的字典
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["vegs"].append("carrot")
print(dict(dd))

# deque - 双端队列
dq = deque([1, 2, 3])
dq.appendleft(0)             # 在左端添加
dq.append(4)                 # 在右端添加
print(dq)                    # deque([0, 1, 2, 3, 4])
print(dq.popleft())          # 从左端弹出：0

# itertools - 迭代器工具
import itertools
print("\nitertools 模块：")
# product - 笛卡尔积
for combo in itertools.product([1, 2], ["a", "b"]):
    print(combo, end=" ")
print()

# chain - 链接多个迭代器
for item in itertools.chain([1, 2], [3, 4], [5]):
    print(item, end=" ")
print()

# combinations - 组合
for combo in itertools.combinations([1, 2, 3, 4], 2):
    print(combo, end=" ")
print()

# -------------------------------------------------------
# 3. 第三方库（需要 pip 安装）
# -------------------------------------------------------
print("\n--- 第三方库介绍 ---")
print("""
常用第三方库：

数据处理：
  pip install numpy        # 数值计算
  pip install pandas       # 数据分析

可视化：
  pip install matplotlib   # 绘图
  pip install seaborn      # 统计可视化

Web 开发：
  pip install flask        # 轻量级 Web 框架
  pip install django       # 全功能 Web 框架
  pip install fastapi      # 现代异步 API 框架

网络请求：
  pip install requests     # HTTP 请求
  pip install httpx        # 异步 HTTP 请求

机器学习：
  pip install scikit-learn  # 机器学习
  pip install tensorflow    # 深度学习
  pip install torch         # PyTorch 深度学习
""")

# -------------------------------------------------------
# 4. __name__ 变量
# -------------------------------------------------------
print("--- __name__ 变量 ---")
print(f"当前模块名：{__name__}")

# 当直接运行文件时，__name__ 等于 "__main__"
# 当被其他模块导入时，__name__ 等于模块名
# 这个模式常用于区分直接运行和被导入的情况：

if __name__ == "__main__":
    print("这段代码只在直接运行时执行，不会在被导入时执行")

# -------------------------------------------------------
# 5. 模块搜索路径
# -------------------------------------------------------
print("\n--- 模块搜索路径 ---")
import sys
# Python 按以下顺序查找模块：
# 1. 当前目录
# 2. PYTHONPATH 环境变量中的目录
# 3. Python 安装目录下的标准库目录
# 4. 已安装的第三方包目录
print("搜索路径（前3个）:")
for p in sys.path[:3]:
    print(f"  {p}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 使用 random 模块生成一个 6 位随机验证码（数字+字母）
# 2. 使用 datetime 计算今天到年底还有多少天
# 3. 使用 Counter 统计一段文字中出现最多的 5 个单词

print("\n--- 练习参考答案 ---")
# 1. 随机验证码
import string
chars = string.ascii_letters + string.digits
code = "".join(random.choices(chars, k=6))
print(f"验证码：{code}")

# 2. 距年底天数
from datetime import date
today = date.today()
year_end = date(today.year, 12, 31)
days_left = (year_end - today).days
print(f"距 {today.year} 年底还有 {days_left} 天")

# 3. 词频统计
text = "to be or not to be that is the question to be"
word_counter = Counter(text.split())
print("出现最多的 5 个单词：")
for word, count in word_counter.most_common(5):
    print(f"  '{word}': {count} 次")
