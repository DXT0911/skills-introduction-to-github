# =============================================================
# 第19节：生成器与迭代器（Generators and Iterators）
# =============================================================
# 生成器是一种特殊的迭代器，使用懒求值，节省内存。
# 对于大数据集处理，生成器是非常强大的工具。
# =============================================================

# -------------------------------------------------------
# 1. 迭代器协议
# -------------------------------------------------------
print("--- 迭代器协议 ---")

# 可迭代对象（Iterable）：实现了 __iter__ 方法
# 迭代器（Iterator）：同时实现了 __iter__ 和 __next__ 方法

# 手动使用 iter() 和 next()
my_list = [1, 2, 3]
it = iter(my_list)      # 获取迭代器

print(next(it))   # 1
print(next(it))   # 2
print(next(it))   # 3
try:
    print(next(it))   # StopIteration
except StopIteration:
    print("迭代结束")

# for 循环本质上就是调用 iter() 和 next()
for item in [10, 20, 30]:
    print(item, end=" ")
print()

# -------------------------------------------------------
# 2. 自定义迭代器
# -------------------------------------------------------
print("\n--- 自定义迭代器 ---")

class CountDown:
    """倒计时迭代器"""
    def __init__(self, start):
        self.start = start
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in CountDown(5):
    print(n, end=" ")
print()

# 自定义无限迭代器
class Fibonacci:
    """斐波那契数列迭代器"""
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value

import itertools
fib = Fibonacci()
first_10 = list(itertools.islice(fib, 10))
print("斐波那契前10项:", first_10)

# -------------------------------------------------------
# 3. 生成器函数（yield）
# -------------------------------------------------------
print("\n--- 生成器函数 ---")

# 使用 yield 关键字的函数是生成器函数
def simple_generator():
    print("生成第一个值")
    yield 1
    print("生成第二个值")
    yield 2
    print("生成第三个值")
    yield 3
    print("生成器结束")

gen = simple_generator()
print(f"生成器对象：{gen}")
print(next(gen))    # 生成第一个值 → 1
print(next(gen))    # 生成第二个值 → 2
print(next(gen))    # 生成第三个值 → 3

# for 循环遍历生成器
def count_up(start, end):
    """生成 start 到 end 的整数序列"""
    current = start
    while current <= end:
        yield current
        current += 1

for n in count_up(1, 5):
    print(n, end=" ")
print()

# -------------------------------------------------------
# 4. 生成器表达式
# -------------------------------------------------------
print("\n--- 生成器表达式 ---")

# 列表推导式（立即计算所有值）
lst = [n**2 for n in range(5)]
print(f"列表：{lst}")

# 生成器表达式（懒求值）
gen = (n**2 for n in range(5))
print(f"生成器：{gen}")
print(f"值：{list(gen)}")

# 节省内存的例子
import sys

# 100万个数的和
# 方式1：列表（占用大量内存）
# big_list = [n for n in range(1_000_000)]
# sum(big_list)  # 约 8MB

# 方式2：生成器（几乎不占内存）
gen_sum = sum(n for n in range(1_000_000))
print(f"生成器求和结果：{gen_sum}")

# -------------------------------------------------------
# 5. yield from
# -------------------------------------------------------
print("\n--- yield from ---")

def flatten(nested):
    """展开嵌套列表"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # 委托给子生成器
        else:
            yield item

nested_list = [1, [2, 3], [4, [5, 6]], 7]
flat = list(flatten(nested_list))
print(flat)   # [1, 2, 3, 4, 5, 6, 7]

def chain(*iterables):
    """合并多个可迭代对象"""
    for it in iterables:
        yield from it

result = list(chain([1, 2], [3, 4], [5, 6]))
print(result)   # [1, 2, 3, 4, 5, 6]

# -------------------------------------------------------
# 6. 生成器的 send() 方法
# -------------------------------------------------------
print("\n--- 生成器 send() ---")

def accumulator():
    """累加器：接收值并返回累计和"""
    total = 0
    while True:
        value = yield total   # yield 返回当前 total，并接收 send 的值
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)          # 启动生成器（到第一个 yield）
print(gen.send(10))   # 发送 10，返回 10
print(gen.send(20))   # 发送 20，返回 30
print(gen.send(30))   # 发送 30，返回 60

# -------------------------------------------------------
# 7. 实际应用：处理大文件
# -------------------------------------------------------
print("\n--- 实际应用：大文件处理 ---")

def read_large_file_chunks(filepath, chunk_size=1024):
    """逐块读取大文件（不会将整个文件载入内存）"""
    import io
    fake_file = io.StringIO("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")
    for line in fake_file:
        yield line.strip()

def count_words_in_lines(lines):
    """统计每行的单词数"""
    for line in lines:
        yield len(line.split())

lines = read_large_file_chunks("/dev/null")
word_counts = count_words_in_lines(lines)

# 管道式处理（只有需要时才计算）
for count in word_counts:
    print(f"本行 {count} 个单词")

# -------------------------------------------------------
# 8. itertools 中的无限迭代器
# -------------------------------------------------------
print("\n--- itertools 无限迭代器 ---")
import itertools

# count() - 从 start 开始无限计数
counter = itertools.count(10, 2)   # 从 10 开始，步长 2
print(list(itertools.islice(counter, 5)))   # [10, 12, 14, 16, 18]

# cycle() - 无限循环
cycler = itertools.cycle(["A", "B", "C"])
print(list(itertools.islice(cycler, 7)))    # ['A', 'B', 'C', 'A', 'B', 'C', 'A']

# repeat() - 无限重复（或指定次数）
repeater = itertools.repeat("Python", 3)
print(list(repeater))                        # ['Python', 'Python', 'Python']

# -------------------------------------------------------
# 9. 生成器性能对比
# -------------------------------------------------------
print("\n--- 性能对比 ---")

import time

# 普通函数（创建完整列表）
def get_numbers_list(n):
    return [i * i for i in range(n)]

# 生成器函数
def get_numbers_gen(n):
    for i in range(n):
        yield i * i

n = 10_000_000

start = time.time()
lst = get_numbers_list(n)
s1 = sum(lst)
list_time = time.time() - start

start = time.time()
gen = get_numbers_gen(n)
s2 = sum(gen)
gen_time = time.time() - start

print(f"列表方式：{list_time:.3f}秒，和={s1}")
print(f"生成器方式：{gen_time:.3f}秒，和={s2}")
print(f"内存大小对比：列表约 {sys.getsizeof(get_numbers_list(100))} 字节（100个元素）")
print(f"              生成器约 {sys.getsizeof(get_numbers_gen(100))} 字节（不受数量影响）")

import sys

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写一个生成器，生成指定范围内的所有素数
# 2. 编写一个生成器，读取 CSV 文件并逐行解析（无需加载整个文件）
# 3. 使用生成器实现一个无限的 ID 生成器

print("\n--- 练习参考答案 ---")
# 1. 素数生成器
def prime_generator(limit):
    """生成 2 到 limit 之间的所有素数"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    for n in range(2, limit + 1):
        if is_prime(n):
            yield n

primes = list(prime_generator(50))
print(f"50以内的素数：{primes}")

# 2. ID 生成器
def id_generator(prefix="ID", start=1):
    """无限 ID 生成器"""
    counter = start
    while True:
        yield f"{prefix}-{counter:06d}"
        counter += 1

gen = id_generator("USER")
print(next(gen))    # USER-000001
print(next(gen))    # USER-000002
print(next(gen))    # USER-000003
