# =============================================================
# 第4节：字符串操作
# =============================================================
# 字符串是 Python 中最常用的数据类型之一。
# 本节详细介绍字符串的创建、访问和各种操作方法。
# =============================================================

# -------------------------------------------------------
# 1. 字符串创建
# -------------------------------------------------------
print("--- 字符串创建 ---")
s1 = "双引号字符串"
s2 = '单引号字符串'
s3 = """
多行字符串
第二行
第三行
"""
# 原始字符串（raw string）：忽略转义字符
path = r"C:\Users\Alice\Desktop"
print(path)           # C:\Users\Alice\Desktop

# -------------------------------------------------------
# 2. 转义字符
# -------------------------------------------------------
print("\n--- 转义字符 ---")
print("Hello\nWorld")      # \n 换行
print("A\tB\tC")           # \t 制表符
print("She said \"Hi\"")   # \" 双引号
print('It\'s fine')        # \' 单引号
print("反斜杠: \\")         # \\ 反斜杠

# -------------------------------------------------------
# 3. 字符串索引与切片
# -------------------------------------------------------
print("\n--- 索引与切片 ---")
s = "Python"
#    P  y  t  h  o  n
#    0  1  2  3  4  5   正向索引
#   -6 -5 -4 -3 -2 -1   反向索引

print(s[0])      # P（第一个字符）
print(s[-1])     # n（最后一个字符）
print(s[2])      # t

# 切片 [start:end:step]（不包括 end）
print(s[0:3])    # Pyt（索引 0, 1, 2）
print(s[2:])     # thon（从索引 2 到末尾）
print(s[:4])     # Pyth（从开头到索引 3）
print(s[::2])    # Pto（步长为 2）
print(s[::-1])   # nohtyP（反转字符串）

# -------------------------------------------------------
# 4. 字符串运算
# -------------------------------------------------------
print("\n--- 字符串运算 ---")
# 拼接
first = "Hello"
second = "World"
result = first + ", " + second + "!"
print(result)         # Hello, World!

# 重复
line = "-" * 20
print(line)           # --------------------

# 成员检查
print("ell" in "Hello")    # True
print("xyz" in "Hello")    # False

# -------------------------------------------------------
# 5. 字符串常用方法
# -------------------------------------------------------
print("\n--- 字符串方法 ---")
text = "  Hello, Python World!  "

# 大小写转换
print(text.upper())           # 全部大写
print(text.lower())           # 全部小写
print(text.title())           # 首字母大写
print(text.swapcase())        # 大小写互换

# 去除空白
print(text.strip())           # 去除两端空白
print(text.lstrip())          # 去除左端空白
print(text.rstrip())          # 去除右端空白

# 查找与替换
s = "Hello, Python!"
print(s.find("Python"))       # 7（返回起始索引）
print(s.find("Java"))         # -1（未找到）
print(s.index("Python"))      # 7
print(s.replace("Python", "World"))   # Hello, World!
print(s.count("l"))           # 2（统计出现次数）

# 分割与连接
words = "apple,banana,cherry"
lst = words.split(",")         # 按逗号分割
print(lst)                     # ['apple', 'banana', 'cherry']

joined = "-".join(lst)         # 用 - 连接列表
print(joined)                  # apple-banana-cherry

# 检查字符串内容
print("12345".isdigit())       # True（全是数字）
print("hello".isalpha())       # True（全是字母）
print("hello123".isalnum())    # True（字母或数字）
print("  ".isspace())          # True（全是空白）
print("Hello".startswith("He"))  # True
print("Hello".endswith("lo"))    # True

# 对齐
print("Hi".center(10))         # "    Hi    "
print("Hi".ljust(10, "-"))     # "Hi--------"
print("Hi".rjust(10, "-"))     # "--------Hi"

# -------------------------------------------------------
# 6. 字符串格式化
# -------------------------------------------------------
print("\n--- 字符串格式化 ---")
name = "Alice"
age = 25
score = 98.5

# 方式1：% 格式化（老式风格）
print("姓名：%s，年龄：%d，分数：%.1f" % (name, age, score))

# 方式2：str.format()
print("姓名：{}，年龄：{}，分数：{:.1f}".format(name, age, score))
print("姓名：{0}，年龄：{1}，分数：{2:.1f}".format(name, age, score))
print("姓名：{n}，年龄：{a}".format(n=name, a=age))

# 方式3：f-string（推荐，Python 3.6+）
print(f"姓名：{name}，年龄：{age}，分数：{score:.1f}")
print(f"计算结果：{2 ** 10}")       # 可以直接写表达式
print(f"{'居中':^20}")              # 格式化对齐
print(f"{3.14159:.3f}")            # 保留3位小数

# -------------------------------------------------------
# 7. 字符串与字符
# -------------------------------------------------------
print("\n--- 字符与编码 ---")
# ord() 获取字符的 Unicode 编码
print(ord('A'))     # 65
print(ord('a'))     # 97
print(ord('中'))    # 20013

# chr() 将编码转为字符
print(chr(65))      # A
print(chr(20013))   # 中

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 给定字符串 s = "Hello, Python 3!"
#    - 统计其中 'l' 的个数
#    - 将所有小写字母转为大写
#    - 取出 "Python" 子串
# 2. 将用户输入的句子反转（提示：切片 [::-1]）
# 3. 写一个函数，判断一个字符串是否为回文（正读倒读一样）

print("\n--- 练习参考答案 ---")
s = "Hello, Python 3!"
print(s.count('l'))         # 统计 'l'：2
print(s.upper())            # 全部大写
print(s[7:13])              # 取出 "Python"

# 反转字符串
sentence = "Hello Python"
print(sentence[::-1])       # nohtyP olleH

# 判断回文
def is_palindrome(text):
    text = text.lower().replace(" ", "")
    return text == text[::-1]

print(is_palindrome("racecar"))   # True
print(is_palindrome("hello"))     # False
print(is_palindrome("A man a plan a canal Panama"))  # True
