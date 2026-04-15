# =============================================================
# 第14节：文件读写（File I/O）
# =============================================================
# Python 提供了内置的文件操作功能，让我们可以读写文件。
# 处理文件时，始终推荐使用 with 语句确保文件被正确关闭。
# =============================================================

import os
import json
import csv
import tempfile

# 创建临时目录用于演示
DEMO_DIR = tempfile.mkdtemp()

# -------------------------------------------------------
# 1. 写入文本文件
# -------------------------------------------------------
print("--- 写入文件 ---")
filepath = os.path.join(DEMO_DIR, "hello.txt")

# 写入模式 "w"（会覆盖已有文件）
with open(filepath, "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
    f.write("文件读写很简单。\n")
    f.write("第三行内容。\n")

print(f"已写入文件：{filepath}")

# 追加模式 "a"（在文件末尾追加内容）
with open(filepath, "a", encoding="utf-8") as f:
    f.write("追加的第四行。\n")

# writelines() - 写入多行
lines = ["第五行\n", "第六行\n", "第七行\n"]
with open(filepath, "a", encoding="utf-8") as f:
    f.writelines(lines)

print("写入完成")

# -------------------------------------------------------
# 2. 读取文本文件
# -------------------------------------------------------
print("\n--- 读取文件 ---")

# read() - 读取全部内容（字符串）
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()
print("全部内容：")
print(content)

# readline() - 读取一行
with open(filepath, "r", encoding="utf-8") as f:
    first_line = f.readline()
    second_line = f.readline()
print(f"第一行：{first_line.strip()}")
print(f"第二行：{second_line.strip()}")

# readlines() - 读取所有行（列表）
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"共 {len(lines)} 行")

# 逐行读取（内存高效）
with open(filepath, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"第{i}行：{line.strip()}")

# -------------------------------------------------------
# 3. 文件打开模式
# -------------------------------------------------------
print("\n--- 文件模式 ---")
print("""
常用文件打开模式：
  "r"   - 只读（默认）
  "w"   - 写入（会覆盖已有内容）
  "a"   - 追加
  "x"   - 创建新文件（文件已存在则报错）
  "b"   - 二进制模式（与其他模式组合：rb, wb）
  "t"   - 文本模式（默认）
  "+"   - 读写模式（与其他模式组合：r+, w+）
""")

# -------------------------------------------------------
# 4. 文件指针
# -------------------------------------------------------
print("--- 文件指针 ---")
with open(filepath, "r", encoding="utf-8") as f:
    print(f"当前位置：{f.tell()}")   # 0
    f.read(5)                          # 读取 5 个字符
    print(f"读取后位置：{f.tell()}")

    f.seek(0)                          # 回到文件开头
    print(f"seek(0) 后位置：{f.tell()}")

# -------------------------------------------------------
# 5. JSON 文件操作
# -------------------------------------------------------
print("\n--- JSON 文件操作 ---")
json_path = os.path.join(DEMO_DIR, "data.json")

# 写入 JSON
data = {
    "students": [
        {"name": "Alice", "age": 20, "grades": [85, 90, 92]},
        {"name": "Bob", "age": 22, "grades": [78, 88, 80]},
    ],
    "class": "Python 101",
    "year": 2025
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"已写入 JSON：{json_path}")

# 读取 JSON
with open(json_path, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print(f"班级：{loaded_data['class']}")
print(f"学生数：{len(loaded_data['students'])}")
for student in loaded_data["students"]:
    avg = sum(student["grades"]) / len(student["grades"])
    print(f"  {student['name']}：平均分 {avg:.1f}")

# -------------------------------------------------------
# 6. CSV 文件操作
# -------------------------------------------------------
print("\n--- CSV 文件操作 ---")
csv_path = os.path.join(DEMO_DIR, "students.csv")

# 写入 CSV
students = [
    ["姓名", "年龄", "成绩"],
    ["Alice", 20, 85],
    ["Bob", 22, 90],
    ["Charlie", 21, 78],
]

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"已写入 CSV：{csv_path}")

# 读取 CSV
with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 使用 DictReader/DictWriter（推荐）
people = [
    {"姓名": "Dave", "年龄": 23, "成绩": 92},
    {"姓名": "Eve", "年龄": 24, "成绩": 88},
]
csv_path2 = os.path.join(DEMO_DIR, "people.csv")
with open(csv_path2, "w", newline="", encoding="utf-8-sig") as f:
    fieldnames = ["姓名", "年龄", "成绩"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(people)

with open(csv_path2, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))

# -------------------------------------------------------
# 7. 二进制文件操作
# -------------------------------------------------------
print("\n--- 二进制文件 ---")
bin_path = os.path.join(DEMO_DIR, "data.bin")

# 写入二进制
data_bytes = bytes([0, 1, 2, 3, 255, 128])
with open(bin_path, "wb") as f:
    f.write(data_bytes)

# 读取二进制
with open(bin_path, "rb") as f:
    read_bytes = f.read()
print(f"读取到的字节：{list(read_bytes)}")

# -------------------------------------------------------
# 8. 文件和目录操作
# -------------------------------------------------------
print("\n--- 文件系统操作 ---")

# os 模块
print(f"当前目录：{os.getcwd()}")
print(f"目录内容：{os.listdir(DEMO_DIR)}")

# 检查文件是否存在
test_path = os.path.join(DEMO_DIR, "test.txt")
print(f"文件存在：{os.path.exists(test_path)}")

# 创建目录
new_dir = os.path.join(DEMO_DIR, "subdir")
os.makedirs(new_dir, exist_ok=True)
print(f"已创建目录：{new_dir}")

# 文件信息
stat = os.stat(filepath)
print(f"文件大小：{stat.st_size} 字节")

# pathlib 模块（现代推荐方式）
from pathlib import Path

p = Path(DEMO_DIR)
print(f"\npathlib 示例：")
print(f"路径：{p}")
print(f"是目录：{p.is_dir()}")
print(f"目录内容：{[x.name for x in p.iterdir()]}")

txt_file = p / "hello.txt"    # 路径拼接
print(f"文件名：{txt_file.name}")
print(f"后缀：{txt_file.suffix}")
print(f"文件大小：{txt_file.stat().st_size} 字节")

# 使用 pathlib 读写文件
(p / "pathlib_test.txt").write_text("Hello from pathlib!\n", encoding="utf-8")
content = (p / "pathlib_test.txt").read_text(encoding="utf-8")
print(f"pathlib 读取：{content.strip()}")

# -------------------------------------------------------
# 9. 清理临时文件
# -------------------------------------------------------
import shutil
shutil.rmtree(DEMO_DIR)
print(f"\n已清理临时目录：{DEMO_DIR}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 将一段文字写入文件，再读取并统计其中各词的频率
# 2. 读取一个 CSV 文件，计算某列的平均值
# 3. 将 Python 字典列表序列化为 JSON 文件，再读取并查询

print("\n--- 练习提示 ---")
print("1. 使用 write() 写入，read().split() 分词，Counter 统计")
print("2. 使用 csv.DictReader 读取，float() 转换，求和后除以行数")
print("3. 使用 json.dump() 写入，json.load() 读取")
