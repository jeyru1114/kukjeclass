import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QFont
import cv2

class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__() # QWidgey에 대한 기본 생성자 생성
        self.initializeUI()

    def initializeUI(self):
        background_image = "images/m1.jpg"
        profile_image = "images/j.png"
        """
        Application GUI 설정
        """
        numpy_data = cv2.imread(background_image)
        height, width, channel = numpy_data.shape
        START_X = 0 # START_X 대문자는 상수로 인식, 바꾸지 않을경우
        START_Y = 0 # START_Y
        MARGIN = 50
        self.setGeometry(START_X,START_Y,START_X+width+MARGIN,START_Y+height+MARGIN)
        self.setWindowTitle("개인 프로필")
        self.displayImages(background_image,profile_image)
        self.displayUserInfo() # 함수 구현
        self.show()

    def displayImages(self,img1,img2):
        """
        배경과 프로필 이미지 표시
        이미지 파일이 존재하는지 체크하고 존재하지 않으면 예외처리
        """
        text = QLabel(self)
        text.setText("안녕하세요")
        text.move(105,15)


        try:
            with open(img1):
                background= QLabel(self)
                pixmap = QPixmap(img1)
                background.setPixmap(pixmap)
        except FileNotFoundError:
            print("이미지가 없어요")
        try:
            with open(img2):
                user_image = QLabel(self)
                pixmap = QPixmap(img2)
                user_image.setPixmap(pixmap)
                user_image.move(80,20)
        except FileNotFoundError:
            print("이미지가 없어요")

    def displayUserInfo(self):
        """
        사용자 프로필을 표시하기 위한 Label 생성
        """
        #QLabel객체 생성(user_name)
        #setText() 이용하여 여러분 이름
        #user_name을 x 축으로 85, y 축으로 140이동
        #setFont를 이용하여 인자 전달(QFont('Arial', 20))
        user_name = QLabel(self)
        user_name.setText('은영')
        user_name.move(82,400)
        user_name.setFont(QFont('Arial', 20))
        user_name.setStyleSheet("color: white")

        # QLabel객체 생성(bio_title)
        # setText()이용하여 'Biography'전달
        # bio_title x축으로 15, y 축으로 170 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 17))
        bio_title = QLabel(self)
        bio_title.setText('Biography')
        bio_title.move(15,440)
        bio_title.setFont(QFont('Arial', 17))
        bio_title.setStyleSheet("color: skyblue")

        # QLabel객체 생성(about)
        # setText()이용하여 '나는 국제 아카데미에서 공부중 2개월이 되었고 유능한 개발자를 꿈꾸다' 전달
        # about.setWordWrap(True)
        # about x축으로 15, y 축으로 190 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 20))
        about = QLabel(self)
        about.setText('나는 국제 아카데미에서 공부중 2개월이 되었고 유능한 개발자를 꿈꾸다')
        about.move(15,480)
        about.setFont(QFont('Arial', 20))
        about.setStyleSheet("color: white;")

        # QLabel객체 생성(skills_title)
        # setText()이용하여 'skills' 전달
        # skills_title x축으로 15, y 축으로 240 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 17))
        skills_title = QLabel(self)
        skills_title.setText('skills')
        skills_title.move(15,520)
        skills_title.setFont(QFont('Arial', 17))
        skills_title.setStyleSheet("color: pink;")

        # QLabel객체 생성(skills)
        # skills x축으로 15, y 축으로 260 이동
        skills = QLabel(self)
        skills.setText('Python | JS | Java | SQL')
        skills.move(15,560)
        skills.setStyleSheet("color: white;")

        # QLabel객체 생성(experience_title)
        # setText()이용하여 '경력' 전달
        # experience_title x축으로 15, y 축으로 290 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 17))
        experience_title = QLabel(self)
        experience_title.setText('경력')
        experience_title.move(15,580)
        experience_title.setFont(QFont('Arial', 17))
        experience_title.setStyleSheet("color: gray;")

        # QLabel객체 생성(experience)
        # setText()이용하여 '파이썬 개발자' 전달
        # experience x축으로 15, y 축으로 310 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 17))
        experience = QLabel(self)
        experience.setText('파이썬 개발자')
        experience.move(15,620)
        experience.setFont(QFont('Arial', 17))
        experience.setStyleSheet("color: white;")

        # QLabel객체 생성(dates)
        # setText()이용하여 '2022 7월 부터 현재까지' 전달
        # dates x축으로 15, y 축으로 330 이동
        # setFont를 이용하여 인자 전달 (QFont('Arial', 10))
        dates = QLabel(self)
        dates.setText('2022 7월 부터 현재까지')
        dates.move(15,660)
        dates.setFont(QFont('Arial', 10))
        dates.setStyleSheet("color: white;")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmptyWindow()
    sys.exit(app.exec())