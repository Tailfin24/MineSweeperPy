'''
constant.py
存放游戏中用到的资源与常量，方便调用
'''

from PyQt5.QtGui import (QImage, QColor)

# 游戏状态
ST_READY = 0
ST_GAMING = 1
ST_LOSE = 2
ST_WIN = 3


# 难度设定
DIFFICULTY = [
    (8, 8, 10),  # 8*8 10个雷
    (16, 16, 40),  # 16*16 40个雷
    (30, 16, 99)  # 16*30 99个雷
]

# 载入图像文件
IMG_BOMB = QImage("./img/bomb.png")
IMG_FLAG = QImage("./img/flag.png")
IMG_CLOCK = QImage("./img/clock.png")

ST_ICON = {
    ST_READY: "./img/ready.png",
    ST_GAMING: "./img/smile.png",
    ST_LOSE: "./img/cry.png",
    ST_WIN: "./img/lol.png"
}

# 数字的颜色
COLOR_OF_NUM = {
    1: QColor('#0000ff'),  # 蓝色
    2: QColor('#274e13'),  # 绿色
    3: QColor('#ff0000'),  # 红色 
    4: QColor('#20124d'),  # 深蓝色
    5: QColor('#660000'),  # 棕色
    6: QColor('#32a788'),  # 青色
    7: QColor('#000000'),  # 黑色
    8: QColor('#666666')  # 灰色
}
