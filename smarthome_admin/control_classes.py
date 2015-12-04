__author__ = 'dmarkey'
from .models import TemperatureRecord

class ControlBase(object):
    @staticmethod
    def init(controller):
        pass

    @staticmethod
    def on_beacon(controller):
        pass

    @staticmethod
    def get_extra_items(self, controller):
        return None


class Sockets(ControlBase):
    @staticmethod
    def init(controller, number_of_sockets=4):
        from .models import Socket

        for i in range(1, number_of_sockets + 1):
            Socket(controller=controller, number=i).save()

    @staticmethod
    def event(controller, event):
        if event['event'] == "BEACON":
            from .models import Socket
            for s in Socket.objects.filter(controller=controller):
                s.send_state()


class Temperature(ControlBase):
    @staticmethod
    def init(controller):
        pass

    @staticmethod
    def event(controller, event):
        if event['event'] == "Temp":

            TemperatureRecord(temperature=event['value'], controller=controller).save()

    def get_extra_items(self, controller):
        return TemperatureRecord.objects.filter(controller=controller).order_by("-pk")[0]


class RemoteControl(ControlBase):
    @staticmethod
    def init(controller):
        pass

    @staticmethod
    def event(controller, event):
        print("RC Event")
        from .models import RemoteEvent, RegisteredRemoteEvent
        if event['event'] == "IRIN":
            RemoteEvent(encoding=event['encoding'], value=event['code'], controller=controller).save()
            for x in RegisteredRemoteEvent.objects.filter(value=event['code'], encoding=event['encoding']):
                x.execute()
        elif event['event'] == "BEACON":
            RemoteEvent.objects.filter(controller=controller).delete()


CONTROL_CLASSES = {"Sockets": Sockets,
                   "Temperature": Temperature, "RemoteControl": RemoteControl}
