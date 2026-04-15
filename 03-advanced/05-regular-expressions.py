# =============================================================
# 第21节：正则表达式（Regular Expressions）
# =============================================================
# 正则表达式是用于匹配字符串模式的强大工具。
# Python 通过内置的 re 模块提供正则表达式支持。
# =============================================================

import re

# -------------------------------------------------------
# 1. 基本模式匹配
# -------------------------------------------------------
print("--- 基本匹配 ---")

# re.match() - 从字符串开头匹配
result = re.match(r"Hello", "Hello, World!")
if result:
    print(f"match: 找到 '{result.group()}' 在位置 {result.start()}-{result.end()}")

# re.search() - 在整个字符串中搜索（找第一个匹配）
result = re.search(r"World", "Hello, World!")
if result:
    print(f"search: 找到 '{result.group()}'")

# re.findall() - 找所有匹配（返回列表）
results = re.findall(r"\d+", "我有 3 只猫和 12 只狗，共 15 只宠物")
print(f"findall 数字: {results}")   # ['3', '12', '15']

# re.finditer() - 找所有匹配（返回迭代器）
for m in re.finditer(r"\d+", "价格：28元，折扣：9折，节省：3元"):
    print(f"  找到数字 '{m.group()}' 在 {m.start()}-{m.end()}")

# -------------------------------------------------------
# 2. 正则表达式语法
# -------------------------------------------------------
print("\n--- 正则语法 ---")

text = "Python 3.11 was released on October 24, 2022."

# 元字符
patterns = {
    r"\d": "任意数字 [0-9]",
    r"\w": "字母、数字或下划线",
    r"\s": "空白字符（空格、制表符等）",
    r".":  "任意字符（除换行）",
}

for pattern, desc in patterns.items():
    matches = re.findall(pattern, text)
    print(f"{desc}：找到 {len(matches)} 个")

# 量词
print("\n量词：")
test = "aabbbcccc"
print(f"a+  : {re.findall(r'a+', test)}")     # 一个或多个 a
print(f"b*  : {re.findall(r'b*', test)}")     # 零个或多个 b
print(f"c?  : {re.findall(r'c?', test)}")     # 零个或一个 c
print(f"b{{2,3}}: {re.findall(r'b{2,3}', test)}")  # 2到3个 b

# 字符集
print("\n字符集：")
print(re.findall(r"[aeiou]", "Hello World"))   # 元音字母
print(re.findall(r"[A-Z]", "Hello World"))     # 大写字母
print(re.findall(r"[^aeiou ]", "hello world")) # 非元音非空格

# 锚点
print("\n锚点：")
lines = ["Python is great", "I love Python", "Python Python"]
for line in lines:
    print(f"  '{line}'")
    print(f"    ^Python: {bool(re.match(r'^Python', line))}")  # 以 Python 开头
    print(f"    Python$: {bool(re.search(r'Python$', line))}")  # 以 Python 结尾

# -------------------------------------------------------
# 3. 分组（Groups）
# -------------------------------------------------------
print("\n--- 分组 ---")

# 基本分组
date_str = "2025-04-15"
match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
if match:
    print(f"完整匹配：{match.group(0)}")   # 或 match.group()
    print(f"年：{match.group(1)}")
    print(f"月：{match.group(2)}")
    print(f"日：{match.group(3)}")
    year, month, day = match.groups()
    print(f"解包：{year}/{month}/{day}")

# 命名分组
match = re.match(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", date_str)
if match:
    print(f"\n命名分组：")
    print(f"年：{match.group('year')}")
    print(f"月：{match.group('month')}")

# 非捕获分组 (?:...)
text = "color colour"
print(re.findall(r"colou?r", text))             # ['color', 'colour']
print(re.findall(r"colo(?:u?)r", text))         # 同上，但 (?:) 不捕获

# -------------------------------------------------------
# 4. 特殊语法
# -------------------------------------------------------
print("\n--- 特殊语法 ---")

# 前瞻（lookahead）和后顾（lookbehind）
prices = "苹果$5.00，香蕉$3.50，橙子$2.00"

# 正向前瞻 (?=...)：匹配后面跟着指定内容的位置
# 正向后顾 (?<=...)：匹配前面是指定内容的位置
prices_only = re.findall(r"(?<=\$)\d+\.\d+", prices)
print(f"价格数字：{prices_only}")

# 非贪婪匹配（? 在量词后面）
html = "<b>粗体</b>和<i>斜体</i>"
print(f"贪婪：{re.findall(r'<.+>', html)}")       # 整个字符串
print(f"非贪婪：{re.findall(r'<.+?>', html)}")    # 每个标签

# -------------------------------------------------------
# 5. re.sub() - 替换
# -------------------------------------------------------
print("\n--- 替换 ---")

# 基本替换
text = "Hello     World   Python"
# 将多个空格替换为单个空格
result = re.sub(r"\s+", " ", text)
print(result)   # "Hello World Python"

# 使用函数作为替换
def double_number(match):
    return str(int(match.group()) * 2)

text = "I have 3 cats and 5 dogs"
result = re.sub(r"\d+", double_number, text)
print(result)   # "I have 6 cats and 10 dogs"

# 使用分组引用
date = "2025-04-15"
# 将 YYYY-MM-DD 转为 DD/MM/YYYY
result = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", date)
print(result)   # "15/04/2025"

# 脱敏处理（隐藏中间字符）
phone = "13812345678"
result = re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", phone)
print(result)   # "138****5678"

# -------------------------------------------------------
# 6. re.split() - 分割
# -------------------------------------------------------
print("\n--- 分割 ---")

# 按标点符号分割
text = "苹果,香蕉;橙子，葡萄;草莓"
parts = re.split(r"[,;，；]", text)
print(parts)    # ['苹果', '香蕉', '橙子', '葡萄', '草莓']

# 分割并保留分隔符
parts = re.split(r"([,;])", "a,b;c,d")
print(parts)    # ['a', ',', 'b', ';', 'c', ',', 'd']

# -------------------------------------------------------
# 7. 编译正则表达式（提高性能）
# -------------------------------------------------------
print("\n--- 编译正则 ---")

# re.compile() 预编译正则，适合重复使用的模式
email_pattern = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

emails = [
    "alice@example.com",
    "bob.smith@company.org",
    "invalid-email",
    "test123@test.co.uk",
    "not an email"
]

for email in emails:
    if email_pattern.match(email):
        print(f"  ✓ {email}")
    else:
        print(f"  ✗ {email}")

# -------------------------------------------------------
# 8. 标志（Flags）
# -------------------------------------------------------
print("\n--- 正则标志 ---")

text = "Hello\nWorld\nPython"

# re.IGNORECASE (re.I) - 忽略大小写
print(re.findall(r"python", text, re.IGNORECASE))  # ['Python']

# re.MULTILINE (re.M) - 多行模式（^ 和 $ 匹配每行开头结尾）
print(re.findall(r"^\w+", text, re.MULTILINE))     # 每行第一个单词

# re.DOTALL (re.S) - . 匹配包括换行在内的所有字符
print(re.findall(r"Hello.World", text, re.DOTALL))

# 组合多个标志
print(re.findall(r"^python", text, re.MULTILINE | re.IGNORECASE))

# -------------------------------------------------------
# 9. 实用案例
# -------------------------------------------------------
print("\n--- 实用案例 ---")

# 验证邮箱
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

# 验证手机号（中国）
def validate_phone(phone):
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, phone))

# 提取 URL
def extract_urls(text):
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)

# 提取 HTML 标签内容
def extract_html_text(html):
    pattern = r"<[^>]+>"
    return re.sub(pattern, "", html)

# 测试
print("邮箱验证：")
for email in ["test@example.com", "invalid.email", "a@b.c"]:
    print(f"  {email}: {'有效' if validate_email(email) else '无效'}")

print("手机验证：")
for phone in ["13812345678", "12345678901", "138123456789"]:
    print(f"  {phone}: {'有效' if validate_phone(phone) else '无效'}")

text = "访问 https://www.python.org 和 http://docs.python.org 了解更多"
print(f"提取 URL：{extract_urls(text)}")

html = "<h1>标题</h1><p>这是<b>粗体</b>文字</p>"
print(f"HTML 纯文本：{extract_html_text(html)}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写正则表达式验证中国身份证号码（18位，最后一位可以是X）
# 2. 从文本中提取所有金额（如：¥123.45、$99.99）
# 3. 编写一个函数，将驼峰命名转换为下划线命名
#    （如 "camelCase" → "camel_case"）

print("\n--- 练习参考答案 ---")
# 1. 身份证验证
def validate_id_card(id_card):
    pattern = r"^\d{17}[\dX]$"
    return bool(re.match(pattern, id_card))

print(validate_id_card("11010119900307099X"))  # True
print(validate_id_card("123456"))              # False

# 2. 提取金额
text = "商品A ¥123.45，商品B $99.99，商品C €50"
amounts = re.findall(r"[¥$€]\d+(?:\.\d{2})?", text)
print(f"金额：{amounts}")

# 3. 驼峰转下划线
def camel_to_snake(name):
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s1).lower()

for name in ["camelCase", "CamelCase", "HTTPRequest", "getHTTPSUrl"]:
    print(f"  {name} → {camel_to_snake(name)}")
