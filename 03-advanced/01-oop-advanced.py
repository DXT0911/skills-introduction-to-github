# =============================================================
# 第17节：面向对象高级特性
# =============================================================
# 本节介绍 Python OOP 的高级特性：多重继承、MRO、
# 魔术方法、抽象类、接口模式等。
# =============================================================

# -------------------------------------------------------
# 1. 多重继承
# -------------------------------------------------------
print("--- 多重继承 ---")

class Flyable:
    def fly(self):
        return f"{self.name} 在飞翔"

class Swimmable:
    def swim(self):
        return f"{self.name} 在游泳"

class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name

    def quack(self):
        return f"{self.name}：嘎嘎！"

donald = Duck("唐老鸭")
print(donald.fly())
print(donald.swim())
print(donald.quack())

# -------------------------------------------------------
# 2. 方法解析顺序（MRO）
# -------------------------------------------------------
print("\n--- MRO ---")

class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return "Hello from B"

class C(A):
    def hello(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.hello())          # Hello from B（B 优先于 C）
print(D.__mro__)          # 查看方法解析顺序

# -------------------------------------------------------
# 3. 魔术方法（Dunder Methods）
# -------------------------------------------------------
print("\n--- 魔术方法 ---")

class Vector:
    """二维向量类，演示各种魔术方法"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __bool__(self):
        return bool(self.x or self.y)

    def __len__(self):
        return 2    # 向量有两个分量

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("向量索引只有 0 或 1")

    def __iter__(self):
        yield self.x
        yield self.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)       # Vector(4, 6)
print(v2 - v1)       # Vector(2, 2)
print(v1 * 3)        # Vector(3, 6)
print(3 * v1)        # Vector(3, 6)（__rmul__）
print(v1 == Vector(1, 2))   # True
print(abs(v2))        # 5.0
print(len(v1))        # 2
print(v1[0], v1[1])   # 1 2
print(list(v1))        # [1, 2]（__iter__）

# -------------------------------------------------------
# 4. 比较魔术方法
# -------------------------------------------------------
print("\n--- 比较方法 ---")
from functools import total_ordering

@total_ordering
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        return self.celsius == other.celsius

    def __lt__(self, other):
        return self.celsius < other.celsius

    def __str__(self):
        return f"{self.celsius}°C"

# @total_ordering 自动生成其他比较方法
temps = [Temperature(30), Temperature(20), Temperature(25)]
print(sorted(temps))           # 需要 __str__ 的列表
print(min(temps))
print(max(temps))
print(Temperature(20) <= Temperature(25))  # True

# -------------------------------------------------------
# 5. 抽象基类（ABC）
# -------------------------------------------------------
print("\n--- 抽象基类 ---")
from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象形状类，不能直接实例化"""

    @abstractmethod
    def area(self) -> float:
        """子类必须实现计算面积的方法"""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """子类必须实现计算周长的方法"""
        pass

    def describe(self):
        return (f"{type(self).__name__}："
                f"面积={self.area():.2f}，周长={self.perimeter():.2f}")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# try:
#     s = Shape()  # TypeError: 不能实例化抽象类
# except TypeError as e:
#     print(f"错误：{e}")

shapes = [Circle(5), Rectangle(4, 6)]
for s in shapes:
    print(s.describe())

# -------------------------------------------------------
# 6. Mixin 类
# -------------------------------------------------------
print("\n--- Mixin 模式 ---")

class JsonMixin:
    """提供 JSON 序列化能力的 Mixin"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj

class LogMixin:
    """提供日志能力的 Mixin"""
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")

class User(JsonMixin, LogMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

user = User("Alice", "alice@example.com")
json_str = user.to_json()
print(json_str)

user2 = User.from_json(json_str)
print(user2.name, user2.email)
user2.log("用户登录成功")

# -------------------------------------------------------
# 7. __slots__
# -------------------------------------------------------
print("\n--- __slots__ ---")

class Point:
    """使用 __slots__ 节省内存，限制可用属性"""
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x, p.y)

# 不能添加未声明的属性
try:
    p.z = 3    # AttributeError
except AttributeError as e:
    print(f"错误：{e}")

# 内存比较
import sys
class NormalPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

normal_p = NormalPoint(1, 2)
slots_p = Point(1, 2)
print(f"普通类实例大小：{sys.getsizeof(normal_p.__dict__)} 字节")

# -------------------------------------------------------
# 8. 数据类（dataclasses）- Python 3.7+
# -------------------------------------------------------
print("\n--- 数据类 ---")
from dataclasses import dataclass, field

@dataclass
class Product:
    """使用 @dataclass 自动生成 __init__, __repr__, __eq__"""
    name: str
    price: float
    quantity: int = 0
    tags: list = field(default_factory=list)

    def total_value(self):
        return self.price * self.quantity

# 自动生成的方法
p1 = Product("Python书", 59.9, 10)
p2 = Product("Python书", 59.9, 10)
p3 = Product("笔记本", 15.0, 100, tags=["文具"])

print(p1)
print(p1 == p2)        # True（自动生成 __eq__）
print(p3.total_value())

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 实现一个 Stack 类，使用魔术方法让它支持 len()、in 操作和 for 循环
# 2. 用 ABC 定义 Animal 抽象类，要求子类实现 speak() 和 move()
# 3. 用 @dataclass 创建表示扑克牌的类

print("\n--- 练习参考答案 ---")
# 1. Stack 类
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[-1] if self._data else None

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(reversed(self._data))

    def __str__(self):
        return f"Stack({self._data})"

stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"长度：{len(stack)}")
print(f"2 在栈中：{2 in stack}")
print(f"栈内容（从顶到底）：{list(stack)}")
print(f"弹出：{stack.pop()}")
