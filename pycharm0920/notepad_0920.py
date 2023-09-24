import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QCheckBox, QTextEdit, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np

class NotePad(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
            어플리케이션 UI 설정
        """
        self.setGeometry(100,100,300,400)
        self.setWindowTitle("Notepad GUI")
        self.notepadWidgets()
        self.show()

    def notepadWidgets(self):
        """
            편집 메뉴를 위한 푸시 버튼 생성
        """
        self.new_button = QPushButton("새로작성",self)
        self.new_button.move(20,20)
        self.new_button.clicked.connect(self.clearText)
        self.new_button.setStyleSheet("background-color: skyblue; color: white;")
        self.save_button = QPushButton("저장",self)
        self.save_button.move(170,20)
        self.save_button.clicked.connect(self.saveText)
        self.save_button.setStyleSheet("background-color: skyblue; color: white;")
        #텟스트 편집 field
        self.text_field = QTextEdit(self)
        self.text_field.resize(280,330)
        self.text_field.move(10,60)
        self.text_field.setStyleSheet("border: 4px solid skyblue;")

    ## 문제1) 2개의 event handler 작성
    def clearText(self):
        """
            "새로 작성" 버튼이 눌리면 텍스트 편집 field를 지우고 싶은지 물어보기 위한 표시 대화 창
        """
        answer = QMessageBox.question(self,"텍스트 지우기","당신은 텍스트를 지우고 싶으신가요?",QMessageBox.No | QMessageBox.Yes,
                                       QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            self.text_field.clear()
        else: pass

    def saveText(self):
        """
            "저장" 버튼이 눌리면 텍스트 편집 field에 있는 내용을 저장할지 물어보는 위한 표시대화 창
        """
        options = QFileDialog.Options()
        notepad_text = self.text_field.toPlainText()
        file_name, _ = QFileDialog.getSaveFileName(self, "파일 저장","","모든 파일(*);;Text Files(*.txt)", options=options)
        if file_name:
            with open(file_name, "w") as f:
                f.write(notepad_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePad()
    sys.exit(app.exec())