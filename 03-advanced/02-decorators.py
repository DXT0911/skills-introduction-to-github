# =============================================================
# 第18节：装饰器（Decorators）
# =============================================================
# 装饰器是一种修改函数或类行为的设计模式。
# 它允许在不修改原函数代码的情况下，为函数添加额外功能。
# =============================================================

import time
import functools

# -------------------------------------------------------
# 1. 理解装饰器的原理
# -------------------------------------------------------
print("--- 装饰器原理 ---")

# 首先理解：函数是 Python 的一等公民
def greet(name):
    return f"Hello, {name}!"

# 函数可以作为参数传递
def apply_function(func, value):
    return func(value)

print(apply_function(greet, "Alice"))

# 函数可以作为返回值
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
print(double(5))      # 10

# -------------------------------------------------------
# 2. 手动实现装饰器
# -------------------------------------------------------
print("\n--- 手动实现装饰器 ---")

# 为函数添加计时功能
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时：{end - start:.4f} 秒")
        return result
    return wrapper

def slow_sum(n):
    """计算 1 到 n 的和"""
    total = 0
    for i in range(n + 1):
        total += i
    return total

# 手动装饰
timed_sum = timer(slow_sum)
result = timed_sum(100000)
print(f"结果：{result}")

# -------------------------------------------------------
# 3. 使用 @ 语法糖
# -------------------------------------------------------
print("\n--- @ 语法糖 ---")

@timer
def slow_product(n):
    """计算 1 到 n 的乘积"""
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product

result = slow_product(10)
print(f"结果：{result}")

# -------------------------------------------------------
# 4. 使用 functools.wraps 保留函数信息
# -------------------------------------------------------
print("\n--- functools.wraps ---")

def my_decorator(func):
    @functools.wraps(func)   # 保留原函数的名称、文档字符串等
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__} 之前")
        result = func(*args, **kwargs)
        print(f"调用 {func.__name__} 之后")
        return result
    return wrapper

@my_decorator
def add(a, b):
    """返回 a + b 的和"""
    return a + b

print(add(3, 5))
print(add.__name__)    # add（没有 wraps 的话会是 wrapper）
print(add.__doc__)     # 返回 a + b 的和

# -------------------------------------------------------
# 5. 常用装饰器示例
# -------------------------------------------------------
print("\n--- 常用装饰器示例 ---")

# 1. 日志装饰器
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(str(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"调用 {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回：{result}")
        return result
    return wrapper

@logger
def multiply(x, y):
    return x * y

multiply(3, 5)

# 2. 缓存（记忆化）装饰器
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])

# Python 内置的 lru_cache 更完善
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))    # 非常快，因为有缓存

# 3. 重试装饰器
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        print(f"第 {attempt + 1} 次失败，重试中...")
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

# 演示重试（模拟不稳定的操作）
import random
call_count = [0]

@retry(max_attempts=3, delay=0)   # delay=0 避免等待
def unstable_operation():
    call_count[0] += 1
    if random.random() < 0.7:   # 70% 概率失败
        raise ConnectionError("连接失败")
    return "操作成功"

random.seed(42)
try:
    result = unstable_operation()
    print(f"结果：{result}（尝试了 {call_count[0]} 次）")
except ConnectionError as e:
    print(f"最终失败：{e}（尝试了 {call_count[0]} 次）")

# -------------------------------------------------------
# 6. 带参数的装饰器
# -------------------------------------------------------
print("\n--- 带参数的装饰器 ---")

def repeat(times):
    """装饰器工厂：让函数重复执行指定次数"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Bob")

# -------------------------------------------------------
# 7. 类装饰器
# -------------------------------------------------------
print("\n--- 类装饰器 ---")

class Singleton:
    """单例模式装饰器"""
    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance

@Singleton
class DatabaseConnection:
    def __init__(self, host="localhost"):
        self.host = host
        print(f"创建数据库连接：{host}")

    def query(self, sql):
        return f"执行查询：{sql}"

db1 = DatabaseConnection("server1")
db2 = DatabaseConnection("server2")   # 不会创建新实例

print(db1 is db2)     # True（同一个实例）
print(db1.host)       # server1

# -------------------------------------------------------
# 8. 装饰器堆叠
# -------------------------------------------------------
print("\n--- 装饰器堆叠 ---")

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def uppercase(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@bold
@uppercase
def greet(name):
    return f"hello, {name}"

# 执行顺序：greet -> uppercase -> bold
print(greet("Alice"))   # **HELLO, ALICE**

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写一个 @validate_types 装饰器，检查函数参数类型
# 2. 编写一个 @rate_limit 装饰器，限制函数调用频率
# 3. 使用装饰器实现简单的权限控制系统

print("\n--- 练习参考答案 ---")

# 1. 类型验证装饰器
def validate_types(**type_hints):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取参数名
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, value in bound.arguments.items():
                if name in type_hints and not isinstance(value, type_hints[name]):
                    raise TypeError(
                        f"参数 '{name}' 应为 {type_hints[name].__name__}，"
                        f"得到 {type(value).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(a=int, b=int)
def safe_divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

print(safe_divide(10, 2))     # 5.0
try:
    safe_divide("10", 2)      # TypeError
except TypeError as e:
    print(f"类型错误：{e}")
