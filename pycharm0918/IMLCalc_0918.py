import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from  PyQt5.QtCore import pyqtSlot

class Form(QWidget): # 소괄호안에 부모를 상속받음
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("IMLCalc.ui", self) # UI파일 불러오기, self.ui 멤버변수

        b_list = [
            self.ui.b1,
            self.ui.b2,
            self.ui.b3,
            self.ui.b4,
            self.ui.b5,
            self.ui.b6,
            self.ui.b7,
            self.ui.b8,
            self.ui.b9,
            self.ui.bplus,
            self.ui.bminus,
            self.ui.bmul,
            self.ui.bdiv,
            self.ui.bdiv_2,
            self.ui.bopen,
            self.ui.bclose
        ]
        for i in b_list: # 해당 버튼이 눌리면 호출되는 event handler
            i.clicked.connect(lambda state, button = i:self.write_edit(state,button))
        self.ui.show()

    @pyqtSlot()
    def write_edit(self, state, button):
        if self.ui.ledit.text()=="잘못된 수식!":
            self.ui.ledit.text("")
        if button.text() == "x":
            exp = "*"
        else:
            exp = button.text()
        self.ui.ledit.setText(self.ui.ledit.text()+exp)

    @pyqtSlot()
    def one_delete(self):
        arr = self.ui.ledit.text()
        self.ledit.setText(arr[:-1]) # 이상함 ui가 빠진 듯

    @pyqtSlot()
    def answer(self):
        exp = self.ui.ledit.text()
        try:
            self.ledit.setText(str(eval(exp)))
        except:
            self.ledit.setText("잘못된 수식!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())