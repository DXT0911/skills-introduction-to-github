# =============================================================
# 第8节：集合（Set）
# =============================================================
# 集合是无序、不重复元素的集合。
# 适合用于去重、成员检测和集合运算（并集、交集、差集）。
# =============================================================

# -------------------------------------------------------
# 1. 创建集合
# -------------------------------------------------------
print("--- 创建集合 ---")
empty_set = set()               # 注意：{} 创建的是空字典，不是集合！
numbers = {1, 2, 3, 4, 5}
fruits = {"apple", "banana", "cherry"}
with_dups = {1, 2, 2, 3, 3, 3}  # 自动去重

print(empty_set)       # set()
print(numbers)
print(with_dups)       # {1, 2, 3}（重复元素被去除）

# 从列表/字符串创建集合
from_list = set([1, 2, 2, 3, 3])
from_str = set("hello")         # {'h', 'e', 'l', 'o'}（自动去重 'l'）
print(from_list)
print(from_str)

# -------------------------------------------------------
# 2. 集合的无序性
# -------------------------------------------------------
print("\n--- 无序性 ---")
s = {3, 1, 4, 1, 5, 9, 2, 6}
print(s)               # 输出顺序可能不同！集合是无序的
print(len(s))          # 7（去重后的元素个数）

# 集合不支持索引
# print(s[0])  # TypeError: 'set' object is not subscriptable

# -------------------------------------------------------
# 3. 集合常用操作
# -------------------------------------------------------
print("\n--- 集合操作 ---")
s = {1, 2, 3, 4}

# 添加元素
s.add(5)
print("add:", s)

s.update([6, 7, 8])     # 添加多个元素
print("update:", s)

# 删除元素
s.remove(8)              # 删除，不存在则报错
print("remove:", s)

s.discard(99)            # 删除，不存在也不报错
print("discard:", s)

popped = s.pop()         # 随机删除一个元素
print("pop:", s, "弹出:", popped)

s.clear()                # 清空集合
print("clear:", s)

# -------------------------------------------------------
# 4. 集合运算
# -------------------------------------------------------
print("\n--- 集合运算 ---")
A = {1, 2, 3, 4, 5}
B = {3, 4, 5, 6, 7}

# 并集（A 和 B 中所有元素）
print("并集:", A | B)             # {1, 2, 3, 4, 5, 6, 7}
print("并集:", A.union(B))

# 交集（A 和 B 共同的元素）
print("交集:", A & B)             # {3, 4, 5}
print("交集:", A.intersection(B))

# 差集（在 A 中但不在 B 中）
print("差集 A-B:", A - B)         # {1, 2}
print("差集 A-B:", A.difference(B))

print("差集 B-A:", B - A)         # {6, 7}

# 对称差集（在 A 或 B 中，但不在两者共同部分）
print("对称差集:", A ^ B)          # {1, 2, 6, 7}
print("对称差集:", A.symmetric_difference(B))

# -------------------------------------------------------
# 5. 集合关系判断
# -------------------------------------------------------
print("\n--- 集合关系 ---")
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}
C = {4, 5, 6}

# 子集
print(A.issubset(B))          # True（A 是 B 的子集）
print(A <= B)                 # True

# 超集
print(B.issuperset(A))        # True（B 是 A 的超集）
print(B >= A)                 # True

# 是否有交集
print(A.isdisjoint(C))        # True（A 和 C 没有共同元素）
print(A.isdisjoint(B))        # False（A 和 B 有共同元素）

# 成员检测（集合比列表快！）
print(3 in A)       # True
print(6 in A)       # False

# -------------------------------------------------------
# 6. 冻结集合（frozenset）
# -------------------------------------------------------
print("\n--- frozenset ---")
# frozenset 是不可变集合，可以作为字典的键或集合的元素
fs = frozenset([1, 2, 3, 4])
print(fs)

# 不能修改 frozenset
# fs.add(5)  # AttributeError

# 可以作为字典键
d = {frozenset([1, 2]): "坐标一", frozenset([3, 4]): "坐标二"}
print(d)

# -------------------------------------------------------
# 7. 实用案例：列表去重
# -------------------------------------------------------
print("\n--- 实用：去重 ---")
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# 方法1：转为集合（不保证顺序）
unique_unordered = list(set(data))
print("去重（不保证顺序）:", sorted(unique_unordered))

# 方法2：保持顺序的去重
seen = set()
unique_ordered = []
for item in data:
    if item not in seen:
        seen.add(item)
        unique_ordered.append(item)
print("去重（保持顺序）:", unique_ordered)

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 给定两个班级的学生名单，找出同时在两个班的学生
# 2. 统计一段文字中有多少个不同的单词
# 3. 给定列表，用集合判断是否有重复元素

print("\n--- 练习参考答案 ---")
# 1. 两个班共同的学生
class_a = {"Alice", "Bob", "Charlie", "Dave"}
class_b = {"Bob", "Eve", "Charlie", "Frank"}
common = class_a & class_b
print("共同学生:", common)

# 2. 不同单词数
text = "the quick brown fox jumps over the lazy dog"
words = text.split()
unique_words = set(words)
print(f"共 {len(words)} 个单词，{len(unique_words)} 个不重复")

# 3. 是否有重复元素
def has_duplicates(lst):
    return len(lst) != len(set(lst))

print(has_duplicates([1, 2, 3, 4]))      # False
print(has_duplicates([1, 2, 2, 3]))      # True
