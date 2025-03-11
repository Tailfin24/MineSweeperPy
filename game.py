'''
game.py
游戏主体内容的实现
'''

from PyQt5.QtWidgets import (QMainWindow)

from constant import (DIFFICULTY, ST_READY, ST_GAMING, ST_LOSE, ST_WIN,
                      )
from gui import Minesweeper_GUI
from mine import Mine
import random
import time


class Minesweeper(QMainWindow, Minesweeper_GUI):
    
    def __init__(self, curr_difficulty, parent=None):
        self.b_row, self.b_col, self.num_of_mines = DIFFICULTY[curr_difficulty]
        super().__init__()
        self.init_game()

    def init_game(self):
        ''' 
        初始化游戏 
        '''
        
        self.update_st(ST_READY)  # 准备开始
        self.init_map()  # 初始化地图
        self.reset_map()  # 重置地图

        self.show()  # 显示窗口

    def init_map(self):
        '''
        初始化地图
        '''
        for x in range(0, self.b_row):
            for y in range(0, self.b_col):
                # 创建一个地雷对象
                mine = Mine(x, y)
                self.grid.addWidget(mine, y, x)
                # 将地雷对象中的信号与槽绑定
                mine.clicked.connect(self.start_game)  # 按下第一个格子开始游戏
                mine.expand.connect(self.display_expand)  # 发出扩张信号扩张格子
                mine.gameover.connect(self.game_over)  # 触发地雷游戏结束
                mine.win.connect(self.game_win)  # 每次点击后判断是否胜利

    def reset_map(self):
        # 重置地图
        for x in range(0, self.b_row):
            for y in range(0, self.b_col):
                mine = self.grid.itemAtPosition(y, x).widget()
                mine.reset()

        # 添加地雷
        positions = []
        while len(positions) < self.num_of_mines:
            x = random.randint(0, self.b_row - 1)
            y = random.randint(0, self.b_col - 1)
            if (x, y) not in positions:
                mine = self.grid.itemAtPosition(y, x).widget()
                mine.is_mine = True
                positions.append((x, y))
        
        # 添加周围有多少雷的信息
        def get_num_of_mines(x, y):
            pos = self.get_surround(x, y)
            num_of_mines = sum(1 if mine.is_mine else 0 for mine in pos)

            return num_of_mines
        
        for x in range(0, self.b_row):
            for y in range(0, self.b_col):
                mine = self.grid.itemAtPosition(y, x).widget()
                mine.nums = get_num_of_mines(x, y)

        # 设定开始位置
        times = 0
        while True:
            x = random.randint(1, self.b_row - 2)
            y = random.randint(1, self.b_col - 2)
            if (x, y) not in positions:
                mine = self.grid.itemAtPosition(y, x).widget()
                if mine.nums == 0 or times >= 15:
                    mine.is_begin = True

                    for w in self.get_surround(x, y):
                        if not mine.is_mine:
                            mine.click()
                    break
                times += 1

    def get_surround(self, x, y):
        '''
        获取一个格子周边的格子
        '''
        pos = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_row)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_col)):
                pos.append(self.grid.itemAtPosition(yi, xi).widget())
        return pos

    def display_map(self):
        '''
        失败时展示整个地图
        '''
        for x in range(0, self.b_row):
            for y in range(0, self.b_col):
                mine = self.grid.itemAtPosition(y, x).widget()
                mine.display()

    def display_expand(self, x, y):
        '''
        一个格子被点开，其周边格子中周围地雷数为 0 的格子也要点开
        '''
        for xi in range(max(0, x - 1), min(x + 2, self.b_row)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_col)):
                mine = self.grid.itemAtPosition(yi, xi).widget()
                if not mine.is_mine:
                    mine.click()
    
    def button_reset_perssed(self):
        if self.st == ST_GAMING:
            self.update_st(ST_LOSE)
            self.display_map()

        elif self.st == ST_LOSE or self.st == ST_WIN:
            self.update_st(ST_READY)
            self.reset_map()

    def start_game(self):
        '''
        点击第一个格子后，开始计时
        '''
        if self.st == ST_READY:  # 如果不在游戏中
            self.update_st(ST_GAMING)  # 变成游戏中状态
            self.time_start = int(time.time())  # 获取开始游戏的时间

    def update_time(self):
        if self.st == ST_GAMING:
            game_time = int(time.time()) - self.time_start  # 获取游戏时间
            self.clock.display("%03d" % game_time)  # 将游戏时间绑定到clock组件上
    
    def game_over(self):
        if self.st == ST_GAMING:
            self.display_map()
            self.update_st(ST_LOSE)

    def is_win(self):
        for x in range(0, self.b_row):
            for y in range(0, self.b_col):
                mine = self.grid.itemAtPosition(y, x).widget()
                if (not mine.is_mine) and (not mine.is_display):
                    return False
        return True

    def game_win(self):
        if self.is_win() and self.st == ST_GAMING:
            self.display_map()
            self.update_st(ST_WIN)
