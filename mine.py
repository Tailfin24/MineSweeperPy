'''
mine.py
地雷格子的实现
'''

from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtCore import (pyqtSignal, QSize, Qt)

from gui import Mine_GUI


class Mine(QWidget, Mine_GUI):
    expand = pyqtSignal(int, int)  # 表示扩展
    clicked = pyqtSignal()  # 表示是否按下
    gameover = pyqtSignal()  # 表示游戏结束
    win = pyqtSignal()  # 胜利的判定

    def __init__(self, x, y):
        super().__init__()

        self.setFixedSize(QSize(20, 20))
        self.x = x
        self.y = y
        self.is_begin = False  # 是否是初始点
        self.is_mine = False  # 是否是地雷
        self.nums = 0  # 周围的地雷数
        self.is_display = False  # 是否显示
        self.is_flag = False  # 是否插旗

        self.update()

    def click(self):
        ''' 点击事件 '''
        if not self.is_display:
            self.display()  # 显示
            if self.nums == 0:
                self.expand.emit(self.x, self.y)

        self.clicked.emit()  # 释放所有按键

    def flag(self):
        ''' 为空格标上旗子 '''
        self.is_flag = True
        self.update()
        self.clicked.emit()

    def unflag(self):
        ''' 去除旗子 '''
        self.is_flag = False
        self.update()
        self.clicked.emit()

    def display(self):
        ''' 显示该格 '''
        self.is_display = True
        self.update()

    def reset(self):
        ''' 重新设置 '''
        self.is_begin = False 
        self.is_mine = False
        self.nums = 0 
        self.is_display = False
        self.is_flag = False

        self.update()

    def mouseReleaseEvent(self, mouse):
        ''' 鼠标事件 '''
        # 判断右键
        if mouse.button() == Qt.RightButton and (not self.is_display):
            if not self.is_flag:
                self.flag()
            else:
                self.unflag()

        # 判断左键
        elif mouse.button() == Qt.LeftButton and (not self.is_flag):
            self.click()

            # 按下后判断游戏有没有胜利
            self.win.emit()

            # 如果这个格子是雷， 触发游戏结束事件
            if self.is_mine:
                self.gameover.emit()
