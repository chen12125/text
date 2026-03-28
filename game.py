import pygame
from levels import parse_level, get_level_count


class SokobanGame:
    def __init__(self):
        pygame.init()
        self.cell_size = 50
        self.screen = None
        self.clock = None
        self.current_level = 0
        self.reset_game()
        
        # 颜色定义
        self.colors = {
            'floor': (240, 240, 240),
            'wall': (100, 100, 100),
            'target': (100, 200, 100),
            'player': (50, 100, 200),
            'box': (180, 140, 100),
            'box_on_target': (100, 180, 100),
            'text': (50, 50, 50),
            'developer_bg': (200, 220, 255),  # 开发者话语背景
            'developer_border': (100, 150, 200),  # 开发者话语边框
            'developer_text': (30, 30, 100),  # 开发者话语文字
        }
        
        # 开发者的话
        self.show_developer_message = False
        self.developer_message = [
            "👨‍💻 开发者的话",
            "",
            "欢迎体验推箱子游戏!",
            "",
            "这个游戏是我用心制作的",
            "希望能给你带来快乐和挑战。",
            "",
            "关卡设计经过精心安排，",
            "每一关都有独特的解法思路。",
            "",
            "推箱子不仅是游戏，",
            "更是锻炼逻辑思维的好方式。",
            "",
            "感谢你的游玩！",
            "祝你玩得开心！😊",
            "",
            "—— 陈召"
        ]
    
    def reset_game(self):
        """重置游戏到第一关"""
        self.current_level = 0
        self.load_level(0)
    
    def load_level(self, level_index):
        """加载指定关卡"""
        level_data = parse_level(level_index)
        if level_data is None:
            return False
        
        self.level_data = level_data
        self.player_pos = level_data['player']
        self.boxes = set(level_data['boxes'])
        self.targets = set(level_data['targets'])
        self.walls = set(level_data['walls'])
        self.level = level_data['level']
        
        # 计算地图尺寸并初始化屏幕
        max_width = max(len(row) for row in self.level)
        max_height = len(self.level)
        self.width = max_width * self.cell_size
        self.height = max_height * self.cell_size
        
        if self.screen is None:
            self.screen = pygame.display.set_mode((self.width, self.height + 40))
            pygame.display.set_caption('Sokoban - 推箱子')
            self.clock = pygame.time.Clock()
        
        return True
    
    def move_player(self, dx, dy):
        """移动玩家"""
        new_pos = (self.player_pos[0] + dx, self.player_pos[1] + dy)
        
        # 检查是否撞墙
        if new_pos in self.walls:
            return False
        
        # 检查是否碰到箱子
        if new_pos in self.boxes:
            # 尝试推动箱子
            box_new_pos = (new_pos[0] + dx, new_pos[1] + dy)
            if box_new_pos in self.walls or box_new_pos in self.boxes:
                return False  # 推不动
            
            # 移动箱子
            self.boxes.remove(new_pos)
            self.boxes.add(box_new_pos)
        
        # 移动玩家
        self.player_pos = new_pos
        return True
    
    def check_win(self):
        """检查是否获胜"""
        return self.boxes == self.targets
    
    def reset_level(self):
        """重置当前关卡"""
        self.load_level(self.current_level)
    
    def next_level(self):
        """进入下一关"""
        if self.current_level < get_level_count() - 1:
            self.current_level += 1
            return self.load_level(self.current_level)
        return False
    
    def prev_level(self):
        """返回上一关"""
        if self.current_level > 0:
            self.current_level -= 1
            return self.load_level(self.current_level)
        return False
    
    def toggle_developer_message(self):
        """切换开发者的话显示/隐藏"""
        self.show_developer_message = not self.show_developer_message
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(self.colors['floor'])
        
        # 绘制目标位置
        for target in self.targets:
            rect = pygame.Rect(
                target[0] * self.cell_size,
                target[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.colors['target'], rect)
            # 绘制目标标记 (X)
            margin = self.cell_size // 4
            pygame.draw.line(self.screen, (50, 150, 50),
                           (rect.left + margin, rect.top + margin),
                           (rect.right - margin, rect.bottom - margin), 3)
            pygame.draw.line(self.screen, (50, 150, 50),
                           (rect.right - margin, rect.top + margin),
                           (rect.left + margin, rect.bottom - margin), 3)
        
        # 绘制箱子
        for box in self.boxes:
            rect = pygame.Rect(
                box[0] * self.cell_size + 5,
                box[1] * self.cell_size + 5,
                self.cell_size - 10,
                self.cell_size - 10
            )
            color = self.colors['box_on_target'] if box in self.targets else self.colors['box']
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
        
        # 绘制墙壁
        for wall in self.walls:
            rect = pygame.Rect(
                wall[0] * self.cell_size,
                wall[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, self.colors['wall'], rect)
        
        # 绘制玩家
        player_rect = pygame.Rect(
            self.player_pos[0] * self.cell_size + 10,
            self.player_pos[1] * self.cell_size + 10,
            self.cell_size - 20,
            self.cell_size - 20
        )
        pygame.draw.circle(self.screen, self.colors['player'],
                          player_rect.center, (self.cell_size - 20) // 2)
        
        # 绘制关卡信息
        font = pygame.font.Font(None, 28)
        level_text = f"Level: {self.current_level + 1}/{get_level_count()}"
        text_surface = font.render(level_text, True, self.colors['text'])
        self.screen.blit(text_surface, (10, self.height + 8))
        
        # 绘制提示
        hint_text = "Arrow Keys: Move | R: Reset | N: Next | P: Prev | D: Dev Message | ESC: Quit"
        hint_surface = font.render(hint_text, True, self.colors['text'])
        self.screen.blit(hint_surface, (self.width - hint_surface.get_width() - 10, self.height + 8))
        
        # 绘制胜利信息
        if self.check_win():
            win_font = pygame.font.Font(None, 48)
            win_text = "🎉 Level Complete! Press N for next level"
            win_surface = win_font.render(win_text, True, (50, 150, 50))
            win_rect = win_surface.get_rect(center=(self.width // 2, self.height // 2))
            pygame.draw.rect(self.screen, (255, 255, 255), win_rect.inflate(20, 20))
            pygame.draw.rect(self.screen, (50, 150, 50), win_rect.inflate(20, 20), 3)
            self.screen.blit(win_surface, win_rect)
        
        # 如果需要显示开发者的话
        if self.show_developer_message:
            self.draw_developer_message()
        
        pygame.display.flip()
    
    def draw_developer_message(self):
        """绘制开发者的话"""
        # 创建半透明覆盖层
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)  # 半透明度
        overlay.fill((0, 0, 0))  # 黑色背景
        self.screen.blit(overlay, (0, 0))
        
        # 计算消息框尺寸
        margin = 30
        padding = 20
        line_height = 30
        
        box_width = max([len(line.encode('utf-8')) * 12 for line in self.developer_message]) + padding * 2
        box_width = max(box_width, 400)  # 最小宽度
        box_height = len(self.developer_message) * line_height + padding * 2
        
        # 居中计算位置
        box_x = (self.width - box_width) // 2
        box_y = (self.height - box_height) // 2
        
        # 绘制消息框背景
        bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, self.colors['developer_bg'], bg_rect)
        pygame.draw.rect(self.screen, self.colors['developer_border'], bg_rect, 3)
        
        # 绘制标题
        title_font = pygame.font.Font(None, 36)
        title_surface = title_font.render("👨‍💻 开发者的话", True, self.colors['developer_text'])
        title_rect = title_surface.get_rect()
        title_rect.midtop = (self.width // 2, box_y + padding // 2)
        self.screen.blit(title_surface, title_rect)
        
        # 绘制消息内容
        font = pygame.font.Font(None, 28)
        for i, line in enumerate(self.developer_message[1:]):  # 跳过标题
            if line.strip():  # 非空行
                text_surface = font.render(line, True, self.colors['developer_text'])
            else:  # 空行
                text_surface = font.render("", True, self.colors['developer_text'])
            
            text_rect = text_surface.get_rect()
            text_rect.midtop = (self.width // 2, box_y + padding + 30 + i * line_height)
            self.screen.blit(text_surface, text_rect)
        
        # 绘制关闭提示
        hint_font = pygame.font.Font(None, 24)
        hint_surface = hint_font.render("按 D 键关闭", True, self.colors['developer_text'])
        hint_rect = hint_surface.get_rect()
        hint_rect.midbottom = (self.width // 2, box_y + box_height - 10)
        self.screen.blit(hint_surface, hint_rect)
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.move_player(0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.move_player(0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.move_player(-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.move_player(1, 0)
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key == pygame.K_n:
                        if self.check_win():
                            self.next_level()
                    elif event.key == pygame.K_p:
                        self.prev_level()
                    elif event.key == pygame.K_d:
                        self.toggle_developer_message()
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
