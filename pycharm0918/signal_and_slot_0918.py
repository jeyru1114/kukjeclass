import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import(
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton
)

class MainWindow(QWidget):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Qt signals & slots')

        #위젯 생성
        # label - Qlabel()
        # Line_edit = QLineEdit()
        # Line_edit.textChanged
        button = QPushButton('나를 눌러라')
        button.clicked.connect(self.button_clicked)

        #수직 layout를 사용하여 window에 button 배치
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(button)

        self.show()

    def button_clicked(self):
        print('버튼이 눌렸어요')
        x = np.arange(-10,10,0.01)
        y = [2 * i * i + 5 * i + 3 for i in x]
        #문제1) 미분 함수 결과도 그래프 그리기

        def derivative(f, x, h=0.0001):  # 미분의 정의
            return (f(x + h) - f(x)) / h

        def f1(x):
            return 2 * x * x + +5 * x + 3
        y_dev = derivative(f1, x)
        plt.plot(x,y)
        plt.plot(x, y_dev)
        plt.show()


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())