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

        self.name_label = QLabel("버튼을 누르지 말아주세요", self)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name_label.move(60,30)

        self.button =QPushButton("버튼",self)
        self.button.move(80,70)
        self.button.clicked.connect(self.buttonClicked)
        # 버튼의 스타일 시트를 설정하여 배경색을 변경합니다.
        self.button.setStyleSheet("background-color: red; color: white;")

        self.button_gugu =QPushButton("구구단",self)
        self.button_gugu.move(80,110)
        self.button_gugu.clicked.connect(self.buttonClicked_2)
        # 버튼의 스타일 시트를 설정하여 배경색을 변경합니다.
        self.button_gugu.setStyleSheet("background-color: pink; color: white;")

        self.button_dev =QPushButton("미분",self)
        self.button_dev.move(80,150)
        self.button_dev.clicked.connect(self.dev_)
        # 버튼의 스타일 시트를 설정하여 배경색을 변경합니다.
        self.button_dev.setStyleSheet("background-color: skyblue; color: white;")

        self.button_diff = QPushButton("강사님 미분", self)
        self.button_diff.move(80, 200)
        self.button_diff.clicked.connect(self.buttonDiffClicked)

    def buttonClicked(self):
        """
            버튼이 눌리면 호출되는 handler
            위젯의 텍스트가 변경되면 위젯의 크기와 위치를 변경하고 이벤트에 대한 윈도우 종료
        """
        self.times_pressed += 1
        if self.times_pressed ==1:
            self.name_label.setText("폭파 2초전...")
        if self.times_pressed ==2:
            self.name_label.setText("폭파 1초전..")
            self.button.setText("STOP")
            self.button.adjustSize()
            self.button.move(80,70)
        if self.times_pressed ==3:
            print("폭파가 정지되었습니다")
            self.close()

    def buttonClicked_2(self):
        """
            버튼이 눌리면 호출되는 handler
            위젯의 텍스트가 변경되면 위젯의 크기와 위치를 변경하고 이벤트에 대한 윈도우 종료
        """
        for i in range(2,10):
            for j in range(1,10):
                print(i, "x", j ,"=", i*j )
                self.close()

    def dev_(self):
        x_num = np.array([i for i in np.arange(-10,10,0.01)])
        list_func = [lambda x: x**2+3*x+9,
                     lambda x: x**3+4*x+91,
                     lambda x: x**4+5*x+7]

        def derivative(f, x, h=0.000001):  # 미분의 정의
            return (f(x + h) - f(x)) / h

        self.times_pressed += 1
        if self.times_pressed ==1:
            numpy_derivate1 = np.array([derivative(list_func[0], x) for x in x_num])
            print('미분1' ,numpy_derivate1)
            plt.plot(x_num, numpy_derivate1)
            plt.show()
        if self.times_pressed == 2:
            numpy_derivate2 = np.array([derivative(list_func[1], x) for x in x_num])
            print('미분2' ,numpy_derivate2)
            plt.plot(x_num, numpy_derivate2)
            plt.show()
        if self.times_pressed == 3:
            numpy_derivate3 = np.array([derivative(list_func[2], x) for x in x_num])
            print('미분3' ,numpy_derivate3)
            plt.plot(x_num, numpy_derivate3)
            plt.show()
            self.close()

    def derivative(self, f, x, h=0.000001):  # 미분의 정의
        return np.array(f(x + h) - f(x)) / h

    def buttonDiffClicked(self):
        print('미분')
        x = np.arange(-10, 10, 0.01)
        for i in range(len(self.list_func)):
            if i == self.times_pressed:
                print(self.times_pressed)
                y_deri = self.derivative(self.list_func[i], x)
                print('y drivative: ', y_deri)
                plt.plot(x, self.list_func[i](x))
                plt.plot(x, y_deri)
                plt.draw()
                plt.pause(0.0001)
                plt.clf()
        self.times_pressed += 1
        if self.times_pressed == len(self.list_func): self.times_pressed = 0




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())