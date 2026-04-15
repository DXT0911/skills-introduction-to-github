#!/usr/bin/env python3
# =============================================================
# 项目3：数字猜谜游戏
# =============================================================
# 这是一个综合性项目，运用了以下知识点：
#   - 随机数生成
#   - 循环和条件语句
#   - 用户输入处理
#   - 面向对象编程
#   - 分数和排名系统
# =============================================================

import random
import time
import os
import json
from pathlib import Path


class GameConfig:
    """游戏配置"""
    DIFFICULTIES = {
        "简单": {"range": (1, 50), "max_attempts": 10, "score_multiplier": 1},
        "中等": {"range": (1, 100), "max_attempts": 7, "score_multiplier": 2},
        "困难": {"range": (1, 200), "max_attempts": 5, "score_multiplier": 4},
        "地狱": {"range": (1, 500), "max_attempts": 5, "score_multiplier": 8},
    }

    @classmethod
    def get_difficulty(cls, name: str) -> dict:
        return cls.DIFFICULTIES.get(name, cls.DIFFICULTIES["中等"])


def calculate_score(difficulty: str, attempts_used: int,
                    max_attempts: int, time_taken: float) -> int:
    """计算分数"""
    config = GameConfig.get_difficulty(difficulty)
    base_score = 1000

    # 剩余尝试次数奖励
    remaining = max_attempts - attempts_used
    attempt_bonus = remaining * 50

    # 时间奖励（60秒内完成）
    time_bonus = max(0, int((60 - time_taken) * 5))

    # 难度系数
    multiplier = config["score_multiplier"]

    return int((base_score + attempt_bonus + time_bonus) * multiplier)


def get_hint(guess: int, target: int, attempts_left: int) -> str:
    """根据猜测给出提示"""
    diff = abs(guess - target)

    direction = "太大了 📉" if guess > target else "太小了 📈"

    if attempts_left <= 1:
        # 最后一次机会给出更多提示
        if diff > 50:
            hint = f"差得很远！{direction}（差距超过50）"
        elif diff > 20:
            hint = f"还差很多！{direction}（差距约{diff}）"
        elif diff > 10:
            hint = f"接近了！{direction}（差距约{diff}）"
        else:
            hint = f"非常接近！{direction}（差距不到10）"
    else:
        if diff > 100:
            hint = f"差得很远！{direction}"
        elif diff > 50:
            hint = f"还差很多。{direction}"
        elif diff > 20:
            hint = f"越来越近了！{direction}"
        elif diff > 10:
            hint = f"已经很近了！{direction}"
        elif diff > 5:
            hint = f"非常接近！{direction}"
        else:
            hint = f"极度接近！！{direction}"

    return hint


class Leaderboard:
    """排行榜管理"""

    def __init__(self, filepath: str = None):
        if filepath is None:
            filepath = os.path.join(Path.home(), ".guess_game_scores.json")
        self.filepath = filepath
        self.scores = self._load()

    def _load(self) -> list:
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []

    def _save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def add_score(self, player: str, score: int, difficulty: str,
                  attempts: int, time_taken: float):
        """添加新分数"""
        entry = {
            "player": player,
            "score": score,
            "difficulty": difficulty,
            "attempts": attempts,
            "time": round(time_taken, 1),
            "date": time.strftime("%Y-%m-%d"),
        }
        self.scores.append(entry)
        # 按分数降序排序，保留前20名
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:20]
        self._save()

    def display(self, top_n: int = 10):
        """显示排行榜"""
        print("\n🏆 排行榜（前{}名）：".format(min(top_n, len(self.scores))))
        if not self.scores:
            print("  （暂无记录）")
            return

        print(f"  {'排名':4} {'玩家':10} {'分数':7} {'难度':6} {'尝试':4} {'时间':6} {'日期'}")
        print("  " + "-" * 55)

        for i, entry in enumerate(self.scores[:top_n], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}"
            print(f"  {medal:4} {entry['player']:10} {entry['score']:7} "
                  f"{entry['difficulty']:6} {entry['attempts']:4} "
                  f"{entry['time']:5.1f}s {entry['date']}")


class GuessGame:
    """猜数字游戏主类"""

    def __init__(self, storage_file=None):
        self.leaderboard = Leaderboard(storage_file)
        self.player_name = None

    def get_player_name(self) -> str:
        """获取玩家名称"""
        while True:
            name = input("请输入你的昵称（2-10个字符）：").strip()
            if 2 <= len(name) <= 10:
                return name
            print("昵称长度需在 2-10 个字符之间，请重新输入")

    def choose_difficulty(self) -> str:
        """选择难度"""
        difficulties = list(GameConfig.DIFFICULTIES.keys())
        print("\n选择难度：")
        for i, diff in enumerate(difficulties, 1):
            config = GameConfig.get_difficulty(diff)
            r = config["range"]
            attempts = config["max_attempts"]
            mult = config["score_multiplier"]
            print(f"  {i}. {diff:4} | 范围：{r[0]}-{r[1]:3} | "
                  f"最多 {attempts} 次 | 分数系数 ×{mult}")

        while True:
            try:
                choice = input(f"\n请选择难度（1-{len(difficulties)}）：").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(difficulties):
                    return difficulties[idx]
            except (ValueError, IndexError):
                pass
            print(f"请输入 1 到 {len(difficulties)} 之间的数字")

    def play_round(self, difficulty: str) -> dict:
        """进行一轮游戏，返回结果"""
        config = GameConfig.get_difficulty(difficulty)
        min_val, max_val = config["range"]
        max_attempts = config["max_attempts"]

        target = random.randint(min_val, max_val)
        attempts = 0
        start_time = time.time()
        guess_history = []

        print(f"\n🎯 猜一个 {min_val} 到 {max_val} 之间的整数")
        print(f"⚠️ 你有 {max_attempts} 次机会\n")

        while attempts < max_attempts:
            attempts_left = max_attempts - attempts
            print(f"（剩余 {attempts_left} 次机会）", end=" ")

            try:
                user_input = input("你的猜测：").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n游戏中断")
                return None

            if user_input.lower() in ("quit", "exit", "q"):
                print("已放弃本局")
                return None

            try:
                guess = int(user_input)
            except ValueError:
                print("请输入整数！")
                continue

            if not (min_val <= guess <= max_val):
                print(f"请输入 {min_val} 到 {max_val} 之间的数字！")
                continue

            attempts += 1
            guess_history.append(guess)

            if guess == target:
                elapsed = time.time() - start_time
                score = calculate_score(difficulty, attempts, max_attempts, elapsed)
                print(f"\n🎉 恭喜你猜对了！答案就是 {target}")
                print(f"⏱️ 用时 {elapsed:.1f} 秒")
                print(f"🎯 你用了 {attempts} 次猜到的")
                print(f"💯 本局得分：{score}")
                return {
                    "success": True,
                    "target": target,
                    "attempts": attempts,
                    "time": elapsed,
                    "score": score,
                    "history": guess_history,
                }
            else:
                hint = get_hint(guess, target, attempts_left - 1)
                print(f"  {hint}")

        # 用完所有机会
        elapsed = time.time() - start_time
        print(f"\n😞 很遗憾，次数用完了！答案是 {target}")
        print(f"你的猜测历史：{guess_history}")
        return {
            "success": False,
            "target": target,
            "attempts": attempts,
            "time": elapsed,
            "score": 0,
            "history": guess_history,
        }

    def run(self):
        """运行游戏"""
        print("╔════════════════════════════════╗")
        print("║        数字猜谜游戏            ║")
        print("╚════════════════════════════════╝")

        self.player_name = self.get_player_name()
        print(f"\n欢迎，{self.player_name}！🎮")

        session_scores = []

        while True:
            print("\n" + "=" * 40)
            print("1. 开始游戏")
            print("2. 查看排行榜")
            print("3. 退出")
            print("=" * 40)

            try:
                choice = input("选择（1-3）：").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见！")
                break

            if choice == "1":
                difficulty = self.choose_difficulty()
                result = self.play_round(difficulty)

                if result is not None:
                    if result["success"]:
                        self.leaderboard.add_score(
                            self.player_name,
                            result["score"],
                            difficulty,
                            result["attempts"],
                            result["time"],
                        )
                        session_scores.append(result["score"])

            elif choice == "2":
                self.leaderboard.display()

            elif choice == "3":
                if session_scores:
                    print(f"\n本次游戏统计：")
                    print(f"  游玩了 {len(session_scores)} 局（成功）")
                    print(f"  最高分：{max(session_scores)}")
                    print(f"  总分：{sum(session_scores)}")
                print("感谢游玩，再见！👋")
                break

            else:
                print("无效选择，请输入 1、2 或 3")


def demo():
    """演示模式（不需要用户输入）"""
    print("=== 数字猜谜游戏演示 ===\n")

    # 模拟一局游戏
    random.seed(42)
    difficulty = "中等"
    config = GameConfig.get_difficulty(difficulty)
    min_val, max_val = config["range"]
    max_attempts = config["max_attempts"]
    target = random.randint(min_val, max_val)

    print(f"难度：{difficulty}，范围：{min_val}-{max_val}，最多{max_attempts}次")
    print(f"（演示中：目标数字是 {target}）\n")

    # 模拟二分查找策略猜测
    low, high = min_val, max_val
    attempts = 0
    start_time = time.time()

    while low <= high and attempts < max_attempts:
        guess = (low + high) // 2
        attempts += 1
        print(f"第{attempts}次猜测：{guess}", end=" → ")

        if guess == target:
            elapsed = time.time() - start_time
            score = calculate_score(difficulty, attempts, max_attempts, elapsed)
            print(f"✅ 猜对了！")
            print(f"\n🎉 用 {attempts} 次猜到 {target}，得分 {score}")
            break
        elif guess < target:
            print(get_hint(guess, target, max_attempts - attempts))
            low = guess + 1
        else:
            print(get_hint(guess, target, max_attempts - attempts))
            high = guess - 1

    # 显示分数计算说明
    print("\n--- 分数说明 ---")
    for diff_name, conf in GameConfig.DIFFICULTIES.items():
        r = conf["range"]
        print(f"  {diff_name}：{r[0]}-{r[1]}，×{conf['score_multiplier']} 倍系数")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        if sys.stdin.isatty():
            game = GuessGame()
            game.run()
        else:
            demo()
