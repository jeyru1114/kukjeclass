import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QPushButton,QCheckBox,QDesktopWidget,QMessageBox,QTextEdit,QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
import numpy as np
class NotePad(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        어플리케이션 UI설정
        """
        self.setGeometry(100,100,300,400)
        self.setWindowTitle("Notepad GUI")
        self.notepadWidgets()
        self.show()

    def notepadWidgets(self):
        """
        편집메뉴를 위한 푸시 버튼 생성
        """
        self.new_button = QPushButton("New",self)
        self.new_button.move(10,20)
        self.new_button.clicked.connect(self.clearText)
        self.new_button.setStyleSheet("color: #7FFFD4;"
                                      "background-color: pink")
        font = QFont()  # QFont 객체 생성
        font.setBold(True)  # 폰트를 굵게 설정
        font.setPointSize(12)  # 원하는 폰트 크기로 설정



        self.new_button.setFont(font)  # 버튼에 폰트 적용
        self.save_button = QPushButton("Save",self)
        self.save_button.move(180,20)
        self.save_button.clicked.connect(self.saveText)
        self.save_button.setStyleSheet("color: #7FFFD4;"
                                      "background-color: pink")

        font = QFont()  # QFont 객체 생성
        font.setBold(True)  # 폰트를 굵게 설정
        font.setPointSize(12)  # 원하는 폰트 크기로 설정
        self.save_button.setFont(font)  # 새로운 폰트로 설정


        #텍스트 편집 field
        self.text_field = QTextEdit(self)
        self.text_field.resize(280,330)
        self.text_field.move(10,60)
        self.text_field.setStyleSheet("border: 4px solid pink;")

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
        file_name, _ =QFileDialog.getSaveFileName(self,"파일 저장","","모든파일(*);;Text File(*.txt)",options=options)
        if file_name:
            with open(file_name,"w") as f:
                f.write(notepad_text)
        # print(f"{self.save_button.text()} 버튼이 눌렸어요")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePad()
    sys.exit(app.exec())