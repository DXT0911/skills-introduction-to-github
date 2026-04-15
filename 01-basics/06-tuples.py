# =============================================================
# 第6节：元组（Tuple）
# =============================================================
# 元组与列表类似，但元组是不可变的（immutable）。
# 一旦创建就不能修改，适合存储不应被修改的数据。
# =============================================================

# -------------------------------------------------------
# 1. 创建元组
# -------------------------------------------------------
print("--- 创建元组 ---")
empty_tuple = ()                    # 空元组
single = (42,)                      # 单元素元组（注意逗号！）
single_wrong = (42)                 # 这不是元组，只是括号
numbers = (1, 2, 3, 4, 5)
mixed = (1, "hello", 3.14, True)
nested = ((1, 2), (3, 4), (5, 6))

print(type(single))         # <class 'tuple'>
print(type(single_wrong))   # <class 'int'>（不是元组！）
print(numbers)
print(mixed)

# 也可以省略括号
coords = 10, 20, 30         # 等同于 (10, 20, 30)
print(coords, type(coords)) # (10, 20, 30) <class 'tuple'>

# -------------------------------------------------------
# 2. 访问元组元素
# -------------------------------------------------------
print("\n--- 访问元素 ---")
colors = ("red", "green", "blue", "yellow")

print(colors[0])      # red
print(colors[-1])     # yellow
print(colors[1:3])    # ('green', 'blue')
print(colors[::-1])   # 反转

# 嵌套元组
point_3d = ((1, 2), (3, 4))
print(point_3d[0][1])  # 2

# -------------------------------------------------------
# 3. 元组的不可变性
# -------------------------------------------------------
print("\n--- 不可变性 ---")
t = (1, 2, 3)

# 以下操作会报错（取消注释后会抛出 TypeError）：
# t[0] = 10         # TypeError: 'tuple' object does not support item assignment
# t.append(4)       # AttributeError: 'tuple' object has no attribute 'append'

print("元组内容不可修改")

# 但如果元组内部包含可变对象，该可变对象可以修改
t2 = ([1, 2], [3, 4])
t2[0].append(99)        # 列表本身可修改
print(t2)               # ([1, 2, 99], [3, 4])

# -------------------------------------------------------
# 4. 元组方法
# -------------------------------------------------------
print("\n--- 元组方法 ---")
t = (1, 2, 3, 2, 4, 2, 5)

print(t.count(2))    # 3（2 出现的次数）
print(t.index(3))    # 2（第一个 3 的索引）
print(len(t))        # 7
print(min(t))        # 1
print(max(t))        # 5
print(sum(t))        # 19

# -------------------------------------------------------
# 5. 元组解包（拆包）
# -------------------------------------------------------
print("\n--- 元组解包 ---")
point = (3, 7)
x, y = point
print(f"x={x}, y={y}")    # x=3, y=7

person = ("Alice", 25, "Engineer")
name, age, job = person
print(f"{name} 今年 {age} 岁，是一名 {job}")

# 使用 * 收集剩余元素
first, *rest = (1, 2, 3, 4, 5)
print(first)    # 1
print(rest)     # [2, 3, 4, 5]

*start, last = (1, 2, 3, 4, 5)
print(start)    # [1, 2, 3, 4]
print(last)     # 5

first, *middle, last = (1, 2, 3, 4, 5)
print(first, middle, last)    # 1 [2, 3, 4] 5

# 函数返回多个值时，其实是返回元组
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([3, 1, 4, 1, 5, 9])
print(f"最小值：{minimum}，最大值：{maximum}")

# -------------------------------------------------------
# 6. 元组与列表的对比
# -------------------------------------------------------
print("\n--- 元组 vs 列表 ---")
import sys

lst = [1, 2, 3, 4, 5]
tpl = (1, 2, 3, 4, 5)

# 内存占用：元组更小
print(f"列表大小：{sys.getsizeof(lst)} 字节")
print(f"元组大小：{sys.getsizeof(tpl)} 字节")

# 元组可以作为字典的键（因为可哈希），列表不行
d = {(1, 2): "坐标", (3, 4): "另一坐标"}
print(d[(1, 2)])   # 坐标

# 何时用元组：
# - 存储不应被修改的数据（如坐标、配置）
# - 函数返回多个值
# - 作为字典的键

# -------------------------------------------------------
# 7. 元组转换
# -------------------------------------------------------
print("\n--- 类型转换 ---")
lst = [1, 2, 3]
tpl = tuple(lst)       # 列表转元组
print(tpl)

back_to_list = list(tpl)  # 元组转列表
print(back_to_list)

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 创建一个包含你的姓名、年龄、身高的元组，并解包
# 2. 给定元组 (10, 20, 30, 40, 50)，计算平均值
# 3. 写一个函数，返回两个数的商和余数（作为元组）

print("\n--- 练习参考答案 ---")
# 1. 解包
info = ("小明", 20, 1.75)
name, age, height = info
print(f"姓名：{name}，年龄：{age}，身高：{height}")

# 2. 平均值
nums = (10, 20, 30, 40, 50)
average = sum(nums) / len(nums)
print(f"平均值：{average}")

# 3. 商和余数
def divide(a, b):
    return a // b, a % b

quotient, remainder = divide(17, 5)
print(f"17 ÷ 5 = {quotient} 余 {remainder}")
