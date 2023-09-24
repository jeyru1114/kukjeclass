import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QPushButton,QCheckBox,QDesktopWidget)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np

class CheckBoxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.list_func = [lambda x:x**2, lambda x:x**3,lambda x:x**4]


    def derivative(self,f,x,h=1e-5):
        return np.array((f(x-h)-f(x))/h)

    def initializeUI(self):
        self.setGeometry(100, 100, 250, 250)
        self.setWindowTitle("QPushButton")
        self.center()
        self.displayCheckBoxes()
        self.show()
    def center(self): #화면 가운데로 창이 생성되게하는 함수

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def displayCheckBoxes(self):
        self.cnt_ = 0
        self.header_label = QLabel(self)
        self.header_label.setText("직업의 선호하는 것은? 모두 선택하세요.")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setWordWrap(True)
        self.header_label.resize(230,60)
        #morning_cb.toggle() # check가 해제된 상태로 시작하려면 주석해제


        morning_cb = QCheckBox("아침 8시부터 오후 2시까지",self)# 부모에 text 전달
        morning_cb.move(20,80)
        morning_cb.stateChanged.connect(self.printToTerminal)


        font = morning_cb.font()  # 현재 폰트 가져오기
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        morning_cb.setFont(font)  # 새로운 폰트로 설정
        morning_cb.setStyleSheet("color: red;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: #FA8072;"
                      "border-radius: 3px")

        after_cb = QCheckBox("오후 1시부터 8시까지",self)
        font = after_cb.font()  # 현재 폰트 가져오기
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        after_cb.setFont(font)  # 새로운 폰트로 설정
        after_cb.move(20,100)
        after_cb.stateChanged.connect(self.printToTerminal1)

        after_cb.setStyleSheet("color: green;"
                                "background-color: #7FFFD4")
        night_cb = QCheckBox("밤 7시부터 새벽 3시까지",self)
        font = night_cb.font()  # 현재 폰트 가져오기
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        night_cb.setFont(font)  # 새로운 폰트로 설정
        night_cb.move(20,120)
        night_cb.stateChanged.connect(self.printToTerminal2)

        night_cb.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;"
                               "border-style: dashed;"
                               "border-width: 3px;"
                               "border-color: #1E90FF")

    def printToTerminal(self):
        self.cnt_ += 1
        if self.cnt_ == 1:
            x = np.arange(-10, 10, 0.01)
            plt.plot(x, self.list_func[0](x))
            diff = self.derivative(self.list_func[0],x)
            plt.plot(x,diff, 'r')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        if self.cnt_ >= 2:
            self.cnt_ = 0
            plt.close()

    def printToTerminal1(self):
        self.cnt_ += 2
        if self.cnt_ == 2:
            x = np.arange(-10, 10, 0.01)
            plt.plot(x, self.list_func[1](x))
            diff = self.derivative(self.list_func[1], x)
            plt.plot(x, diff, 'g')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        if self.cnt_ >= 3:
            self.cnt_=0
            plt.close()

    def printToTerminal2(self):
        self.cnt_ += 3
        if self.cnt_ == 3:
            x = np.arange(-10, 10, 0.01)
            plt.plot(x, self.list_func[2](x))
            diff = self.derivative(self.list_func[2], x)
            plt.plot(x, diff, 'y')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        if self.cnt_ >= 4:
            self.cnt_=0
            plt.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window =   CheckBoxWindow()
    sys.exit(app.exec())

