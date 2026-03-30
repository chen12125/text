#!/usr/bin/env python3
"""
Sokoban - 推箱子游戏
经典益智游戏 Python 实现
"""

from game import SokobanGame


def main():
    print("🎮 Sokoban - 推箱子游戏")
    print("=" * 40)
    print("操作说明:")
    print("  方向键/WASD - 移动玩家")
    print("  R - 重置当前关卡")
    print("  N - 下一关 (通关后)")
    print("  P - 上一关")
    print("  D - 开发者的话")
    print("  S - 游戏统计")
    print("  ESC - 退出游戏")
    print("=" * 40)
    print("正在启动游戏...")
    
    game = SokobanGame()
    game.run()


if __name__ == '__main__':
    main()
