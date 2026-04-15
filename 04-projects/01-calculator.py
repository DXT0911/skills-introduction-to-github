#!/usr/bin/env python3
# =============================================================
# 项目1：命令行计算器
# =============================================================
# 这是一个综合性项目，运用了以下知识点：
#   - 函数定义
#   - 异常处理
#   - 循环和条件语句
#   - 字符串操作
#   - 运算符
# =============================================================


def add(a: float, b: float) -> float:
    """加法"""
    return a + b


def subtract(a: float, b: float) -> float:
    """减法"""
    return a - b


def multiply(a: float, b: float) -> float:
    """乘法"""
    return a * b


def divide(a: float, b: float) -> float:
    """除法（带零除检查）"""
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b


def power(base: float, exp: float) -> float:
    """幂运算"""
    return base ** exp


def modulo(a: float, b: float) -> float:
    """取余"""
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a % b


def sqrt(n: float) -> float:
    """平方根"""
    import math
    if n < 0:
        raise ValueError("不能对负数开平方根")
    return math.sqrt(n)


# 运算符映射
OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
    "%": modulo,
}

HELP_TEXT = """
╔════════════════════════════════════╗
║           Python 计算器            ║
╚════════════════════════════════════╝

支持的运算：
  +   加法      (例：3 + 5)
  -   减法      (例：10 - 4)
  *   乘法      (例：6 * 7)
  /   除法      (例：15 / 3)
  **  幂运算    (例：2 ** 10)
  %   取余      (例：17 % 5)
  sqrt 开方     (例：sqrt 16)

命令：
  help    显示帮助
  hist    查看计算历史
  clear   清除历史
  quit    退出程序
"""


def format_number(n: float) -> str:
    """格式化数字显示（整数不显示小数点）"""
    if n == int(n):
        return str(int(n))
    return f"{n:.10g}"    # 去掉尾随零


def parse_and_calculate(expression: str, history: list) -> str:
    """解析并计算表达式，返回结果字符串"""
    expression = expression.strip()

    # 处理 sqrt
    if expression.lower().startswith("sqrt"):
        parts = expression.split()
        if len(parts) != 2:
            return "错误：格式应为 'sqrt <数字>'"
        try:
            n = float(parts[1])
            result = sqrt(n)
            record = f"√{format_number(n)} = {format_number(result)}"
            history.append(record)
            return f"= {format_number(result)}"
        except ValueError as e:
            return f"错误：{e}"
        except Exception:
            return "错误：无效的数字"

    # 解析 "a op b" 格式
    # 尝试不同的分割策略（处理 ** 等多字符运算符）
    for op in ["**", "+", "-", "*", "/", "%"]:
        # 找到运算符的位置（避免将负号当作减号）
        if op == "-":
            parts = expression.split(op)
            if len(parts) == 2:
                try:
                    a = float(parts[0].strip())
                    b = float(parts[1].strip())
                    result = OPERATIONS[op](a, b)
                    record = f"{format_number(a)} {op} {format_number(b)} = {format_number(result)}"
                    history.append(record)
                    return f"= {format_number(result)}"
                except (ValueError, IndexError):
                    continue
                except ZeroDivisionError as e:
                    return f"错误：{e}"
        else:
            parts = expression.split(op)
            if len(parts) == 2:
                try:
                    a = float(parts[0].strip())
                    b = float(parts[1].strip())
                    result = OPERATIONS[op](a, b)
                    record = f"{format_number(a)} {op} {format_number(b)} = {format_number(result)}"
                    history.append(record)
                    return f"= {format_number(result)}"
                except (ValueError, IndexError):
                    continue
                except ZeroDivisionError as e:
                    return f"错误：{e}"

    return "错误：无法解析表达式，请输入 'help' 查看帮助"


def run_calculator():
    """主计算器循环"""
    history = []
    print(HELP_TEXT)

    while True:
        try:
            user_input = input("计算器> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("quit", "exit", "q"):
            print("再见！")
            break
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "hist":
            if not history:
                print("（暂无历史记录）")
            else:
                print("\n计算历史：")
                for i, record in enumerate(history, 1):
                    print(f"  {i:3}. {record}")
        elif cmd == "clear":
            history.clear()
            print("历史记录已清除")
        else:
            result = parse_and_calculate(user_input, history)
            print(result)


def demo():
    """演示模式：运行一系列预设计算"""
    print("=== 计算器演示模式 ===\n")

    history = []
    test_cases = [
        "3 + 5",
        "100 - 37",
        "6 * 7",
        "15 / 3",
        "2 ** 10",
        "17 % 5",
        "sqrt 144",
        "10 / 0",        # 测试错误处理
        "sqrt -4",       # 测试错误处理
    ]

    for expr in test_cases:
        result = parse_and_calculate(expr, history)
        print(f"  {expr:20} {result}")

    print("\n计算历史：")
    for i, record in enumerate(history, 1):
        print(f"  {i}. {record}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        # 检查是否在交互式环境中
        if sys.stdin.isatty():
            run_calculator()
        else:
            demo()
