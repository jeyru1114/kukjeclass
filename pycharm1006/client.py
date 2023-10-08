import select
import socket
import threading
import queue
import time
from gui import * #우리가 오전에 열심히 노가다 했던 파일 import

ENCODING = 'utf-8'
HOST='localhost'
PORT=8880

class Client(threading.Thread):
    def __init__(self,host,port):
        super().__init__(daemon=False, target=self.run)

        self.host=host
        self.port=port
        self.buffer_size=2048
        self.sock=None
        self.connected=self.connect_to_server()
        self.buffer_size=1024
        self.queue=queue.Queue()
        self.lock=threading.RLock()
        self.login=''
        self.target=''
        self.login_list=[]
        if self.connected:
            self.gui=GUI(self)
            self.start()
            self.gui.start()
            #gui가 데몬 쓰레드가 아닌경우,
            #데몬 쓰레드는 background에서 돌아가는 쓰레드
            #gui app을 종료한 후 종료됨

    def connect_to_server(self):
        """
            소켓(socket) 인터페이스를 이용하여 서버와 통신(연결) is_connected 반환
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET는 인터넷, SOCK_STREAM은 소켓스트림
            self.sock.connect((str(self.host),int(self.port)))
        except ConnectionRefusedError:
            print("서버가 비활성화 상태이므로 연결할수 없어요")
            return False
        return True

    def run(self): # 오른쪽 화살표가 뜨는건 반환 타입이 없다(권고 사항)
        """
            select 모듈을 이용하여 클라이언트 - 서버 통신을 처리하는 핸들러
        """
        inputs = [self.sock]
        outputs = [self.sock]
        while inputs:
            try:
                read, write, exceptional = select.select(inputs,outputs,inputs)
                #서버가 예기치 않게 종료되면 file descriptor 값이 0보다 작은것이 발생하고
                #valueError 예외가 발생함
            except ValueError:
                print("서버 오류")
                GUI.display_alert('서버 오류가 발생하였습니다. 앱을 종료하세요')
                self.sock.close()
                break
            if self.sock in read:
                with self.lock:
                    try:
                        data = self.sock.recv(self.buffer_size)
                    except socket.error:
                        print("소켓 오류")
                        GUI.display_alert('서버 오류가 발생하였습니다. 앱을 종료하세요')
                        self.sock.close()
                        break

                self.process_received_data(data)
            if self.sock in write:
                if not self.queue.empty():
                    data = self.queue.get()
                    self.send_message(data)
                    self.queue.task_done()
                else:
                    time.sleep(0.05)
            if self.sock in exceptional:
                print("서버 오류")
                GUI.display_alert('서버 오류가 발생하였습니다. 앱을 종료하세요')
                self.sock.close()
                break

    def process_received_data(self,data):
        """
            서버로부터 수신된 데이터 처리
        """
        if data:
            message = data.decode(ENCODING)
            message = message.split('\n')
            # 반복문 message에서 하나씩 꺼내어 msg로 하고
            # msg가 공백이 아니면
            # msg를 문자열 분리(;로 분리)하고 분리한 msg를 다시 msg에 저장하고

            #만약 0번 msg가 'msg'와 같은지 판단하여
            #같으면 msg의 1번 index의 값과 3번 index의 값을 문자열 결합 하고 출력함
            #self.gui.display_message에 text 문자열 전달함
            #그렇지 않고 msg의 2번 index가 self.login과 같지 않고 msg의 2번 index의 값이 'ALL'과 같지 않으면
            #self.login에 msg의 2번 index의 값을 저장
            # msg[0]의 elif 에서
            #msg의 0번 index의 값이 'login'이면
            #self.gui.main_window.update_login_list 에 msg의 1번 index부터 마지막 데이터까지 slicing 하여 전달함
            print(message)
            for msg in message:
                if msg != '':
                    msg = msg.split(';')

                    if msg[0] == 'msg':
                        text = msg[1] + ' >> ' + msg[3] + '\n'
                        print(msg)
                        self.gui.display_message(text)

                        # if chosen login is already in use
                        if msg[2] != self.login and msg[2] != 'ALL':
                            self.login = msg[2]

                    elif msg[0] == 'login':
                        self.gui.main_window.update_login_list(msg[1:])


    def notify_server(self, action,action_type):
        """
            클라이언트로부터 이벤트(action)이 발생하면 서버에 알림(notify)
        """
        self.queue.put(action)
        if action_type == 'login':
            self.login = action.decode(ENCODING).split(';')[1]
        elif action_type == 'logout':
            self.sock.close()

    def send_message(self,data):
        """
            서버로 암호화된(encoded) 데이터 전송
        """
        with self.lock:
            try:
                self.sock.send(data)
            except socket.error:
                GUI.display_alert('서버 오류가 발생하였습니다. 앱을 종료하세요')

if __name__ == '__main__':
    Client(HOST,PORT) #새로운 CLient 생성 (IP,Port를 사용하여)