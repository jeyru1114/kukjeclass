import tkinter as tk
import threading
from tkinter import scrolledtext
from tkinter import messagebox

ENCODING='utf-8'

class GUI(threading.Thread):
    def __init__(self,client):
        super().__init__(daemon=False,target=self.run)
        self.font=('Helvetica',13)
        self.client=client
        self.login_window=None
        self.main_window=None

    def run(self):
        self.login_window = LoginWindow(self,self.font)
        self.main_window = ChatWindow(self, self.font)
        self.notify_server(self.login_window.login, 'login')
        self.main_window.run()

    @staticmethod
    def display_alert(message):
        """Display alert box"""
        messagebox.showinfo('Error', message)

    def update_login_list(self, active_users):
        """Update login list in main window with list of users"""
        self.main_window.update_login_list(active_users)

    def display_message(self, message):
        """Display message in ChatWindow"""
        self.main_window.display_message(message)

    def send_message(self, message):
        """Enqueue message in client's queue"""
        self.client.queue.put(message)

    def set_target(self, target):
        """Set target for messages"""
        self.client.target = target

    def notify_server(self, message, action):
        """Notify server after action was performed"""
        data = action + ";" + message
        data = data.encode(ENCODING)
        self.client.notify_server(data, action)

    def login(self, login):
        self.client.notify_server(login, 'login')

    def logout(self, logout):
        self.client.notify_server(logout, 'logout')
class Window(object):
    def __init__(self,title,font):
        self.root=tk.Tk()
        self.title=title
        self.root.title(title)
        self.font=font

class LoginWindow(Window):
    def __init__(self,gui,font):
        super().__init__('Login',font)
        self.gui=gui
        self.label=None
        self.entry=None
        self.button = None
        self.login = None
        self.build_window()
        self.run()

    def build_window(self):
        """
        로그인 윈도우 생성, 위젯의 위치 설정과 이벤트 등록
        """
        self.label=tk.Label(self.root, text='로그인 입력', width=20, font=self.font)
        self.label.pack(side=tk.LEFT, expand=tk.YES)
        self.entry=tk.Entry(self.root, width=20,font=self.font)
        self.entry.focus_set()
        self.entry.pack(side=tk.LEFT)
        self.entry.bind('<Return>',self.get_login_event)
        self.button=tk.Button(self.root,text='Login',font=self.font)
        self.button.pack(side=tk.LEFT)
        self.button.bind('<Button-1>', self.get_login_event)

    def run(self):
        """
        로그인 윈도우 이벤트(action) 핸들러
        """
        self.root.mainloop()
        self.root.destroy()
    def get_login_event(self,event):
        """
            로그인 박스로부터 login 데이터 획득 하고 로그인 윈도우 닫음
        """
        self.login=self.entry.get()
        self.root.quit()
class ChatWindow(Window):
    def __init__(self,gui,font):
        super().__init__("파이썬 채팅",font)
        self.gui=gui
        self.messages_list=None
        self.logins_list=None
        self.entry=None
        self.send_button=None
        self.exit_button=None
        self.lock=threading.RLock()
        self.target=''
        self.login=self.gui.login_window.login
        self.build_window()

    def build_window(self):
        """
            chat 윈도우 구축, 위젯의 위치 설정 및 이벤트 등록
        """
        #크기 환경
        self.root.geometry('750x500')
        self.root.minsize(600, 400)
        #프레임 환경
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        #메시지 목록
        frame00 = tk.Frame(main_frame)
        frame00.grid(column=0, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)
        #로그인 목록
        frame01 = tk.Frame(main_frame)
        frame01.grid(column=1, row=0, rowspan=3, sticky=tk.N + tk.S + tk.W + tk.E)
        #entry 메시지
        frame02 = tk.Frame(main_frame)
        frame02.grid(column=0, row=2, columnspan=1, sticky=tk.N + tk.S + tk.W + tk.E)
        # 버튼
        frame03 = tk.Frame(main_frame)
        frame03.grid(column=0, row=3, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=8)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        #메시지를 표시하기 위한 스크롤 가능한 위젯
        self.messages_list = scrolledtext.ScrolledText(frame00, wrap='word', font=self.font)
        self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')
        # Listbox widget for displaying active users and selecting them
        self.logins_list = tk.Listbox(frame01, selectmode=tk.SINGLE, font=self.font,
                                      exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)
        #메시지를 입력하기 위한 Entry 위젯
        self.entry = tk.Text(frame02, font=self.font)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.send_entry_event)
        
        # Button widget for sending messages
        self.send_button = tk.Button(frame03, text='Send', font=self.font)
        self.send_button.bind('<Button-1>', self.send_entry_event)
        
        #종료 버튼
        self.exit_button=tk.Button(frame03,text='종료',font=self.font)
        self.exit_button.bind('<Button-1>',self.exit_event)
        
        #프레임에 위젯 위치 설정
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.exit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        #'x'버튼을 사용하여 윈도우 종료를 위한 프로토콜(protocol)
    def run(self):
        """
            chat 윈도우 이벤트 핸들러
        """
        self.root.mainloop()
        self.root.destroy()
    def selected_login_event(self,event):
        """
            로그인 목록에 현재 선택된 로그인을 타겟으로 설정
        """
        target=self.logins_list.get(self.logins_list.curselection())
        self.target=target
        self.gui.set_target(target)
    def send_entry_event(self,event):
        """
            Entry 필드로부터 target으로 메시지 전송
        """
        text=self.entry.get(1.0,tk.END)
        if text !='\n':
            message='msg;'+self.login+';'+self.target+';'+text[:-1]
            print(message)
            self.gui.send_message(message.encode(ENCODING))
            self.entry.mark_set(tk.INSERT,1.0)
            self.entry.delete(1.0,tk.END)
            self.entry.focus_set()
        else:
            messagebox.showinfo('Warning','입력하지 않으면 안돼요')
        with self.lock:
            self.messages_list.configure(state='normal')
            if text!='\n':
                self.messages_list.insert(tk.END,text)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)
        return 'break'
    def exit_event(self,event):
        """
            로그아웃 메시지 전송하고 '종료' 버튼 누르면 앱 종료
        """
        self.gui.notify_server(self.login,'logout')
        self.root.quit()
    def on_closing_event(self):
        """
            'x' 버튼이 눌리면 window 종료
        """
        self.exit_event(None)
    def display_message(self,message):
        """
            스크롤링 가능한 text 위젯에 표시
        """
        with self.lock:
            self.messages_list.configure(state='normal')
            self.messages_list.insert(tk.END,message)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)
    def update_login_list(self,active_users):
        """
            리스트 박스에 활성화 사용자 갱신
        """
        self.logins_list.delete(0,tk.END)
        for user in active_users:
            self.logins_list.insert(tk.END,user)
        self.logins_list.select_set(0)
        self.target=self.logins_list.get(self.logins_list.curselection())


