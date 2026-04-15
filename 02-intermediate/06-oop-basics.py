# =============================================================
# 第16节：面向对象编程基础（OOP Basics）
# =============================================================
# 面向对象编程（OOP）是一种通过"类"和"对象"组织代码的方法。
# 核心概念：封装、继承、多态
# =============================================================

# -------------------------------------------------------
# 1. 类和对象
# -------------------------------------------------------
print("--- 类和对象 ---")

# 定义一个简单的类
class Dog:
    """表示一只狗的类"""

    # 类属性（所有实例共享）
    species = "Canis familiaris"

    # __init__ 是构造方法，创建对象时自动调用
    def __init__(self, name, age):
        # 实例属性（每个对象独有）
        self.name = name
        self.age = age

    # 实例方法（第一个参数是 self，指代当前对象）
    def bark(self):
        return f"{self.name} 汪汪叫！"

    def describe(self):
        return f"{self.name}，{self.age} 岁，{self.species}"

# 创建对象（实例化）
dog1 = Dog("旺财", 3)
dog2 = Dog("小白", 5)

# 访问属性
print(dog1.name)          # 旺财
print(dog2.age)           # 5
print(Dog.species)         # 类属性（通过类名访问）
print(dog1.species)        # 也可以通过实例访问

# 调用方法
print(dog1.bark())
print(dog2.describe())

# 修改属性
dog1.age = 4
print(dog1.age)           # 4

# -------------------------------------------------------
# 2. __str__ 和 __repr__
# -------------------------------------------------------
print("\n--- __str__ 和 __repr__ ---")

class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        """用户友好的字符串表示（用于 print）"""
        return f"《{self.title}》 by {self.author}（¥{self.price}）"

    def __repr__(self):
        """开发者调试用的字符串表示"""
        return f"Book(title={self.title!r}, author={self.author!r}, price={self.price})"

book = Book("Python 从入门到精通", "小明", 59.9)
print(book)         # 调用 __str__
print(repr(book))   # 调用 __repr__

# -------------------------------------------------------
# 3. 继承
# -------------------------------------------------------
print("\n--- 继承 ---")

# 基类（父类）
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} 说：{self.sound}"

    def __str__(self):
        return f"动物：{self.name}"

# 派生类（子类）继承 Animal
class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "喵喵")  # 调用父类的 __init__
        self.is_domestic = True

    def purr(self):
        return f"{self.name} 咕噜咕噜..."

class Duck(Animal):
    def __init__(self, name):
        super().__init__(name, "嘎嘎")

    def swim(self):
        return f"{self.name} 在游泳"

# 使用子类
cat = Cat("咪咪")
duck = Duck("唐老鸭")

print(cat.speak())       # 继承的方法
print(cat.purr())        # 子类特有的方法
print(duck.speak())
print(duck.swim())

print(isinstance(cat, Cat))     # True
print(isinstance(cat, Animal))  # True（is-a 关系）

# -------------------------------------------------------
# 4. 方法重写（多态）
# -------------------------------------------------------
print("\n--- 方法重写与多态 ---")

class Shape:
    def area(self):
        raise NotImplementedError("子类必须实现 area() 方法")

    def describe(self):
        return f"这是一个 {type(self).__name__}，面积是 {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

# 多态：同一接口，不同实现
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
for shape in shapes:
    print(shape.describe())   # 调用同名方法，但行为不同

# -------------------------------------------------------
# 5. 类方法和静态方法
# -------------------------------------------------------
print("\n--- 类方法和静态方法 ---")

class Person:
    count = 0    # 类变量，统计创建的对象数量

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.count += 1

    def introduce(self):
        """实例方法"""
        return f"我叫 {self.name}，今年 {self.age} 岁"

    @classmethod
    def get_count(cls):
        """类方法：第一个参数是 cls（类本身），而不是 self"""
        return f"已创建 {cls.count} 个 Person 对象"

    @classmethod
    def from_birth_year(cls, name, birth_year):
        """工厂方法：从出生年份创建对象"""
        from datetime import date
        age = date.today().year - birth_year
        return cls(name, age)

    @staticmethod
    def is_adult(age):
        """静态方法：与类和实例都无关，只是逻辑上属于这个类"""
        return age >= 18

p1 = Person("Alice", 25)
p2 = Person("Bob", 17)
p3 = Person.from_birth_year("Charlie", 2000)

print(p1.introduce())
print(Person.get_count())          # 通过类名调用
print(Person.is_adult(20))         # True
print(Person.is_adult(16))         # False

# -------------------------------------------------------
# 6. 访问控制（封装）
# -------------------------------------------------------
print("\n--- 访问控制 ---")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner             # 公有属性
        self._account_id = "A001"      # 受保护属性（约定，仍可访问）
        self.__balance = balance        # 私有属性（名称改写）

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于零")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于零")
        if amount > self.__balance:
            raise ValueError("余额不足")
        self.__balance -= amount
        return self.__balance

    def get_balance(self):
        return self.__balance

    def __str__(self):
        return f"账户：{self.owner}，余额：¥{self.__balance:.2f}"

account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)
print(account)
print(account.get_balance())    # 通过公有方法访问私有属性

# -------------------------------------------------------
# 7. 属性（property）
# -------------------------------------------------------
print("\n--- property 装饰器 ---")

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """获取摄氏度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏度（带验证）"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度（-273.15°C）")
        self._celsius = value

    @property
    def fahrenheit(self):
        """获取华氏度（只读）"""
        return self._celsius * 9 / 5 + 32

temp = Temperature(25)
print(f"摄氏度：{temp.celsius}°C")
print(f"华氏度：{temp.fahrenheit}°F")

temp.celsius = 100
print(f"沸点：{temp.celsius}°C = {temp.fahrenheit}°F")

try:
    temp.celsius = -300   # 会触发验证
except ValueError as e:
    print(f"错误：{e}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 创建一个 Student 类，包含姓名、学号、成绩列表，
#    添加方法计算平均分，并定义 __str__ 方法
# 2. 创建 Vehicle 父类和 Car/Motorcycle 子类，
#    实现 start() 和 stop() 方法
# 3. 为 BankAccount 类添加交易历史记录功能

print("\n--- 练习参考答案 ---")
# 1. Student 类
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return (f"学生：{self.name}（{self.student_id}），"
                f"平均分：{self.average_grade():.1f}")

s = Student("小明", "S001")
s.add_grade(85)
s.add_grade(90)
s.add_grade(92)
print(s)
