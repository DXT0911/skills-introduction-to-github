# =============================================================
# 第22节：异步编程（Async Programming）
# =============================================================
# Python 的 asyncio 模块提供了基于协程的异步编程支持。
# 异步编程适合 I/O 密集型任务（网络请求、文件操作等）。
# =============================================================

import asyncio
import time
import random

# -------------------------------------------------------
# 1. 同步 vs 异步对比
# -------------------------------------------------------
print("--- 同步 vs 异步 ---")

# 同步版本（顺序执行，耗时较长）
def sync_fetch(url):
    """模拟同步 HTTP 请求"""
    time.sleep(0.1)   # 模拟网络延迟
    return f"来自 {url} 的响应"

def sync_main():
    urls = [f"https://api.example.com/{i}" for i in range(5)]
    start = time.time()
    results = [sync_fetch(url) for url in urls]
    elapsed = time.time() - start
    print(f"同步：获取 {len(results)} 个响应，耗时 {elapsed:.2f} 秒")

sync_main()

# -------------------------------------------------------
# 2. 协程基础（async/await）
# -------------------------------------------------------
print("\n--- 协程基础 ---")

async def say_hello(name, delay=0):
    """简单的协程"""
    await asyncio.sleep(delay)   # 非阻塞等待
    print(f"Hello, {name}!")
    return f"greeting sent to {name}"

async def main_basic():
    # 直接 await 一个协程
    result = await say_hello("Alice")
    print(result)

asyncio.run(main_basic())

# -------------------------------------------------------
# 3. 并发执行（asyncio.gather）
# -------------------------------------------------------
print("\n--- 并发执行 ---")

async def async_fetch(url):
    """模拟异步 HTTP 请求"""
    delay = random.uniform(0.05, 0.2)
    await asyncio.sleep(delay)
    return f"来自 {url} 的响应（延迟 {delay:.2f}s）"

async def async_main():
    urls = [f"https://api.example.com/{i}" for i in range(5)]
    start = time.time()

    # gather 同时执行多个协程（并发，不是并行）
    results = await asyncio.gather(*[async_fetch(url) for url in urls])

    elapsed = time.time() - start
    print(f"异步：获取 {len(results)} 个响应，耗时 {elapsed:.2f} 秒")
    for r in results:
        print(f"  {r}")

asyncio.run(async_main())

# -------------------------------------------------------
# 4. asyncio.create_task - 任务管理
# -------------------------------------------------------
print("\n--- 任务管理 ---")

async def background_task(name, duration):
    """后台任务"""
    print(f"任务 {name} 开始")
    await asyncio.sleep(duration)
    print(f"任务 {name} 完成（用时 {duration:.1f}s）")
    return f"{name} 的结果"

async def main_tasks():
    # 创建任务（立即开始，不需要 await）
    task1 = asyncio.create_task(background_task("A", 0.2))
    task2 = asyncio.create_task(background_task("B", 0.1))
    task3 = asyncio.create_task(background_task("C", 0.15))

    print("所有任务已创建，等待完成...")

    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)
    print("所有任务完成:", results)

asyncio.run(main_tasks())

# -------------------------------------------------------
# 5. 异步生成器
# -------------------------------------------------------
print("\n--- 异步生成器 ---")

async def async_number_generator(start, end):
    """异步生成器"""
    for i in range(start, end):
        await asyncio.sleep(0.01)   # 模拟异步操作
        yield i

async def main_async_gen():
    total = 0
    async for n in async_number_generator(1, 6):
        total += n
        print(f"  接收到 {n}，累计 {total}")
    print(f"总和：{total}")

asyncio.run(main_async_gen())

# -------------------------------------------------------
# 6. 异步上下文管理器
# -------------------------------------------------------
print("\n--- 异步上下文管理器 ---")

class AsyncDatabaseConnection:
    """模拟异步数据库连接"""

    def __init__(self, host):
        self.host = host
        self.connected = False

    async def __aenter__(self):
        await asyncio.sleep(0.05)   # 模拟连接延迟
        self.connected = True
        print(f"已连接到 {self.host}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.01)   # 模拟断开延迟
        self.connected = False
        print(f"已断开 {self.host} 的连接")
        return False

    async def query(self, sql):
        if not self.connected:
            raise RuntimeError("数据库未连接")
        await asyncio.sleep(0.05)   # 模拟查询延迟
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

async def main_async_ctx():
    async with AsyncDatabaseConnection("localhost:5432") as db:
        results = await db.query("SELECT * FROM users")
        print(f"查询结果：{results}")

asyncio.run(main_async_ctx())

# -------------------------------------------------------
# 7. 超时和取消
# -------------------------------------------------------
print("\n--- 超时和取消 ---")

async def slow_operation(name, duration):
    """慢速操作"""
    print(f"开始 {name}（预计 {duration}s）")
    await asyncio.sleep(duration)
    return f"{name} 完成"

async def main_timeout():
    # 设置超时
    try:
        result = await asyncio.wait_for(
            slow_operation("慢操作", 5.0),
            timeout=0.2
        )
        print(result)
    except asyncio.TimeoutError:
        print("操作超时！")

    # 取消任务
    task = asyncio.create_task(slow_operation("可取消操作", 10.0))
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("任务已取消")

asyncio.run(main_timeout())

# -------------------------------------------------------
# 8. 信号量控制并发数
# -------------------------------------------------------
print("\n--- 信号量 ---")

async def fetch_with_limit(semaphore, url):
    """使用信号量限制并发请求数"""
    async with semaphore:
        delay = random.uniform(0.05, 0.15)
        await asyncio.sleep(delay)
        return f"响应来自 {url}"

async def main_semaphore():
    # 最多 3 个并发请求
    semaphore = asyncio.Semaphore(3)
    urls = [f"https://api.example.com/{i}" for i in range(10)]

    start = time.time()
    tasks = [fetch_with_limit(semaphore, url) for url in urls]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"获取 {len(results)} 个结果，耗时 {elapsed:.2f}s（最多3个并发）")

asyncio.run(main_semaphore())

# -------------------------------------------------------
# 9. asyncio.Queue - 生产者消费者模式
# -------------------------------------------------------
print("\n--- 生产者消费者 ---")

async def producer(queue, n):
    """生产者：生成工作项"""
    for i in range(n):
        await asyncio.sleep(random.uniform(0.01, 0.05))
        await queue.put(f"工作项_{i}")
        print(f"  生产：工作项_{i}")
    await queue.put(None)   # 发送结束信号

async def consumer(queue):
    """消费者：处理工作项"""
    while True:
        item = await queue.get()
        if item is None:
            break
        await asyncio.sleep(random.uniform(0.02, 0.08))
        print(f"  消费：{item}")
        queue.task_done()

async def main_producer_consumer():
    queue = asyncio.Queue(maxsize=3)

    producer_task = asyncio.create_task(producer(queue, 5))
    consumer_task = asyncio.create_task(consumer(queue))

    await asyncio.gather(producer_task, consumer_task)
    print("生产消费完成")

asyncio.run(main_producer_consumer())

# -------------------------------------------------------
# 10. 在同步代码中使用异步
# -------------------------------------------------------
print("\n--- 同步调用异步 ---")

async def async_calculate(x, y):
    await asyncio.sleep(0.01)
    return x + y

# 方式1：asyncio.run（最简单，每次创建新事件循环）
result = asyncio.run(async_calculate(10, 20))
print(f"结果：{result}")

# -------------------------------------------------------
# 练习题
# -------------------------------------------------------
# 1. 编写异步函数，并发下载 5 个 URL（用 asyncio.sleep 模拟）
# 2. 实现一个异步速率限制器，控制每秒最多执行 N 次操作
# 3. 实现异步重试装饰器，失败时等待后重试

print("\n--- 练习参考答案 ---")

# 1. 并发模拟下载
async def download(url):
    delay = random.uniform(0.1, 0.5)
    await asyncio.sleep(delay)
    size = random.randint(100, 1000)
    return {"url": url, "size": size, "time": delay}

async def download_all():
    urls = [f"https://files.example.com/file_{i}.zip" for i in range(5)]
    start = time.time()
    results = await asyncio.gather(*[download(url) for url in urls])
    total_time = time.time() - start
    total_size = sum(r["size"] for r in results)
    print(f"并发下载 {len(results)} 个文件：")
    for r in results:
        print(f"  {r['url'].split('/')[-1]}: {r['size']}KB，用时 {r['time']:.2f}s")
    print(f"总计：{total_size}KB，总耗时 {total_time:.2f}s")

asyncio.run(download_all())
