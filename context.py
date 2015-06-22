from abc import ABCMeta, abstractmethod
from tkinter import *
import state


class Context(metaclass=ABCMeta):
    @abstractmethod
    def set_clock(self, hour):
        pass

    @abstractmethod
    def change_state(self, state):
        pass

    @abstractmethod
    def call_security_center(self, msg):
        pass

    @abstractmethod
    def record_log(self, msg):
        pass


class SafeFrame(Context, Frame):
    def __init__(self, master=None):
        # 初期状態を設定
        self.state = state.DayState()

        # click処理のラムダ式
        do_use = lambda: self.state.do_user(self)
        do_alarm = lambda: self.state.do_alarm(self)
        do_phone = lambda: self.state.do_phone(self)
        do_exit = lambda: exit()

        # Frame初期化
        Frame.__init__(self, master)
        self.pack()
        self.text_clock = StringVar()
        Label(self, text='clock', textvariable=self.text_clock).pack()
        self.text_screen = StringVar()
        Label(self, text='screen', textvariable=self.text_screen).pack()

        self.button_use = Button(self, text="金庫使用", command=do_use)
        self.button_alarm = Button(self, text="非常ベル", command=do_alarm)
        self.button_phone = Button(self, text="通常通話", command=do_phone)
        self.button_exit = Button(self, text="終了", command=do_exit)

        self.button_use.pack()
        self.button_alarm.pack()
        self.button_phone.pack()
        self.button_exit.pack()

        # タイマー定期実行
        self.hour = 0
        self.timer()

    def timer(self):
        if self.hour >= 24:
            return
        self.hour += 1
        self.set_clock(self.hour)
        self.after(1000, self.timer)

    def set_clock(self, hour):
        clock_string = "現在の時刻は"
        if hour < 10:
            clock_string += "0{0}:00".format(hour)
        else:
            clock_string += "{0}:00".format(hour)

        print(clock_string)
        self.text_clock.set(clock_string)
        self.state.do_clock(self, self.hour)

    def change_state(self, state):
        print("{0}から{1}へ状態が変化しました。".format(self.state, state))
        self.state = state

    def call_security_center(self, msg):
        self.text_screen.set("{0}\ncall! {1}".format(self.text_screen.get(), msg))

    def record_log(self, msg):
        self.text_screen.set("{0}\nrecord... {1}".format(self.text_screen.get(), msg))
