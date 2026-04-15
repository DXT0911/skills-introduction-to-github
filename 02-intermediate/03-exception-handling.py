# =============================================================
# 第13节：异常处理（Exception Handling）
# =============================================================
# 异常是程序运行时发生的错误。通过异常处理，
# 我们可以优雅地处理错误，防止程序崩溃。
# =============================================================

# -------------------------------------------------------
# 1. 常见异常类型
# -------------------------------------------------------
print("--- 常见异常 ---")

# 演示不同类型的异常（注释掉，避免程序崩溃）
# int("abc")          # ValueError
# 1 / 0               # ZeroDivisionError
# x = undefined_var   # NameError
# [1,2,3][10]         # IndexError
# {"a":1}["b"]        # KeyError
# int + "str"         # TypeError
# open("not_exist.txt")  # FileNotFoundError
# import nonexistent  # ModuleNotFoundError

print("Python 内置异常继承层次（部分）：")
print("""
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    ├── NameError
    ├── AttributeError
    ├── FileNotFoundError
    ├── PermissionError
    └── RuntimeError
""")

# -------------------------------------------------------
# 2. try...except 基本用法
# -------------------------------------------------------
print("--- try...except ---")

# 捕获特定异常
try:
    result = 10 / 0
except ZeroDivisionError:
    print("错误：不能除以零")

# 捕获并获取异常信息
try:
    x = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

# 捕获多种异常
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("错误：除数不能为零")
        return None
    except TypeError:
        print("错误：参数类型不正确")
        return None

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # 错误：除数不能为零
print(safe_divide(10, "a")) # 错误：参数类型不正确

# -------------------------------------------------------
# 3. try...except...else...finally
# -------------------------------------------------------
print("\n--- 完整异常处理结构 ---")

def read_number(s):
    try:
        number = int(s)
    except ValueError:
        print(f"'{s}' 不是有效整数")
        return None
    else:
        # 没有发生异常时执行
        print(f"成功解析：{number}")
        return number
    finally:
        # 无论是否发生异常，都会执行
        print("解析操作完成")

read_number("42")
print()
read_number("abc")

# -------------------------------------------------------
# 4. 捕获多个异常
# -------------------------------------------------------
print("\n--- 捕获多个异常 ---")

def process_data(data, index):
    try:
        value = data[index]
        result = 100 / value
        return result
    except (IndexError, KeyError) as e:
        print(f"索引或键错误：{e}")
    except ZeroDivisionError:
        print("除以零错误")
    except Exception as e:
        # 捕获所有其他异常（通用）
        print(f"未预期的错误：{type(e).__name__}: {e}")

process_data([10, 0, 5], 1)     # 除以零
process_data([10, 5], 5)         # 索引错误
process_data([10, 5], 0)         # 正常

# -------------------------------------------------------
# 5. 自定义异常
# -------------------------------------------------------
print("\n--- 自定义异常 ---")

class ValidationError(Exception):
    """数据验证错误"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class AgeError(ValidationError):
    """年龄验证错误"""
    pass

def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"年龄必须是整数，得到 {type(age).__name__}")
    if age < 0:
        raise AgeError("age", "年龄不能为负数")
    if age > 150:
        raise AgeError("age", f"年龄 {age} 超出合理范围")
    return True

for test_age in [25, -1, 200, "abc"]:
    try:
        validate_age(test_age)
        print(f"年龄 {test_age} 验证通过")
    except AgeError as e:
        print(f"年龄验证错误：{e}")
    except TypeError as e:
        print(f"类型错误：{e}")

# -------------------------------------------------------
# 6. raise 语句
# -------------------------------------------------------
print("\n--- raise 语句 ---")

# 主动抛出异常
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("取款金额必须大于零")
    if amount > balance:
        raise ValueError(f"余额不足，当前余额：{balance}")
    return balance - amount

try:
    print(withdraw(1000, 200))
    print(withdraw(1000, 1500))
except ValueError as e:
    print(f"取款失败：{e}")

# 重新抛出异常
def risky_operation():
    raise RuntimeError("操作失败")

def safe_wrapper():
    try:
        risky_operation()
    except RuntimeError as e:
        print(f"捕获到错误，记录日志：{e}")
        raise   # 重新抛出，让上层处理

try:
    safe_wrapper()
except RuntimeError as e:
    print(f"最终处理：{e}")

# -------------------------------------------------------
# 7. 上下文管理与 with 语句（异常安全）
# -------------------------------------------------------
print("\n--- with 语句 ---")

# 文件操作的异常安全写法
import tempfile
import os

# 创建临时文件用于演示
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("Hello\nWorld\nPython")
    temp_path = f.name

try:
    with open(temp_path, "r") as f:
        content = f.read()
    print("文件内容：", content)
except FileNotFoundError:
    print("文件不存在")
except PermissionError:
    print("没有读取权限")
finally:
    os.unlink(temp_path)    # 清理临时文件

# -------------------------------------------------------
# 8. 异常链
# -------------------------------------------------------
print("\n--- 异常链 ---")

class DatabaseError(Exception):
    pass

def connect_db():
    raise ConnectionError("数据库连接超时")

def get_user(user_id):
    try:
        connect_db()
    except ConnectionError as e:
        raise DatabaseError("无法获取用户信息") from e

try:
    get_user(1)
except DatabaseError as e:
    print(f"DatabaseError: {e}")
    print(f"原因: {e.__cause__}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写一个安全的整数解析函数，返回 None 而不是抛出异常
# 2. 自定义 PasswordError 异常，验证密码规则：
#    - 至少 8 位
#    - 包含大小写字母
#    - 包含数字
# 3. 编写一个函数，安全地读取 JSON 文件，处理各种可能的错误

print("\n--- 练习参考答案 ---")
# 1. 安全整数解析
def safe_int(value, default=None):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))       # 42
print(safe_int("abc"))      # None
print(safe_int("abc", 0))   # 0

# 2. 密码验证
class PasswordError(Exception):
    pass

def validate_password(password):
    if len(password) < 8:
        raise PasswordError("密码至少需要 8 位")
    if not any(c.isupper() for c in password):
        raise PasswordError("密码需包含大写字母")
    if not any(c.islower() for c in password):
        raise PasswordError("密码需包含小写字母")
    if not any(c.isdigit() for c in password):
        raise PasswordError("密码需包含数字")
    return True

test_inputs = ["abc", "abcdefgh", "Abcdefgh", "Abcdefg1"]
for test_input in test_inputs:
    try:
        validate_password(test_input)
        print(f"'{test_input}' 验证通过")
    except PasswordError as e:
        print(f"'{test_input}' 验证未通过：{e}")

# 3. 安全读取 JSON
import json

def safe_read_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件不存在：{filepath}")
    except PermissionError:
        print(f"没有权限读取：{filepath}")
    except json.JSONDecodeError as e:
        print(f"JSON 格式错误：{e}")
    except Exception as e:
        print(f"未知错误：{e}")
    return None

result = safe_read_json("/nonexistent/file.json")
print(f"结果：{result}")
