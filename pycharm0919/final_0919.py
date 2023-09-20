import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import numpy as np
import sympy
import matplotlib.pyplot as plt

class MainWindow(QWidget):

    def f1(self, x): return x ** 2 + 3 * x + 9

    def f2(self, x): return x ** 3 + 4 * x + 91

    def f3(self, x): return x**4+4*x+91 + np.log(np.abs(x)+0.05)

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.list_func=[self.f1, lambda x: x**4+4*x**3 +12*x, self.f2, self.f3]
        self.love_list=["사","랑","해"]

    def initializeUI(self):
        """
            어플리케이션 UI 설정
        """
        self.setGeometry(100,100,300,300)
        self.setWindowTitle("QPushButton 예제")

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """
            메인 윈도우에 위젯을 생성후 배치
        """
        self.times_pressed=0
        self.button = QPushButton("♥",self)
        self.button.move(100,100)
        self.button.clicked.connect(self.f)
        self.button.setStyleSheet("background-color: pink; color: red;")

    def f(self):
        print("하트",self.times_pressed)
        self.times_pressed += 1
        if self.times_pressed == len(self.list_func): self.times_pressed=0
        x = np.arange(-10, 10, 0.01)
        plt.plot(x,self.list_func[self.times_pressed](x))
        plt.draw()
        plt.show()
        plt.pause(0.0001)
        plt.clf()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())