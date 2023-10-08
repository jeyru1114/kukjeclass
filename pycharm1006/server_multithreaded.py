import socket
import threading
import queue
import time


ENCODING = 'utf-8'
HOST='localhost'
PORT=8880

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__(daemon=False, target=self.run)

        self.host = host
        self.port = port
        self.buffer_size = 2048
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.connection_list = []
        self.login_list = {}
        self.queue = queue.Queue()
        
        self.shutdown = False
        try:
            self.sock.bind((str(self.host), int(self.port)))
            self.sock.listen(10)
            self.sock.setblocking(False)
        except socket.error:
            self.shutdown = True
        if not self.shutdown:
            listener = threading.Thread(target=self.listen, daemon=True)
            receiver = threading.Thread(target=self.receive, daemon=True)
            sender = threading.Thread(target=self.send, daemon=True)
            self.lock = threading.RLock()
            listener.start()
            receiver.start()
            sender.start()
            self.start()
    def run(self):
        """
            메인 쓰레드 메서드
        """
        print("종료하기 위해 \'quit\'를 입력하세요")
        while not self.shutdown:
            message = input()
            if message == 'quit':
                self.sock.close()
                self.shutdown = True
                print("종료 되었습니다")

    def listen(self):
        """
            새로운 연결(Connection)을 위해 대기(listen)
        """
        print("리스너 쓰레드가 시작되었습니다")
        while True:
            try:
                self.lock.acquire() #lock 획득(lock을 획득하고 쓰레드가 일처리하고, lock을 해제해야 다른 쓰레드가 사용할수 있음
                connection, address = self.sock.accept() #소켓 수신
                connection.setblocking(False)
                if connection not in self.connection_list:
                    self.connection_list.append(connection)
            except socket.error:
                pass
            finally:
                self.lock.release() #사용후 lock 해제
            time.sleep(0.050)

    def receive(self):
        """
            새로운 메세지를 위한 대기 (listen)
        """
        print("리시버 쓰레드가 시작되었어요")
        while True:
            if len(self.connection_list) > 0:
                for connection in self.connection_list:
                    try:
                        self.lock.acquire()
                        data = connection.recv(self.buffer_size)
                    except socket.error:
                        data = None
                    finally:
                        self.lock.release() # 사용후 lock 해제
                    self.process_data(data, connection)

    def send(self):
        """
            서버의 큐(Queue)로 부터의 메세지 전송
        """
        while True:
            if not self.queue.empty():
                target, origin, data = self.queue.get()
                if target == 'all':
                    self.send_to_all(origin, data)
                else:
                    self.send_to_one(target, data)
                self.queue.task_done()
            else:
                time.sleep(0.05)

    def send_to_all(self, origin, data):
        """
            origin을 제외하고 모든 사용자에게 데이터 전송
        """
        if origin != 'server':
            origin_address = self.login_list[origin]
        else:
            origin_address = None
        for connection in self.connection_list:
            if connection != origin_address:
                try:
                    self.lock.acquire()
                    connection.send(data)
                except socket.error:
                    self.remove_connection(connection)
                finally:
                    self.lock.release()

    def send_to_one(self, target, data):
        """
            특정 target에 데이터 전송
        """
        target_address = self.login_list[target]
        try:
            self.lock.acquire()
            target_address.send(data)
        except socket.error:
            self.remove_connection(target_address)
        finally:
            self.lock.release()

    def process_data(self, data, connection):
        """
            수신된 데이터 처리
        """
        if data:
            message = data.decode(ENCODING)
            message = message.split(";", 3)
            if message[0] == 'login':
                tmp_login = message[1]
                while message[1] in self.login_list:
                    message[1] += '#'
                if tmp_login != message[1]:
                    prompt = 'msg;server;' + message[1] + ';Login ' + tmp_login \
                    	+ ' 이미 사용중 . 당신의 로그인은 ' + message[1] + '로 변경되었습니다 \n'
                    self.queue.put((message[1], 'server', prompt.encode((ENCODING))))
                self.login_list[message[1]] = connection
                print(message[1] + ' 는 로그인 되었어요')
                self.update_login_list()
            elif message[0] == 'logout':
                self.connection_list.remove(self.login_list[message[1]])
                if message[1] in self.login_list:
                    del self.login_list[message[1]]
                print(message[1] + ' 이 로그아웃 되었어요 ')
                self.update_login_list()
            elif message[0] == 'msg' and message[2] != 'all':
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                self.queue.put((message[2], message[1], data))
                
            elif message[0] == 'msg':
                msg = data.decode(ENCODING) + '\n'
                data = msg.encode(ENCODING)
                self.queue.put(('all', message[1], data))

    def remove_connection(self, connection):
        """
            서버의 Connection 목록으로부터 Connection 제거
        """
        self.connerction_list.remove(connection)
        for login, address in self.login_list.items():
            if address == connection:
                del self.login_list[login]
                break
        self.update_login_list()
    def update_login_list(self):
        """
            활성화 사용자 목록 갱신
        """
        logins = 'login'
        for login in self.login_list:
            logins += ';' + login
        logins += ';all' + '\n'
        self.queue.put(('all', 'server', logins.encode(ENCODING))) #daemon 수정

if __name__=='__main__':
    server = Server(HOST, PORT) #IP, PORT를 이용하여 새로운 서버 생성
