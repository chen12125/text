# Sokoban - 推箱子游戏 🎮

经典推箱子游戏的 Python 实现，使用 Pygame。

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 操作

- **方向键** 或 **WASD**: 移动玩家
- **R**: 重置当前关卡
- **N**: 下一关
- **P**: 上一关
- **ESC**: 退出游戏

## 游戏规则

- 玩家 (🟦) 需要把所有箱子 (🟫) 推到目标位置 (🟩)
- 箱子只能被推动，不能被拉动
- 一次只能推动一个箱子
- 把所有箱子推到目标位置即可过关

## 部署到 GitHub

```bash
# 首次配置（在 GitHub 创建仓库后）
git remote add origin https://github.com/你的用户名/sokoban-game.git

# 一键推送
./deploy.sh
```

## 文件结构

```
sokoban-game/
├── main.py          # 游戏入口
├── game.py          # 游戏逻辑
├── levels.py        # 关卡数据
├── deploy.sh        # 一键推送脚本
├── requirements.txt # 依赖
└── README.md        # 说明文档
```
