import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QButtonGroup)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np

class DisplaySurvey(QWidget):

    def derivative(self, f, x, h=1e-5):
        return np.array((f(x+h)-f(x))/h)

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.list_func = [lambda x: x ** 4+3 * x **2+6*x, lambda x: np.log(abs(x)+0.01), lambda x: np.exp(x)]

    def initializeUI(self):
        self.setGeometry(100, 100, 400, 230)
        self.setWindowTitle("Survey GUI")
        self.displayWidgets()
        self.show()

    def displayWidgets(self):
        title = QLabel("레스토랑 이름")
        title.setFont(QFont('Arial', 17))
        question = QLabel("오늘의 서비스 만족도는?")

        # 수평 레이아웃 생성
        title_h_box = QHBoxLayout()
        title_h_box.addStretch()
        title_h_box.addWidget(title)
        title_h_box.addStretch()

        ratings = ["1번 함수", "2번 함수", "3번 함수"]

        # 체크 박스 생성하고 수평 레이아웃에 추가하고 stretable(펼쳐지는 기능) 추가
        # 위젯의 양측 공간 확보
        ratings_h_box = QHBoxLayout()
        ratings_h_box.setSpacing(60)  # 수평 레이아웃에서 위젯 사이의 간격 설정
        ratings_h_box.addStretch()
        for rating in ratings: #s를 붙이면 복수=배열
            rate_label = QLabel(rating, self)
            ratings_h_box.addWidget(rate_label)
            ratings_h_box.addStretch()

        cb_h_box = QHBoxLayout()
        cb_h_box.setSpacing(100)

        # 체크 박스를 포함하는 버튼 그룹 생성
        scale_bg = QButtonGroup(self)
        cb_h_box.addStretch()
        for cb in range(len(ratings)):
            scale_cb = QCheckBox(str(cb), self)
            cb_h_box.addWidget(scale_cb)
            scale_bg.addButton(scale_cb)
            cb_h_box.addStretch()

        # 체크 박스가 눌리면 신호(signal) 발생 확인
        scale_bg.buttonClicked.connect(self.checkboxClicked)
        close_button = QPushButton("종료", self)

        # 수직 레이아웃 생성 후 위젯과 h_box 레이아웃 생성
        v_box = QVBoxLayout()
        v_box.addLayout(title_h_box)
        v_box.addWidget(question)
        v_box.addStretch(1)
        v_box.addLayout(ratings_h_box)
        v_box.addStretch(2)
        v_box.addLayout(cb_h_box)
        v_box.addStretch(3)
        v_box.addWidget(close_button)

        # 윈도우의 main 레이아웃 설정
        self.setLayout(v_box)

    def checkboxClicked(self, cb):
        """
            선택된 checkbox 출력
        """
        x = np.arange(-10, 10, 0.1)
        for _ in self.list_func:
            if cb.text() == '1':  # log 함수 처리
                x = abs(x)
            f = self.list_func[int(cb.text())]
            plt.plot(x + 0.05, f(x), marker='x', color='r')
            plt.plot(x, self.derivative(f, x), marker='o', color='b')
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplaySurvey()
    sys.exit(app.exec())