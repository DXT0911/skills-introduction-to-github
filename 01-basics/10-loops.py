# =============================================================
# 第10节：循环语句（for / while）
# =============================================================
# 循环用于重复执行一段代码，Python 有 for 和 while 两种循环。
# =============================================================

# -------------------------------------------------------
# 1. for 循环 - 遍历序列
# -------------------------------------------------------
print("--- for 循环基础 ---")

# 遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 遍历字符串
for char in "Python":
    print(char, end=" ")
print()

# 遍历字典
person = {"name": "Alice", "age": 25, "city": "Beijing"}
for key in person:          # 默认遍历键
    print(key)

for key, value in person.items():   # 遍历键值对
    print(f"{key}: {value}")

# -------------------------------------------------------
# 2. range() 函数
# -------------------------------------------------------
print("\n--- range() 函数 ---")
# range(stop)
for i in range(5):
    print(i, end=" ")     # 0 1 2 3 4
print()

# range(start, stop)
for i in range(1, 6):
    print(i, end=" ")     # 1 2 3 4 5
print()

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")     # 0 2 4 6 8
print()

# 倒序
for i in range(10, 0, -1):
    print(i, end=" ")     # 10 9 8 7 6 5 4 3 2 1
print()

# -------------------------------------------------------
# 3. enumerate() - 带索引的遍历
# -------------------------------------------------------
print("\n--- enumerate() ---")
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# 从指定索引开始
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# -------------------------------------------------------
# 4. zip() - 同时遍历多个序列
# -------------------------------------------------------
print("\n--- zip() ---")
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["Beijing", "Shanghai", "Guangzhou"]

for name, age, city in zip(names, ages, cities):
    print(f"{name} 今年 {age} 岁，住在 {city}")

# -------------------------------------------------------
# 5. while 循环
# -------------------------------------------------------
print("\n--- while 循环 ---")

# 基本用法
count = 0
while count < 5:
    print(count, end=" ")
    count += 1
print()

# 用 while 读取用户输入（模拟）
# 实际场景会用 input()，这里用列表模拟
inputs = ["exit", "hello", "exit"]
idx = 0
while inputs[idx] != "exit":
    print(f"处理输入：{inputs[idx]}")
    idx += 1
print("退出循环")

# -------------------------------------------------------
# 6. break - 跳出循环
# -------------------------------------------------------
print("\n--- break ---")
# 找到第一个满足条件的元素
numbers = [2, 4, 6, 7, 10, 12]
for n in numbers:
    if n % 2 != 0:
        print(f"找到第一个奇数：{n}")
        break

# while 循环中的 break
n = 0
while True:             # 无限循环
    n += 1
    if n > 5:
        break
print(f"n = {n}")

# -------------------------------------------------------
# 7. continue - 跳过当前迭代
# -------------------------------------------------------
print("\n--- continue ---")
# 跳过偶数，只打印奇数
for i in range(10):
    if i % 2 == 0:
        continue
    print(i, end=" ")
print()

# -------------------------------------------------------
# 8. for...else 和 while...else
# -------------------------------------------------------
print("\n--- 循环 else ---")
# else 子句在循环正常完成时执行（没有被 break 中断）

# 搜索目标元素
target = 5
for n in [1, 2, 3, 4]:
    if n == target:
        print(f"找到 {target}")
        break
else:
    print(f"未找到 {target}")    # 会输出这行

target = 3
for n in [1, 2, 3, 4]:
    if n == target:
        print(f"找到 {target}")
        break
else:
    print(f"未找到 {target}")    # 不会输出（break 阻止了 else）

# -------------------------------------------------------
# 9. 嵌套循环
# -------------------------------------------------------
print("\n--- 嵌套循环 ---")
# 九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j:2}", end="  ")
    print()

# -------------------------------------------------------
# 10. 列表推导式（简化 for 循环）
# -------------------------------------------------------
print("\n--- 列表推导式 ---")
# 普通写法
squares = []
for n in range(1, 6):
    squares.append(n ** 2)
print(squares)

# 推导式写法（更简洁）
squares = [n ** 2 for n in range(1, 6)]
print(squares)

# 带条件的推导式
even_squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]
print(even_squares)     # [4, 16, 36, 64, 100]

# -------------------------------------------------------
# 11. 实用案例：查找与统计
# -------------------------------------------------------
print("\n--- 案例：统计 ---")
grades = [85, 92, 78, 95, 60, 73, 88, 55, 99, 70]

# 统计各等级人数
counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
for g in grades:
    if g >= 90:
        counts["A"] += 1
    elif g >= 80:
        counts["B"] += 1
    elif g >= 70:
        counts["C"] += 1
    elif g >= 60:
        counts["D"] += 1
    else:
        counts["F"] += 1

for grade, count in counts.items():
    print(f"等级 {grade}：{count} 人")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 用 for 循环计算 1 到 100 的所有整数之和
# 2. 用 while 循环找出第一个大于 1000 的 2 的幂次方
# 3. 打印所有 100 以内的素数（质数）

print("\n--- 练习参考答案 ---")
# 1. 1 到 100 的和
total = sum(range(1, 101))
print(f"1+2+...+100 = {total}")

# 2. 第一个大于 1000 的 2 的幂次方
n = 1
while n <= 1000:
    n *= 2
print(f"第一个大于 1000 的 2 的幂次方：{n}")

# 3. 100 以内的素数
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [n for n in range(2, 101) if is_prime(n)]
print(f"100 以内的素数：{primes}")
