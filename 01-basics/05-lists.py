# =============================================================
# 第5节：列表（List）
# =============================================================
# 列表是 Python 中最常用的数据结构，用于存储有序的元素集合。
# 列表是可变的（mutable），支持增删改查。
# =============================================================

# -------------------------------------------------------
# 1. 创建列表
# -------------------------------------------------------
print("--- 创建列表 ---")
empty_list = []                        # 空列表
numbers = [1, 2, 3, 4, 5]             # 整数列表
fruits = ["apple", "banana", "cherry"] # 字符串列表
mixed = [1, "hello", 3.14, True, None] # 混合类型列表
nested = [[1, 2], [3, 4], [5, 6]]     # 嵌套列表

print(numbers)
print(fruits)
print(mixed)
print(nested)

# 用 list() 创建列表
from_range = list(range(1, 6))    # [1, 2, 3, 4, 5]
from_str = list("hello")          # ['h', 'e', 'l', 'l', 'o']
print(from_range)
print(from_str)

# -------------------------------------------------------
# 2. 访问元素（索引与切片）
# -------------------------------------------------------
print("\n--- 索引与切片 ---")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(fruits[0])      # apple（第一个）
print(fruits[-1])     # elderberry（最后一个）
print(fruits[1:3])    # ['banana', 'cherry']
print(fruits[:3])     # ['apple', 'banana', 'cherry']
print(fruits[2:])     # ['cherry', 'date', 'elderberry']
print(fruits[::2])    # ['apple', 'cherry', 'elderberry']
print(fruits[::-1])   # 反转列表

# 嵌套列表访问
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2])   # 6（第2行第3列）

# -------------------------------------------------------
# 3. 修改列表
# -------------------------------------------------------
print("\n--- 修改列表 ---")
fruits = ["apple", "banana", "cherry"]

# 修改单个元素
fruits[1] = "blueberry"
print(fruits)    # ['apple', 'blueberry', 'cherry']

# 修改切片
fruits[1:3] = ["blackberry", "coconut"]
print(fruits)    # ['apple', 'blackberry', 'coconut']

# -------------------------------------------------------
# 4. 列表常用方法
# -------------------------------------------------------
print("\n--- 常用方法 ---")
lst = [3, 1, 4, 1, 5, 9, 2, 6]

# 添加元素
lst.append(5)            # 在末尾添加
print("append:", lst)

lst.insert(2, 99)        # 在指定位置插入
print("insert:", lst)

lst.extend([7, 8])       # 添加另一个列表的所有元素
print("extend:", lst)

# 删除元素
lst.remove(99)           # 删除第一个值为 99 的元素
print("remove:", lst)

popped = lst.pop()       # 删除并返回最后一个元素
print("pop:", lst, "弹出:", popped)

popped = lst.pop(0)      # 删除并返回指定索引的元素
print("pop(0):", lst, "弹出:", popped)

del lst[0]               # 用 del 删除指定索引的元素
print("del:", lst)

# 查找
numbers = [1, 2, 3, 2, 4, 2]
print(numbers.index(2))   # 1（第一个 2 的索引）
print(numbers.count(2))   # 3（2 出现的次数）

# 排序
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()               # 原地升序排序
print("sort:", nums)

nums.sort(reverse=True)   # 原地降序排序
print("sort desc:", nums)

words = ["banana", "apple", "cherry"]
words.sort(key=len)       # 按字符串长度排序
print("sort by len:", words)

# sorted() 返回新列表，不修改原列表
original = [3, 1, 4, 1, 5]
sorted_lst = sorted(original)
print("sorted:", sorted_lst, "original:", original)

# 翻转
lst = [1, 2, 3, 4, 5]
lst.reverse()
print("reverse:", lst)

# 清空
lst.clear()
print("clear:", lst)    # []

# -------------------------------------------------------
# 5. 列表统计函数
# -------------------------------------------------------
print("\n--- 统计函数 ---")
nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(len(nums))        # 长度：8
print(sum(nums))        # 求和：31
print(min(nums))        # 最小值：1
print(max(nums))        # 最大值：9

# -------------------------------------------------------
# 6. 列表拷贝
# -------------------------------------------------------
print("\n--- 列表拷贝 ---")
original = [1, 2, 3]

# 浅拷贝
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

# 注意：直接赋值不是拷贝，而是引用
ref = original
ref.append(4)
print("original:", original)   # [1, 2, 3, 4]（original 也被修改了！）

copy1.append(99)
print("copy1:", copy1)         # [1, 2, 3, 99]
print("original:", original)   # 不受影响

# -------------------------------------------------------
# 7. 列表与循环
# -------------------------------------------------------
print("\n--- 列表与循环 ---")
fruits = ["apple", "banana", "cherry"]

# 基本遍历
for fruit in fruits:
    print(fruit)

# 带索引遍历
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 创建一个包含 1-10 所有奇数的列表
# 2. 给定列表 [5, 2, 8, 1, 9, 3]，找出最大值和最小值，并排序
# 3. 从列表中删除所有重复元素（提示：可以用 set）

print("\n--- 练习参考答案 ---")
# 1. 奇数列表
odd_numbers = list(range(1, 11, 2))
print("奇数:", odd_numbers)

# 2. 排序
nums = [5, 2, 8, 1, 9, 3]
print("最大值:", max(nums), "最小值:", min(nums))
print("升序:", sorted(nums))

# 3. 去重
lst = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(lst))
print("去重:", sorted(unique))
