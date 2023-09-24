import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import numpy as np
class NotePad(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.list_func = [lambda x: x ** 2, lambda x: x ** 3, lambda x: x ** 4]
        self.data=['1번','2번','3번']

    def derivative(self,f,x,h=1e-5):
        return np.array((f(x+h)-f(x))/h)

    def initializeUI(self):
        """
        어플리케이션 UI설정
        """
        self.setGeometry(100,100,800, 600)
        self.setWindowTitle("Notepad GUI")
        self.notepadWidgets()
        # 배경 이미지 설정
        self.set_background_image("images/miss2.jpg")  # 이미지 파일명을 넣으세요
        self.show()

    def set_background_image(self, image_path):
        # 배경 이미지 설정
        pixmap = QPixmap(image_path)

        # 이미지를 원하는 크기로 조정 (예: 800x600 크기로 조정)
        target_size = QSize(800, 600)  # 원하는 크기로 조절
        pixmap = pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    def notepadWidgets(self):
        """
        편집메뉴를 위한 푸시 버튼 생성
        """
        self.new_button = QPushButton("New",self)
        self.new_button.move(10,20)
        self.new_button.clicked.connect(self.clearText)
        self.new_button.setStyleSheet("color: green;"
                                      "background-color: #7FFFD4")
        font = QFont()  # QFont 객체 생성
        font.setBold(True)  # 폰트를 굵게 설정
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        # self.new_button.setStyleSheet("background-color: skyblue; color: white;")


        self.new_button.setFont(font)  # 버튼에 폰트 적용
        self.save_button = QPushButton("Save",self)
        self.save_button.move(220,20)
        self.save_button.clicked.connect(self.saveText)
        self.save_button.clicked.connect(self.math)
        self.save_button.setStyleSheet("color: green;"
                                      "background-color: #7FFFD4")

        font = QFont()  # QFont 객체 생성
        font.setBold(True)  # 폰트를 굵게 설정
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        self.save_button.setFont(font)  # 새로운 폰트로 설정
        # self.save_button.setStyleSheet("background-color: skyblue; color: white;")

        #텍스트 편집 field
        self.text_field = QTextEdit(self)
        self.text_field.resize(280,330)
        self.text_field.move(10,60)
        # self.text_field.setStyleSheet("border: 4px solid skyblue;")


    def clearText(self):
        """
            "새로 작성" 버튼이 눌리면 텍스트 편집 field를 지우고 싶은지 물어보기 위한 표시 대화 창
        """
        answer = QMessageBox.question(self,"Notice","진짜 지운다?",QMessageBox.No | QMessageBox.Yes,QMessageBox.Yes)

        if answer == QMessageBox.Yes:
            self.text_field.clear()
        else:
            pass

        # print(f"{self.new_button.text()} 버튼이 눌렸어요")

    def saveText(self):
        """
        "저장" 버튼이 눌리면 텍스트 편집 field에 있는 내용을 저장할 지 표시 대화 창
        """
        options = QFileDialog.Options()
        notepad_text = self.text_field.toPlainText()
        print(notepad_text)
        file_name, _ =QFileDialog.getSaveFileName(self,"파일 저장","","모든파일(*);;Text File(*.txt)",options=options)
        splited = notepad_text.split("\n")
        print(splited)

        # if file_name:
        #     with open(file_name,"w") as f:
        #         f.write(notepad_text)
        # print(f"{self.save_button.text()} 버튼이 눌렸어요")

    def math(self):
        notepad_text = self.text_field.toPlainText()
        splited = notepad_text.split("\n")
        if '1번' in splited:
            x = np.arange(-10, 10, 0.01)
            plt.figure(1)
            plt.plot(x, self.list_func[0](x))
            diff = self.derivative(self.list_func[0], x)
            plt.plot(x, diff, 'r')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        else:
            pass
        if '2번' in splited:
            x = np.arange(-10, 10, 0.01)
            plt.figure(2)
            plt.plot(x, self.list_func[1](x))
            diff = self.derivative(self.list_func[1], x)
            plt.plot(x, diff, 'g')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        else:
            pass
        if '3번' in splited:
            plt.figure(3)
            x = np.arange(-10, 10, 0.01)
            plt.plot(x, self.list_func[2](x))
            diff = self.derivative(self.list_func[2], x)
            plt.plot(x, diff, 'y')
            plt.draw()
            plt.pause(0.001)
            plt.clf()
            plt.show()
        else:
            pass






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePad()
    sys.exit(app.exec())