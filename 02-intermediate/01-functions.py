# =============================================================
# 第11节：函数（Functions）
# =============================================================
# 函数是一段可复用的代码块。使用函数可以避免重复代码，
# 让程序更加模块化和易维护。
# =============================================================

# -------------------------------------------------------
# 1. 定义和调用函数
# -------------------------------------------------------
print("--- 基本函数 ---")

def greet():
    """打印问候语（这是函数的文档字符串）"""
    print("Hello, World!")

greet()           # 调用函数

# 带返回值的函数
def add(a, b):
    return a + b

result = add(3, 5)
print(result)     # 8

# -------------------------------------------------------
# 2. 函数参数
# -------------------------------------------------------
print("\n--- 函数参数 ---")

# 位置参数
def describe_person(name, age, city):
    print(f"{name} 今年 {age} 岁，住在 {city}")

describe_person("Alice", 25, "Beijing")

# 关键字参数（可以不按顺序）
describe_person(age=30, city="Shanghai", name="Bob")

# 默认参数
def greet_person(name, greeting="你好"):
    print(f"{greeting}, {name}!")

greet_person("Alice")             # 你好, Alice!
greet_person("Bob", "嗨")        # 嗨, Bob!

# 注意：默认参数必须在非默认参数之后
# def func(a=1, b):  # 这会报错

# -------------------------------------------------------
# 3. 可变参数
# -------------------------------------------------------
print("\n--- 可变参数 ---")

# *args - 接收任意数量的位置参数（元组）
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))           # 6
print(sum_all(1, 2, 3, 4, 5))    # 15

# **kwargs - 接收任意数量的关键字参数（字典）
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Beijing")

# 组合使用
def mixed_func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

mixed_func(1, 2, 3, 4, 5, name="test", value=99)

# 解包参数
def add(x, y, z):
    return x + y + z

nums = [1, 2, 3]
print(add(*nums))           # 解包列表为位置参数

config = {"x": 10, "y": 20, "z": 30}
print(add(**config))        # 解包字典为关键字参数

# -------------------------------------------------------
# 4. 返回值
# -------------------------------------------------------
print("\n--- 返回值 ---")

# 返回多个值（实际上是返回元组）
def min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = min_max([3, 1, 4, 1, 5, 9])
print(f"最小：{minimum}，最大：{maximum}")

# 返回 None（没有 return 语句时）
def no_return():
    x = 1 + 1

result = no_return()
print(result)     # None

# -------------------------------------------------------
# 5. 作用域（Scope）
# -------------------------------------------------------
print("\n--- 作用域 ---")

x = 10    # 全局变量

def func():
    y = 20    # 局部变量
    print(x)  # 可以读取全局变量
    print(y)

func()
# print(y)  # 错误！y 在函数外不可访问

# global 关键字 - 修改全局变量
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)    # 2

# nonlocal 关键字 - 修改外层（非全局）变量
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
    inner()
    inner()
    return count

print(outer())    # 2

# -------------------------------------------------------
# 6. Lambda 函数（匿名函数）
# -------------------------------------------------------
print("\n--- Lambda 函数 ---")

# 普通函数
def square(x):
    return x ** 2

# 等价的 lambda 函数
square_lambda = lambda x: x ** 2

print(square(5))        # 25
print(square_lambda(5)) # 25

# lambda 常用于排序
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda s: s[1])   # 按成绩排序
print(students)

# 配合 map() 和 filter() 使用
numbers = [1, 2, 3, 4, 5, 6]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)           # [2, 4, 6, 8, 10, 12]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)             # [2, 4, 6]

# -------------------------------------------------------
# 7. 内置高阶函数
# -------------------------------------------------------
print("\n--- 高阶函数 ---")
from functools import reduce

nums = [1, 2, 3, 4, 5]

# map() - 映射
squares = list(map(lambda x: x**2, nums))
print("map:", squares)

# filter() - 过滤
odds = list(filter(lambda x: x % 2 != 0, nums))
print("filter:", odds)

# reduce() - 归约
product = reduce(lambda x, y: x * y, nums)
print("reduce:", product)   # 1*2*3*4*5 = 120

# sorted() 与 key 参数
words = ["banana", "apple", "Cherry", "date"]
# 忽略大小写排序
sorted_words = sorted(words, key=str.lower)
print("sorted:", sorted_words)

# -------------------------------------------------------
# 8. 递归函数
# -------------------------------------------------------
print("\n--- 递归函数 ---")

# 阶乘
def factorial(n):
    if n <= 1:         # 基本情况（递归终止条件）
        return 1
    return n * factorial(n - 1)  # 递归调用

print(factorial(5))   # 120
print(factorial(10))  # 3628800

# 斐波那契数列
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fib_sequence = [fibonacci(i) for i in range(10)]
print(fib_sequence)   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# -------------------------------------------------------
# 9. 函数文档字符串与类型注解
# -------------------------------------------------------
print("\n--- 文档字符串与类型注解 ---")

def calculate_bmi(weight: float, height: float) -> str:
    """
    根据体重和身高计算 BMI 值并返回健康评估。

    参数：
        weight (float): 体重（千克）
        height (float): 身高（米）

    返回：
        str: BMI 评估结果字符串
    """
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        status = "偏轻"
    elif bmi < 25:
        status = "正常"
    elif bmi < 30:
        status = "超重"
    else:
        status = "肥胖"
    return f"BMI={bmi:.1f}，{status}"

print(calculate_bmi(70, 1.75))
print(calculate_bmi.__doc__)    # 打印文档字符串

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写一个函数，接收一个列表和一个目标值，
#    返回目标值在列表中的所有索引
# 2. 编写一个递归函数计算二进制数到十进制数
# 3. 用 lambda 和 sorted() 对字典列表按多个字段排序

print("\n--- 练习参考答案 ---")
# 1. 查找所有索引
def find_all_indices(lst, target):
    return [i for i, x in enumerate(lst) if x == target]

print(find_all_indices([1, 2, 3, 2, 4, 2], 2))   # [1, 3, 5]

# 2. 二进制转十进制
def binary_to_decimal(binary_str):
    if not binary_str:
        return 0
    return int(binary_str[-1]) + 2 * binary_to_decimal(binary_str[:-1])

print(binary_to_decimal("1010"))   # 10

# 3. 多字段排序
students = [
    {"name": "Alice", "age": 25, "score": 85},
    {"name": "Bob", "age": 25, "score": 90},
    {"name": "Charlie", "age": 22, "score": 85},
]
sorted_students = sorted(students, key=lambda s: (-s["score"], s["age"]))
for s in sorted_students:
    print(s)
