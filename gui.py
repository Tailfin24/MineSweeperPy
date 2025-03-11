'''
gui.py
生成 GUI
'''

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QMainWindow, QToolTip,
                             qApp, QDesktopWidget, QLCDNumber)
from PyQt5.QtCore import (Qt, QTimer, QSize)
from PyQt5.QtGui import (QIcon, QPixmap, QPainter, QPalette, QBrush, 
                         QPen, QFont)


from constant import (IMG_BOMB, IMG_CLOCK, IMG_FLAG, ST_READY, ST_ICON, 
                      COLOR_OF_NUM)


class Minesweeper_GUI():
    def __init__(self):
        self.init_UI()
    
    def init_UI(self):
        '''
        初始化 UI
        '''
        w = QWidget()  # 创建一个窗口

        information_UI = self.init_information_UI()  # 创建信息板
        self.init_map_UI()  # 初始化地图

        # 将信息板和地图的 UI 都加入到一个垂直排列中，UI 制作完成
        vbox = QVBoxLayout()
        vbox.addLayout(information_UI)
        vbox.addLayout(self.grid)
        
        # 将 UI 加入到窗口中
        w.setLayout(vbox)
        self.setCentralWidget(w)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)   

        # 设置标题和图标
        self.setWindowTitle('MineSweeper')
        self.setWindowIcon(QIcon("./img/bomb.png"))  

    def init_information_UI(self):
        '''
        初始化信息板的 UI
        '''
        hbox = QHBoxLayout()  # 设置一个横向的盒排列

        # 设置炸弹数标识       
        self.mines = QLCDNumber(3, self)  # 地雷图标
        self.mines.display("%03d" % self.num_of_mines)
        mine_sign = QLabel()
        mine_sign.setPixmap(QPixmap.fromImage(IMG_BOMB))
        mine_sign.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 设置计时器
        self.clock = QLCDNumber(3, self)  # 时间图标
        self.mines.display("000")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)  # 将计时器与函数 update_time 绑定
        self.timer.start(1000)  # 计时间隔为 1 秒
        
        clock_sign = QLabel()
        clock_sign.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        clock_sign.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 设置重置按钮
        self.button_reset = QPushButton()
        self.button_reset.setFixedSize(QSize(32, 32))
        self.button_reset.setIconSize(QSize(32, 32))
        self.button_reset.setIcon(QIcon(ST_ICON[ST_READY]))
        self.button_reset.setFlat(True)
        self.button_reset.pressed.connect(self.button_reset_perssed) 

        # 按照顺序依次加入 hbox 中
        hbox.addWidget(self.mines)
        hbox.addWidget(mine_sign)
        hbox.addWidget(self.button_reset)
        hbox.addWidget(clock_sign)
        hbox.addWidget(self.clock)

        return hbox

    def init_map_UI(self):
        '''
        初始化地图 UI
        '''
        # 初始化地图格子
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

    def update_st(self, st):
        '''
        更新游戏状态
        '''
        self.st = st
        self.button_reset.setIcon(QIcon(ST_ICON[self.st]))


class Mine_GUI():
    def paintEvent(self, event):
        ''' 绘制事件 '''
        # 初始化画笔
        paint = QPainter(self)
        paint.setRenderHint(QPainter.Antialiasing)

        # 在主窗口上绘制
        rect = event.rect()

        # 设定颜色
        if self.is_display:
            
            color = self.palette().color(QPalette.Background)
            line_color, inner_color = color, color
        else:

            line_color, inner_color = Qt.gray, Qt.lightGray

        # 绘制格子
        paint.fillRect(rect, QBrush(inner_color))
        pen = QPen(line_color)
        pen.setWidth(1)
        paint.setPen(pen)
        paint.drawRect(rect)

        if self.is_display:
            if self.is_mine:
                paint.drawPixmap(rect, QPixmap(IMG_BOMB))
            elif self.nums > 0:
                # 读取数字对应的颜色
                pen = QPen(COLOR_OF_NUM[self.nums])
                paint.setPen(pen)
                font = paint.font()
                font.setBold(True)
                paint.setFont(font)
                # 在正中央绘制数字
                paint.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter,
                               str(self.nums))

        if self.is_flag:
            paint.drawPixmap(rect, QPixmap(IMG_FLAG))


class LevelSelect(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 220)
        self.setWindowTitle('选择难度')
        self.setWindowIcon(QIcon("./img/bomb.png"))
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())        

        QToolTip.setFont(QFont('SansSerif', 10))
        btn1 = QPushButton('简单', self)
        btn1.setToolTip('<b>简单难度</b>：8*8，10个雷')
        btn1.resize(btn1.sizeHint())
        btn1.move(85, 50)
        btn1.clicked.connect(lambda: self.change_level(0))

        btn2 = QPushButton('普通', self)
        btn2.setToolTip('<b>普通难度</b>：16*16，40个雷')
        btn2.resize(btn2.sizeHint())        
        btn2.move(85, 100)
        btn2.clicked.connect(lambda: self.change_level(1))

        btn3 = QPushButton('困难', self)
        btn3.setToolTip('<b>困难难度</b>：16*30，99个雷')
        btn3.resize(btn3.sizeHint())
        btn3.move(85, 150)
        btn3.clicked.connect(lambda: self.change_level(2))

        self.show()

    def change_level(self, dif):
        qApp.exit(dif)
