import time


class Room:
    _light_status = False
    _air_conditioner_status = False
    _fan_status = False
    _curtain_status = False

    def __init__(self, room):
        self.room = room

    def light_control(self):
        if not self._light_status:
            self._light_status = True
            print(f"::[Room: {self.room}] >> Light is turn on now!")
        else:
            self._light_status = False
            print(f"::[Room: {self.room}] >> Light is turn off now!")

    def air_conditioner_control(self):
        if not self._air_conditioner_status:
            self._air_conditioner_status = True
            print(f"::[Room: {self.room}] >> Air Conditioner is turn on now!")
        else:
            self._air_conditioner_status = False
            print(f"::[Room: {self.room}] >> Air Conditioner is turn off now!")

    def fan_control(self):
        if not self._fan_status:
            self._fan_status = True
            print(f"::[Room: {self.room}] >> Fan is turn on now!")
        else:
            self._fan_status = False
            print(f"::[Room: {self.room}] >> Fan is turn off now!")

    def curtain_control(self):
        if not self._curtain_status:
            self._curtain_status = True
            print(f"::[Room: {self.room}] >> Curtain is turn on now!")

            percent = 0
            for i in range(5):
                percent += 20
                print(f"::[Room: {self.room}] >> Curtain turn on status <{percent}%...>")
                time.sleep(1)
            print(f"::[Room: {self.room}] >> Curtain turn on status <Finish!>")

        else:
            self._curtain_status = False
            print(f"::[Room: {self.room}] >> Curtain is turn off now!")

            percent = 0
            for i in range(5):
                percent += 20
                print(f"::[Room: {self.room}] >> Curtain turn off status <{percent}%...>")
                time.sleep(1)
            print(f"::[Room: {self.room}] >> Curtain turn off status <Finish!>")
