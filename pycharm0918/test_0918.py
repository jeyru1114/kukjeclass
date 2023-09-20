class Qwi:
    def __init__(self):
        print("나는 위젯이에요")


class Form(Qwi): # 소괄호안에 부모를 상속받음
    def __init__(self):
        super().__init__()
        print("나는 상속된 놈이에요")

if __name__=='__main__':
    a = Form()
