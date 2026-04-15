# =============================================================
# 第15节：推导式（Comprehensions）
# =============================================================
# 推导式是 Python 的特色语法，可以用简洁的一行代码
# 创建列表、字典、集合或生成器。
# =============================================================

# -------------------------------------------------------
# 1. 列表推导式（List Comprehension）
# -------------------------------------------------------
print("--- 列表推导式 ---")

# 基本语法：[表达式 for 变量 in 可迭代对象]

# 普通写法
squares_normal = []
for n in range(1, 6):
    squares_normal.append(n ** 2)
print("普通写法:", squares_normal)

# 推导式写法
squares = [n ** 2 for n in range(1, 6)]
print("推导式写法:", squares)

# 遍历字符串
chars = [c.upper() for c in "hello"]
print(chars)    # ['H', 'E', 'L', 'L', 'O']

# 带条件过滤：[表达式 for 变量 in 可迭代 if 条件]
evens = [n for n in range(1, 11) if n % 2 == 0]
print("偶数:", evens)    # [2, 4, 6, 8, 10]

# 复杂条件
result = [n if n % 2 == 0 else -n for n in range(1, 6)]
print("条件表达式:", result)    # [-1, 2, -3, 4, -5]

# 嵌套循环推导式
pairs = [(x, y) for x in range(1, 4) for y in range(1, 4) if x != y]
print("不重复对:", pairs)

# 嵌套列表展开（flatten）
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [item for row in matrix for item in row]
print("展开矩阵:", flat)

# -------------------------------------------------------
# 2. 字典推导式（Dict Comprehension）
# -------------------------------------------------------
print("\n--- 字典推导式 ---")

# 基本语法：{键: 值 for 变量 in 可迭代对象}

# 数字到其平方的映射
squares_dict = {n: n**2 for n in range(1, 6)}
print(squares_dict)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 从两个列表创建字典
keys = ["a", "b", "c", "d"]
values = [1, 2, 3, 4]
d = {k: v for k, v in zip(keys, values)}
print(d)    # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 反转字典（键值互换）
original = {"apple": 1, "banana": 2, "cherry": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)    # {1: 'apple', 2: 'banana', 3: 'cherry'}

# 过滤字典
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Dave": 96, "Eve": 60}
high_scores = {name: score for name, score in scores.items() if score >= 80}
print("高分学生:", high_scores)

# 转换字典值
upper_names = {k.upper(): v for k, v in scores.items()}
print("大写键:", upper_names)

# -------------------------------------------------------
# 3. 集合推导式（Set Comprehension）
# -------------------------------------------------------
print("\n--- 集合推导式 ---")

# 基本语法：{表达式 for 变量 in 可迭代对象}

# 平方数集合（自动去重）
squares_set = {n**2 for n in range(-3, 4)}
print(squares_set)    # {0, 1, 4, 9}（无序，去重）

# 从字符串提取唯一字符
unique_chars = {c.lower() for c in "Hello World" if c.isalpha()}
print("唯一字母:", unique_chars)

# -------------------------------------------------------
# 4. 生成器表达式（Generator Expression）
# -------------------------------------------------------
print("\n--- 生成器表达式 ---")

# 语法与列表推导式相同，但使用小括号 ()
# 生成器是懒计算的，不会立即生成所有元素，节省内存

# 列表推导式（立即计算，占用内存）
lst = [n**2 for n in range(1_000_000)]  # 创建100万元素的列表
print(f"列表第一个元素：{lst[0]}")

# 生成器表达式（懒计算，内存高效）
gen = (n**2 for n in range(1_000_000))  # 几乎不占内存
print(f"生成器：{gen}")
print(f"生成器第一个值：{next(gen)}")
print(f"生成器第二个值：{next(gen)}")

# 迭代生成器
gen_small = (n**2 for n in range(5))
for value in gen_small:
    print(value, end=" ")
print()

# 生成器表达式常用于函数参数（避免额外的括号）
total = sum(n**2 for n in range(1, 11))
print(f"1到10的平方和：{total}")

max_value = max(len(word) for word in ["apple", "banana", "cherry"])
print(f"最长单词长度：{max_value}")

# -------------------------------------------------------
# 5. 嵌套推导式
# -------------------------------------------------------
print("\n--- 嵌套推导式 ---")

# 矩阵转置
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print("转置矩阵:")
for row in transposed:
    print(row)

# 生成棋盘坐标
board = [(r, c) for r in range(8) for c in range(8)]
print(f"棋盘共 {len(board)} 个格子")
print(f"前5个：{board[:5]}")

# -------------------------------------------------------
# 6. 推导式 vs 循环 - 何时使用推导式
# -------------------------------------------------------
print("\n--- 推导式使用建议 ---")
print("""
推导式的优点：
  ✓ 代码更简洁
  ✓ 通常比等价的 for 循环更快
  ✓ Python 风格（Pythonic）

使用建议：
  ✓ 简单的映射和过滤操作
  ✓ 单行或两行以内
  ✗ 逻辑复杂时，用普通循环更清晰
  ✗ 包含副作用的操作（如打印、修改外部变量）
""")

# 示例：这种情况不推荐用推导式
# 不好的用法（有副作用）
results = []
[results.append(n**2) for n in range(5)]    # 避免这样写

# 好的用法
results = [n**2 for n in range(5)]          # 推荐

# -------------------------------------------------------
# 7. 实用案例
# -------------------------------------------------------
print("--- 实用案例 ---")

# 案例1：处理文本数据
text = "The quick brown fox jumps over the lazy dog"
word_lengths = {word: len(word) for word in text.split()}
long_words = [w for w, l in word_lengths.items() if l > 4]
print("长度 > 4 的单词:", long_words)

# 案例2：数据转换
raw_data = ["1", "2", "3", "abc", "4", "xyz", "5"]
valid_numbers = [int(x) for x in raw_data if x.isdigit()]
print("有效数字:", valid_numbers)

# 案例3：笛卡尔积生成组合
colors = ["红", "绿", "蓝"]
sizes = ["S", "M", "L"]
products = [f"{c}-{s}" for c in colors for s in sizes]
print("产品组合:", products)

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 用列表推导式生成 1-100 中所有能被 3 或 5 整除的数
# 2. 给定学生成绩字典，用字典推导式创建 {姓名: 等级} 的字典
# 3. 用生成器表达式计算文件中所有行的总字符数（不含换行符）

print("\n--- 练习参考答案 ---")
# 1. 被 3 或 5 整除
result = [n for n in range(1, 101) if n % 3 == 0 or n % 5 == 0]
print(f"被3或5整除的数（共{len(result)}个）：{result}")

# 2. 成绩转等级
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Dave": 96, "Eve": 60}
grade_letters = {
    name: ("A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D")
    for name, score in grades.items()
}
print("成绩等级:", grade_letters)

# 3. 生成器求字符总数
import io
fake_file = io.StringIO("Hello World\nPython is great\nLet's code")
total_chars = sum(len(line.rstrip("\n")) for line in fake_file)
print(f"总字符数：{total_chars}")
