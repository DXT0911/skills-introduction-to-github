# =============================================================
# 第7节：字典（Dictionary）
# =============================================================
# 字典是键值对（key-value）的集合，无序（Python 3.7+ 保持插入顺序）。
# 键必须是不可变类型（字符串、数字、元组），值可以是任意类型。
# =============================================================

# -------------------------------------------------------
# 1. 创建字典
# -------------------------------------------------------
print("--- 创建字典 ---")
empty_dict = {}
person = {"name": "Alice", "age": 25, "city": "Beijing"}
scores = {"math": 95, "english": 88, "science": 92}
mixed = {"id": 1, "active": True, "tags": ["python", "coding"]}

print(person)
print(scores)

# 用 dict() 创建
d1 = dict(name="Bob", age=30)
d2 = dict([("a", 1), ("b", 2)])  # 从键值对列表创建
print(d1)
print(d2)

# 用 fromkeys() 批量创建（同一个默认值）
keys = ["x", "y", "z"]
d3 = dict.fromkeys(keys, 0)
print(d3)    # {'x': 0, 'y': 0, 'z': 0}

# -------------------------------------------------------
# 2. 访问字典元素
# -------------------------------------------------------
print("\n--- 访问元素 ---")
person = {"name": "Alice", "age": 25, "city": "Beijing"}

# 使用键访问
print(person["name"])       # Alice

# get() 方法：不存在时返回默认值（不会抛出异常）
print(person.get("age"))        # 25
print(person.get("email"))      # None
print(person.get("email", "未知"))  # 未知

# -------------------------------------------------------
# 3. 修改字典
# -------------------------------------------------------
print("\n--- 修改字典 ---")
person = {"name": "Alice", "age": 25}

# 修改已有键的值
person["age"] = 26
print(person)

# 添加新键值对
person["email"] = "alice@example.com"
print(person)

# update() 更新多个键值对
person.update({"city": "Shanghai", "age": 27})
print(person)

# -------------------------------------------------------
# 4. 删除字典元素
# -------------------------------------------------------
print("\n--- 删除元素 ---")
d = {"a": 1, "b": 2, "c": 3, "d": 4}

# pop() 删除指定键，并返回其值
val = d.pop("b")
print(f"删除 'b'，值为 {val}，字典：{d}")

# popitem() 删除并返回最后插入的键值对（Python 3.7+）
item = d.popitem()
print(f"删除最后一项 {item}，字典：{d}")

# del 删除指定键
del d["a"]
print(f"del 'a' 后：{d}")

# clear() 清空字典
d.clear()
print(f"clear 后：{d}")

# -------------------------------------------------------
# 5. 字典遍历
# -------------------------------------------------------
print("\n--- 遍历字典 ---")
scores = {"math": 95, "english": 88, "science": 92}

# 遍历键
for key in scores:
    print(key)

# 遍历键（推荐写法）
for key in scores.keys():
    print(key, end=" ")
print()

# 遍历值
for value in scores.values():
    print(value, end=" ")
print()

# 遍历键值对
for key, value in scores.items():
    print(f"{key}: {value}")

# -------------------------------------------------------
# 6. 字典常用方法与函数
# -------------------------------------------------------
print("\n--- 常用方法 ---")
d = {"a": 1, "b": 2, "c": 3}

print(len(d))         # 3（键值对数量）
print(d.keys())       # dict_keys(['a', 'b', 'c'])
print(d.values())     # dict_values([1, 2, 3])
print(d.items())      # dict_items([('a', 1), ('b', 2), ('c', 3)])

# 检查键是否存在
print("a" in d)       # True
print("x" in d)       # False
print("x" not in d)   # True

# 合并字典（Python 3.9+）
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
merged = d1 | d2      # 合并
print(merged)         # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 兼容 Python 3.8 以下的合并方式
merged2 = {**d1, **d2}
print(merged2)

# -------------------------------------------------------
# 7. 嵌套字典
# -------------------------------------------------------
print("\n--- 嵌套字典 ---")
students = {
    "Alice": {"age": 20, "grades": [85, 90, 92]},
    "Bob": {"age": 22, "grades": [78, 88, 80]},
}

print(students["Alice"]["age"])           # 20
print(students["Bob"]["grades"][1])       # 88

# 遍历嵌套字典
for name, info in students.items():
    avg = sum(info["grades"]) / len(info["grades"])
    print(f"{name}：平均分 {avg:.1f}")

# -------------------------------------------------------
# 8. 字典推导式
# -------------------------------------------------------
print("\n--- 字典推导式 ---")
# 从列表创建字典
numbers = [1, 2, 3, 4, 5]
squares = {n: n**2 for n in numbers}
print(squares)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 过滤字典
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Dave": 96}
high_scores = {k: v for k, v in scores.items() if v >= 90}
print(high_scores)    # {'Bob': 92, 'Dave': 96}

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 统计字符串中每个字母出现的次数，用字典存储
# 2. 给定两个列表 keys = ['a', 'b', 'c'] 和 values = [1, 2, 3]，
#    用 zip() 创建字典
# 3. 给定学生成绩字典，计算平均分并找出最高分的学生

print("\n--- 练习参考答案 ---")
# 1. 统计字母频率
text = "hello world"
freq = {}
for char in text:
    if char != " ":
        freq[char] = freq.get(char, 0) + 1
print(freq)

# 2. zip 创建字典
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))
print(d)

# 3. 找最高分学生
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Dave": 96}
avg = sum(grades.values()) / len(grades)
top_student = max(grades, key=grades.get)
print(f"平均分：{avg:.1f}")
print(f"最高分：{top_student}（{grades[top_student]} 分）")
