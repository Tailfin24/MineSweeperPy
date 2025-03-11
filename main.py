'''
main.py
游戏开始的入口
'''

from gui import LevelSelect
from PyQt5.QtWidgets import QApplication
from game import Minesweeper
import sys

if __name__ == '__main__': 

    app = QApplication(sys.argv)
    levelselect = LevelSelect()
    difficulty = app.exec_()
    del levelselect
    minesweeper = Minesweeper(difficulty)
    sys.exit(app.exec_())
