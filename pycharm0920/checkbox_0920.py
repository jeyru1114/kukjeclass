import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QCheckBox)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np


class CheckBoxWindow(QWidget):
    def derivative(self,f,x,h=1e-5):
        return np.array((f(x+h)-f(x))/h)

# check box를 이용하여 그래프 그리기, 1번 = list_func[0] 함수호출하여 결과 그래프 그리기
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.list_func = [lambda x: x**2, lambda x: x**3, lambda x: x**4]

    def initializeUI(self):
        """
            어플리케이션 UI 설정
        """
        self.setGeometry(100, 100, 300, 250)
        self.setWindowTitle("QCheckbox 위젯")
        self.displayCheckBoxes()
        self.show()

    def displayCheckBoxes(self):
        """
            체크 박스와 다른 위젯들 설정
        """
        header_label = QLabel(self)
        header_label.setText("미분을 선택하세요 ")
        header_label.move(20,20)
        header_label.setWordWrap(True)
        header_label.resize(230,60)
        #체크 박스 설정
        morning_cb = QCheckBox("1번 리스트", self) #부모에 text 전달
        morning_cb.move(20,80)
        # morning_cb.toggle() # check가 된 상태로 시작하려면 주석해제
        morning_cb.stateChanged.connect(self.printToTerminal)

        after_cb = QCheckBox("2번 리스트",self)
        after_cb.move(20,100)
        after_cb.stateChanged.connect(self.printToTerminal)
        night_cb = QCheckBox("3번 리스트",self)
        night_cb.move(20,120)
        night_cb.stateChanged.connect(self.printToTerminal)

    def printToTerminal(self,checked):
        """
        체크 박스의 상태를 결정하는 방법을 보여주기 위한 함수
        어떤 위젯이 시그널(siganl)을 전송했는지 결정하기 위해 체크 박스의 텍스트 문자를 출력함
        """
        sender = self.sender()
        # if checked:
        #     print(f"{sender.text()} 가 선택되었어요")
        # else:
        #     print(f"{sender.text()} 가 해제 되었어요")

        x = np.arange(-10,10,0.01)
        if checked:
            if sender.text()=='1번 리스트':
                print("1번")
                plt.plot(x, self.list_func[0](x))
                plt.show()
                plt.draw()

            elif sender.text()=='2번 리스트':
                print("2번")
                plt.plot(x, self.list_func[1](x))
                plt.show()
                plt.draw()
            else:
                print("3번")
                plt.plot(x, self.list_func[2](x))
                plt.show()
                plt.draw()

        else:
            if sender.text() == '1번 리스트':
                plt.pause(0.0001)
                plt.close()
            elif sender.text() == '2번 리스트':
                plt.pause(0.0001)
                plt.close()
            else:
                plt.pause(0.0001)
                plt.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckBoxWindow()
    sys.exit(app.exec())
