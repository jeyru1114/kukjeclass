import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QMessageBox, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np

class NotePad(QWidget):

    def derivative(self, f, x, h=1e-5):
        return np.array((f(x+h)-f(x))/h)

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
            어플리케이션 UI 설정
        """
        self.list_func = [lambda x: x ** 2, lambda x: x ** 3, lambda x: x ** 4]
        self.data=['1번', '2번', '3번']
        self.data_der=['1번 미분', '2번 미분', '3번 미분']
        self.data_total=[self.data, self.data_der]
        # 리스트 내에 2개[['1번', '2번', '3번'],['1번 미분', '2번 미분', '3번 미분']] 리스트가 담겨있음
        self.setGeometry(100,100,300,400)
        self.setWindowTitle("NotePad GUI")
        self.notepadWidgets()
        self.show()

    def notepadWidgets(self):
        """
            편집 메뉴를 위한 푸시 버튼 생성
        """
        self.save_button= QPushButton("저장", self)
        self.save_button.move(80,20)
        self.save_button.clicked.connect(self.saveText)
        self.save_button.setStyleSheet("background-color: skyblue; color: white;")

        #텍스트 편집 field
        self.text_field= QTextEdit(self)
        self.text_field.resize(280,330)
        self.text_field.move(10,60)
        self.text_field.setStyleSheet("border: 4px solid pink;")


    def saveText(self):
        """
            "저장" 버튼이 눌리면 텍스트 편집 field에 있는 내용을 저장할지 물어보는 위한 표시대화 창
        """
        print("저장버튼이 눌렸어요")
        #options = QFileDialog.Options()
        notepad_text = self.text_field.toPlainText()
        splited= notepad_text.split("\n")
        # contain_string_dir= [i for i in splited if i in self.data_total[1]]
        # not_contain_string_dir= [i for i in splited if i not in self.data_total[1]]
        #위에 contain_string_dir 컴프리헨션 코드랑 같은 코드
        contain_string_dir=[]
        not_contain_string_dir=[]
        for i in splited:
            if i in self.data_total[1]:
                contain_string_dir.append(i)
            else:
                not_contain_string_dir.append(i)
        print('미분 포함:', contain_string_dir, '미분 포함x :', not_contain_string_dir)



        #print('a:', contain_string_dir, 'b:', not_contain_string_dir)
        list_zip= zip(self. list_func, self.data)
        list_der_zip= zip(self.list_func, self.data_der)
        x= np.arange(-10, 10, 0.01)
        for f   , d in list_zip:
            if d in not_contain_string_dir:
                plt.plot(x, f(x))

        for f   , d in list_der_zip:
            if d in contain_string_dir:
                plt.plot(x, self.derivative(f,x))
        plt.show()


        # for i in self.data_total:
        #     if splited in i:
        #         print(splited)
        #     else:
        #         print("없어요")


if __name__ == '__main__': #메인 함수
    app= QApplication(sys.argv)
    window= NotePad()
    sys.exit(app.exec())