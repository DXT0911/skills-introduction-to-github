# =============================================================
# 第20节：上下文管理器（Context Managers）
# =============================================================
# 上下文管理器通过 with 语句使用，保证资源被正确获取和释放。
# 最常见的例子是文件操作（自动关闭文件）。
# =============================================================

# -------------------------------------------------------
# 1. with 语句基础
# -------------------------------------------------------
print("--- with 语句基础 ---")

import os
import tempfile

# 最常见的例子：文件操作
temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8")
temp_path = temp_file.name
temp_file.close()

with open(temp_path, "w", encoding="utf-8") as f:
    f.write("Hello, Context Manager!\n")
    f.write("File is automatically closed after with block.\n")

# 文件在 with 块结束后自动关闭
print(f"文件已关闭：{f.closed}")   # True

# 读取内容
with open(temp_path, "r", encoding="utf-8") as f:
    content = f.read()
print(content)

os.unlink(temp_path)   # 清理

# -------------------------------------------------------
# 2. 上下文管理器协议（__enter__ 和 __exit__）
# -------------------------------------------------------
print("--- 上下文管理器协议 ---")

class ManagedFile:
    """手动实现文件上下文管理器"""

    def __init__(self, filepath, mode="r"):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        """进入 with 块时调用，返回值赋给 as 后的变量"""
        print(f"打开文件：{self.filepath}")
        self.file = open(self.filepath, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        """离开 with 块时调用（无论是否发生异常）"""
        if self.file:
            self.file.close()
            print(f"关闭文件：{self.filepath}")

        if exc_type:
            print(f"发生异常：{exc_type.__name__}: {exc_value}")
            return False   # 返回 False 不抑制异常；True 抑制异常

        return False

# 创建临时文件
temp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                    delete=False, encoding="utf-8")
temp.write("Test content")
temp.close()

with ManagedFile(temp.name) as f:
    print(f.read())

os.unlink(temp.name)

# -------------------------------------------------------
# 3. 使用 contextlib.contextmanager 创建上下文管理器
# -------------------------------------------------------
print("\n--- contextlib.contextmanager ---")
from contextlib import contextmanager

@contextmanager
def timer(name=""):
    """计时上下文管理器"""
    import time
    start = time.time()
    try:
        yield   # 这里是 with 块的内容
    finally:
        elapsed = time.time() - start
        label = f"[{name}] " if name else ""
        print(f"{label}耗时：{elapsed:.4f} 秒")

with timer("排序测试"):
    import random
    data = [random.random() for _ in range(100_000)]
    sorted_data = sorted(data)

# -------------------------------------------------------
# 4. 更多 contextlib 工具
# -------------------------------------------------------
print("\n--- contextlib 工具 ---")
from contextlib import suppress, redirect_stdout
import io

# suppress - 抑制指定异常
with suppress(FileNotFoundError):
    os.remove("/nonexistent/file.txt")
    print("如果没有异常，这行会执行")
print("suppress 不会中断程序")

# redirect_stdout - 重定向标准输出
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("这行会被重定向到 buffer")
    print("这行也是")

output = buffer.getvalue()
print(f"捕获的输出：{output!r}")

# ExitStack - 动态管理多个上下文
from contextlib import ExitStack

files_content = []
with ExitStack() as stack:
    for i in range(3):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=f"_{i}.txt",
                                        delete=False, encoding="utf-8")
        f.write(f"File {i} content")
        f.close()
        tmp = stack.enter_context(open(f.name, "r", encoding="utf-8"))
        files_content.append(tmp.read())
        os.unlink(f.name)

print("多文件内容:", files_content)

# -------------------------------------------------------
# 5. 上下文管理器的实际应用
# -------------------------------------------------------
print("\n--- 实际应用 ---")

# 1. 数据库连接管理
class MockDatabase:
    """模拟数据库连接"""
    def __init__(self, host):
        self.host = host
        self.connected = False
        self.transaction_active = False

    def connect(self):
        self.connected = True
        print(f"连接到数据库：{self.host}")

    def disconnect(self):
        self.connected = False
        print(f"断开数据库连接：{self.host}")

    def execute(self, sql):
        if not self.connected:
            raise RuntimeError("未连接到数据库")
        print(f"执行 SQL：{sql}")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@contextmanager
def database_connection(host):
    """数据库连接上下文管理器"""
    db = MockDatabase(host)
    db.connect()
    try:
        yield db
    except Exception as e:
        print(f"数据库操作失败：{e}")
        raise
    finally:
        db.disconnect()

with database_connection("localhost:5432") as db:
    results = db.execute("SELECT * FROM users")
    for row in results:
        print(f"  用户：{row}")

# 2. 线程锁
import threading

@contextmanager
def locked(lock):
    """加锁上下文管理器"""
    lock.acquire()
    try:
        yield lock
    finally:
        lock.release()

shared_data = []
lock = threading.Lock()

def add_items(items):
    with locked(lock):
        shared_data.extend(items)
        print(f"添加 {items}，当前数据：{shared_data}")

add_items([1, 2, 3])
add_items([4, 5, 6])

# 3. 临时改变工作目录
@contextmanager
def working_directory(path):
    """临时改变工作目录"""
    original = os.getcwd()
    os.chdir(path)
    try:
        yield os.getcwd()
    finally:
        os.chdir(original)

print(f"原始目录：{os.getcwd()}")
with working_directory("/tmp") as cwd:
    print(f"临时目录：{cwd}")
print(f"恢复目录：{os.getcwd()}")

# -------------------------------------------------------
# 6. 嵌套 with 语句
# -------------------------------------------------------
print("\n--- 嵌套 with ---")

# Python 3.10+ 允许括号内的多行 with
import tempfile

temp1 = tempfile.NamedTemporaryFile(mode="w", delete=False,
                                    suffix="_1.txt", encoding="utf-8")
temp2 = tempfile.NamedTemporaryFile(mode="w", delete=False,
                                    suffix="_2.txt", encoding="utf-8")
temp1.write("File 1")
temp2.write("File 2")
temp1.close()
temp2.close()

# 同时打开多个文件
with open(temp1.name, "r", encoding="utf-8") as f1, \
     open(temp2.name, "r", encoding="utf-8") as f2:
    print(f"文件1：{f1.read()}")
    print(f"文件2：{f2.read()}")

os.unlink(temp1.name)
os.unlink(temp2.name)

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 实现一个 TempDirectory 上下文管理器，
#    进入时创建临时目录，退出时删除目录及其内容
# 2. 实现一个 Stopwatch 上下文管理器，支持暂停和继续
# 3. 实现一个事务上下文管理器，在异常时回滚操作

print("\n--- 练习参考答案 ---")
# 1. 临时目录上下文管理器
@contextmanager
def temp_directory():
    """创建临时目录，退出时自动删除"""
    import shutil
    tmpdir = tempfile.mkdtemp()
    print(f"创建临时目录：{tmpdir}")
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        print(f"已删除临时目录：{tmpdir}")

with temp_directory() as tmpdir:
    # 在临时目录中创建文件
    test_file = os.path.join(tmpdir, "test.txt")
    with open(test_file, "w") as f:
        f.write("临时文件内容")
    print(f"临时目录存在：{os.path.exists(tmpdir)}")

print(f"临时目录已删除：{not os.path.exists(tmpdir)}")
