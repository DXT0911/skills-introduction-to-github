# =============================================================
# 第9节：条件控制语句（if/elif/else）
# =============================================================
# 条件语句让程序可以根据不同条件执行不同的代码块。
# =============================================================

# -------------------------------------------------------
# 1. 基本 if 语句
# -------------------------------------------------------
print("--- 基本 if ---")
temperature = 35

if temperature > 30:
    print("天气很热，多喝水！")

# 没有满足条件时什么也不执行
age = 16
if age >= 18:
    print("你已成年")    # 不会输出

# -------------------------------------------------------
# 2. if...else 语句
# -------------------------------------------------------
print("\n--- if...else ---")
score = 75

if score >= 60:
    print("通过考试！")
else:
    print("未通过考试，需要补考")

# -------------------------------------------------------
# 3. if...elif...else 语句
# -------------------------------------------------------
print("\n--- if...elif...else ---")
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数 {score}，等级 {grade}")

# -------------------------------------------------------
# 4. 嵌套 if 语句
# -------------------------------------------------------
print("\n--- 嵌套 if ---")
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("可以进入")
    else:
        print("需要携带证件")
else:
    print("未成年，不可进入")

# -------------------------------------------------------
# 5. 条件表达式（三元运算符）
# -------------------------------------------------------
print("\n--- 三元运算符 ---")
# 语法：值1 if 条件 else 值2
x = 10
result = "正数" if x > 0 else ("零" if x == 0 else "负数")
print(result)

# 常用场景
numbers = [3, -1, 4, -1, 5, -9]
abs_numbers = [n if n >= 0 else -n for n in numbers]
print(abs_numbers)

# -------------------------------------------------------
# 6. 真值（Truthy）和假值（Falsy）
# -------------------------------------------------------
print("\n--- 真值与假值 ---")
# Python 中以下值为 False（假值）：
# False, None, 0, 0.0, 0j, "", [], (), {}, set()
# 其他所有值都是 True

falsy_values = [False, None, 0, 0.0, "", [], (), {}, set()]
for v in falsy_values:
    if not v:
        print(f"{repr(v):15} 是假值")

print()
truthy_values = [True, 1, 0.1, "hello", [0], (0,), {0}, {"a": 1}]
for v in truthy_values:
    if v:
        print(f"{repr(v):20} 是真值")

# -------------------------------------------------------
# 7. 复合条件
# -------------------------------------------------------
print("\n--- 复合条件 ---")
age = 25
salary = 8000
has_experience = True

# and：所有条件都为真
if age >= 22 and salary >= 5000 and has_experience:
    print("符合招聘条件")

# or：任一条件为真
vip_member = False
points = 1500
if vip_member or points >= 1000:
    print("可以享受折扣")

# not：取反
is_banned = False
if not is_banned:
    print("可以正常使用")

# 链式比较（Python 特有）
x = 15
if 10 <= x <= 20:
    print(f"{x} 在 10 到 20 之间")

# -------------------------------------------------------
# 8. match 语句（Python 3.10+ 结构模式匹配）
# -------------------------------------------------------
# 注：需要 Python 3.10 以上版本
import sys
print("\n--- match 语句 ---")

def describe_point(point):
    """使用 match-case 描述一个点的位置"""
    match point:
        case (0, 0):
            return "原点"
        case (x, 0):
            return f"在 X 轴上，x={x}"
        case (0, y):
            return f"在 Y 轴上，y={y}"
        case (x, y):
            return f"在 ({x}, {y})"

if sys.version_info >= (3, 10):
    print(describe_point((0, 0)))
    print(describe_point((3, 0)))
    print(describe_point((2, 5)))
else:
    print("match 语句需要 Python 3.10+")

# -------------------------------------------------------
# 9. 实用案例：成绩等级系统
# -------------------------------------------------------
print("\n--- 案例：成绩等级系统 ---")

def evaluate_score(score):
    """根据分数给出评价"""
    if not isinstance(score, (int, float)):
        return "无效分数"
    if score < 0 or score > 100:
        return "分数超出范围"

    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 70:
        return "中等"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

test_scores = [95, 82, 71, 65, 50, -5, 105]
for s in test_scores:
    print(f"分数 {s:4}：{evaluate_score(s)}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写一个判断年份是否为闰年的程序
#    （能被4整除但不能被100整除，或能被400整除）
# 2. 根据 BMI 值判断体重状态（BMI = 体重/身高²）
#    < 18.5: 偏瘦，18.5-24.9: 正常，25-29.9: 超重，>= 30: 肥胖
# 3. 编写石头剪刀布游戏的判断逻辑

print("\n--- 练习参考答案 ---")
# 1. 闰年判断
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

for y in [2000, 1900, 2024, 2023]:
    print(f"{y} 年{'是' if is_leap_year(y) else '不是'}闰年")

# 2. BMI 判断
def bmi_status(weight, height):
    bmi = weight / height ** 2
    if bmi < 18.5:
        status = "偏瘦"
    elif bmi < 25:
        status = "正常"
    elif bmi < 30:
        status = "超重"
    else:
        status = "肥胖"
    return f"BMI={bmi:.1f}，{status}"

print(bmi_status(50, 1.70))
print(bmi_status(70, 1.70))

# 3. 石头剪刀布
def rps_result(player1, player2):
    if player1 == player2:
        return "平局"
    wins = {("石头", "剪刀"), ("剪刀", "布"), ("布", "石头")}
    if (player1, player2) in wins:
        return "玩家1赢"
    return "玩家2赢"

print(rps_result("石头", "剪刀"))
print(rps_result("布", "石头"))
print(rps_result("剪刀", "剪刀"))
