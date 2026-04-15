#!/usr/bin/env python3
# =============================================================
# 项目2：待办事项管理器（To-Do List）
# =============================================================
# 这是一个综合性项目，运用了以下知识点：
#   - 面向对象编程
#   - 文件读写（JSON）
#   - 异常处理
#   - 列表和字典操作
#   - 格式化输出
# =============================================================

import json
import os
from datetime import datetime
from pathlib import Path


class Task:
    """表示一个待办任务"""

    def __init__(self, title: str, description: str = "", priority: str = "中",
                 due_date: str = None):
        self.id = None          # 由 TaskManager 分配
        self.title = title
        self.description = description
        self.priority = priority    # 高 / 中 / 低
        self.due_date = due_date    # "YYYY-MM-DD" 格式
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.completed_at = None

    def complete(self):
        """标记任务为已完成"""
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> dict:
        """转换为字典（用于 JSON 序列化）"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典创建 Task 对象"""
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "中"),
            due_date=data.get("due_date"),
        )
        task.id = data["id"]
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", "")
        task.completed_at = data.get("completed_at")
        return task

    def __str__(self) -> str:
        status = "✅" if self.completed else "⬜"
        priority_icons = {"高": "🔴", "中": "🟡", "低": "🟢"}
        priority_icon = priority_icons.get(self.priority, "⚪")
        due_str = f" [截止：{self.due_date}]" if self.due_date else ""
        return f"[{self.id:3}] {status} {priority_icon} {self.title}{due_str}"


class TaskManager:
    """管理所有待办任务"""

    def __init__(self, storage_file: str = None):
        if storage_file is None:
            storage_file = os.path.join(
                Path.home(), ".todo_list.json"
            )
        self.storage_file = storage_file
        self.tasks = []
        self._next_id = 1
        self.load()

    def load(self):
        """从文件加载任务"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
                    self._next_id = data.get("next_id", 1)
        except (json.JSONDecodeError, KeyError, IOError):
            self.tasks = []
            self._next_id = 1

    def save(self):
        """保存任务到文件"""
        try:
            data = {
                "tasks": [t.to_dict() for t in self.tasks],
                "next_id": self._next_id,
            }
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"保存失败：{e}")

    def add_task(self, title: str, description: str = "",
                 priority: str = "中", due_date: str = None) -> Task:
        """添加新任务"""
        if not title.strip():
            raise ValueError("任务标题不能为空")
        if priority not in ("高", "中", "低"):
            raise ValueError("优先级必须是 高/中/低")

        task = Task(title.strip(), description, priority, due_date)
        task.id = self._next_id
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def get_task(self, task_id: int) -> Task:
        """根据 ID 获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"任务 #{task_id} 不存在")

    def complete_task(self, task_id: int) -> Task:
        """标记任务为已完成"""
        task = self.get_task(task_id)
        if task.completed:
            raise ValueError(f"任务 #{task_id} 已经完成了")
        task.complete()
        self.save()
        return task

    def delete_task(self, task_id: int) -> Task:
        """删除任务"""
        task = self.get_task(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def edit_task(self, task_id: int, **kwargs) -> Task:
        """编辑任务属性"""
        task = self.get_task(task_id)
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        self.save()
        return task

    def list_tasks(self, show_completed: bool = True,
                   filter_priority: str = None) -> list:
        """列出任务"""
        tasks = self.tasks

        if not show_completed:
            tasks = [t for t in tasks if not t.completed]

        if filter_priority:
            tasks = [t for t in tasks if t.priority == filter_priority]

        # 按优先级排序（高 > 中 > 低），未完成的在前
        priority_order = {"高": 0, "中": 1, "低": 2}
        tasks = sorted(tasks, key=lambda t: (t.completed, priority_order.get(t.priority, 1)))
        return tasks

    def get_stats(self) -> dict:
        """获取统计信息"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed

        by_priority = {"高": 0, "中": 0, "低": 0}
        for task in self.tasks:
            if not task.completed:
                by_priority[task.priority] = by_priority.get(task.priority, 0) + 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": by_priority,
        }


def print_task_list(tasks: list):
    """打印任务列表"""
    if not tasks:
        print("（没有任务）")
        return

    print(f"\n{'ID':4} {'状态':4} {'优先级':4} 标题")
    print("-" * 50)
    for task in tasks:
        status = "✅" if task.completed else "⬜"
        priority_icons = {"高": "🔴", "中": "🟡", "低": "🟢"}
        priority = priority_icons.get(task.priority, "⚪")
        due = f" [截止：{task.due_date}]" if task.due_date else ""
        print(f"[{task.id:3}] {status}  {priority}    {task.title}{due}")
        if task.description:
            print(f"         └ {task.description}")


def print_stats(stats: dict):
    """打印统计信息"""
    print(f"\n📊 统计：总计 {stats['total']} 个任务，"
          f"完成 {stats['completed']} 个，"
          f"待办 {stats['pending']} 个")
    if stats["pending"] > 0:
        p = stats["by_priority"]
        print(f"   待办优先级：🔴高={p['高']} 🟡中={p['中']} 🟢低={p['低']}")


HELP_TEXT = """
╔════════════════════════════════════╗
║       待办事项管理器               ║
╚════════════════════════════════════╝

命令列表：
  add  <标题>           添加新任务
  add  <标题> -d <描述> 添加带描述的任务
  add  <标题> -p 高|中|低  设置优先级（默认：中）
  done <ID>             标记任务为已完成
  del  <ID>             删除任务
  list                  查看所有任务
  list -p               只查看待办任务
  list -h               只查看高优先级任务
  show <ID>             查看任务详情
  stats                 查看统计信息
  help                  显示帮助
  quit                  退出
"""


def run_todo_app(storage_file=None):
    """运行待办事项应用"""
    manager = TaskManager(storage_file)
    print(HELP_TEXT)

    stats = manager.get_stats()
    if stats["total"] > 0:
        print_task_list(manager.list_tasks())
        print_stats(stats)

    while True:
        try:
            user_input = input("\n待办> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue

        parts = user_input.split()
        cmd = parts[0].lower() if parts else ""

        try:
            if cmd in ("quit", "exit", "q"):
                print("再见！")
                break

            elif cmd == "help":
                print(HELP_TEXT)

            elif cmd == "add":
                if len(parts) < 2:
                    print("用法：add <标题> [-d <描述>] [-p 高|中|低]")
                    continue

                title = parts[1]
                description = ""
                priority = "中"

                i = 2
                while i < len(parts):
                    if parts[i] == "-d" and i + 1 < len(parts):
                        description = parts[i + 1]
                        i += 2
                    elif parts[i] == "-p" and i + 1 < len(parts):
                        priority = parts[i + 1]
                        i += 2
                    else:
                        title += " " + parts[i]
                        i += 1

                task = manager.add_task(title, description, priority)
                print(f"✅ 已添加任务 #{task.id}：{task.title}")

            elif cmd in ("done", "complete"):
                if len(parts) < 2:
                    print("用法：done <任务ID>")
                    continue
                task = manager.complete_task(int(parts[1]))
                print(f"🎉 任务 #{task.id} 已完成：{task.title}")

            elif cmd in ("del", "delete", "rm"):
                if len(parts) < 2:
                    print("用法：del <任务ID>")
                    continue
                task = manager.delete_task(int(parts[1]))
                print(f"🗑️ 已删除任务 #{task.id}：{task.title}")

            elif cmd == "list":
                show_completed = True
                filter_priority = None

                if "-p" in parts:
                    show_completed = False
                if "-h" in parts:
                    filter_priority = "高"

                tasks = manager.list_tasks(show_completed, filter_priority)
                print_task_list(tasks)

            elif cmd == "show":
                if len(parts) < 2:
                    print("用法：show <任务ID>")
                    continue
                task = manager.get_task(int(parts[1]))
                print(f"\n任务详情：")
                print(f"  ID：{task.id}")
                print(f"  标题：{task.title}")
                print(f"  描述：{task.description or '（无）'}")
                print(f"  优先级：{task.priority}")
                print(f"  截止日期：{task.due_date or '（未设置）'}")
                print(f"  状态：{'已完成' if task.completed else '待办'}")
                print(f"  创建时间：{task.created_at}")
                if task.completed_at:
                    print(f"  完成时间：{task.completed_at}")

            elif cmd == "stats":
                stats = manager.get_stats()
                print_stats(stats)

            else:
                print(f"未知命令：{cmd}，输入 'help' 查看帮助")

        except ValueError as e:
            print(f"错误：{e}")
        except KeyError as e:
            print(f"错误：{e}")


def demo(storage_file=None):
    """演示模式"""
    import tempfile

    if storage_file is None:
        storage_file = os.path.join(tempfile.mkdtemp(), "demo_todo.json")

    print("=== 待办事项管理器演示 ===\n")
    manager = TaskManager(storage_file)

    # 添加任务
    manager.add_task("完成 Python 基础学习", "学习变量、循环、函数", "高")
    manager.add_task("练习面向对象编程", priority="高")
    manager.add_task("阅读 Python 文档", "官方文档很重要", "中")
    manager.add_task("做一个小项目", priority="低")
    manager.add_task("复习装饰器和生成器", priority="中")

    print("添加 5 个任务后：")
    print_task_list(manager.list_tasks())

    # 完成部分任务
    manager.complete_task(1)
    manager.complete_task(3)

    print("\n完成 2 个任务后：")
    print_task_list(manager.list_tasks())

    print("\n只看待办：")
    print_task_list(manager.list_tasks(show_completed=False))

    print_stats(manager.get_stats())

    # 清理
    import shutil
    shutil.rmtree(os.path.dirname(storage_file), ignore_errors=True)


if __name__ == "__main__":
    import sys
    import tempfile

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        if sys.stdin.isatty():
            run_todo_app()
        else:
            demo()
