from abc import ABCMeta, abstractmethod

class State(metaclass=ABCMeta):
    @abstractmethod
    def do_clock(self, context, hour):
        pass

    @abstractmethod
    def do_user(self, context):
        pass

    @abstractmethod
    def do_alarm(self, context):
        pass

    @abstractmethod
    def do_phone(self, context):
        pass

class DayState(State):

    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def do_clock(self, context, hour):
        if hour < 9 or 17 <= hour:
            context.change_state(NightState())

    def do_user(self, context):
        context.record_log("金庫使用（昼間）")

    def do_alarm(self, context):
        context.call_security_center("非常ベル（昼間）")

    def do_phone(self, context):
        context.call_security_center("通常の通話（昼間）")

    def __str__(self):
        return "[昼間]"


class NightState(State):

    __singleton = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def do_clock(self, context, hour):
        if 9 <= hour < 17:
            context.change_state(DayState())

    def do_user(self, context):
        context.call_security_center("非常：夜間の金庫使用！")

    def do_alarm(self, context):
        context.call_security_center("非常ベル（夜間）")

    def do_phone(self, context):
        context.record_log("夜間の通話録音")

    def __str__(self):
        return "[夜間]"
