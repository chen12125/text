# 推箱子关卡数据
# 符号说明:
# # - 墙
# @ - 玩家
# $ - 箱子
# . - 目标位置
# * - 箱子在目标位置上
# + - 玩家在目标位置上
#   - 空地

LEVELS = [
    # 第 1 关 - 教学关
    [
        "  ##### ",
        "###   # ",
        "#.@$  # ",
        "### $.# ",
        "  ##### ",
    ],
    
    # 第 2 关
    [
        "  ####  ",
        "###  ####",
        "#     $ #",
        "# #  #$ #",
        "# . .#@ #",
        "#########",
    ],
    
    # 第 3 关
    [
        "#####   ",
        "#   # ###",
        "#@  # $ #",
        "### . $ #",
        "  # .  ##",
        "  #  ##  ",
        "  ####   ",
    ],
    
    # 第 4 关
    [
        "    #### ",
        "    #  # ",
        "#####  # ",
        "#    $ # ",
        "# #$@ .# ",
        "##### .# ",
        "    #### ",
    ],
    
    # 第 5 关 - 经典关卡
    [
        "  ####  ",
        "  #  #  ",
        "###  $##",
        "#  $ $ #",
        "# .# @ #",
        "## . .##",
        "  ####  ",
    ],
]


def parse_level(level_index):
    """解析关卡数据，返回游戏状态"""
    if level_index < 0 or level_index >= len(LEVELS):
        return None
    
    level = LEVELS[level_index]
    player_pos = None
    boxes = []
    targets = []
    walls = []
    
    for row_idx, row in enumerate(level):
        for col_idx, cell in enumerate(row):
            pos = (col_idx, row_idx)
            if cell == '#':
                walls.append(pos)
            elif cell == '@':
                player_pos = pos
            elif cell == '$':
                boxes.append(pos)
            elif cell == '.':
                targets.append(pos)
            elif cell == '*':  # 箱子在目标上
                boxes.append(pos)
                targets.append(pos)
            elif cell == '+':  # 玩家在目标上
                player_pos = pos
                targets.append(pos)
    
    return {
        'player': player_pos,
        'boxes': boxes,
        'targets': targets,
        'walls': walls,
        'level': level,
    }


def get_level_count():
    return len(LEVELS)
