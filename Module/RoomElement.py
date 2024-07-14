import time


class Room:
    _light_status = False
    _air_conditioner_status = False
    _fan_status = False
    _curtain_status = False
    _music_status = False
    _tv_status = False

    _light_color = ['Good Night', 'Leisure', 'Gorgeous', 'Dream', 'Sunflower', 'Grassland']
    _light_color_index = 0
    _light_color_status = False

    def __init__(self, room):
        self.room = room

    def light_control(self):
        if not self._light_status:
            self._light_status = True
            print(f"::[{self.room}] >> Light is turn on now!")
            print(f"::[{self.room}] >> Room light color \"{self._light_color[self._light_color_index]}\"", end='\n\n')
        else:
            self._light_status = False
            print(f"::[{self.room}] >> Light is turn off now!", end='\n\n')

    def air_conditioner_control(self):
        if not self._air_conditioner_status:
            self._air_conditioner_status = True
            print(f"::[{self.room}] >> Air Conditioner is turn on now!", end='\n\n')
        else:
            self._air_conditioner_status = False
            print(f"::[{self.room}] >> Air Conditioner is turn off now!", end='\n\n')

    def fan_control(self):
        if not self._fan_status:
            self._fan_status = True
            print(f"::[{self.room}] >> Fan is turn on now!", end='\n\n')
        else:
            self._fan_status = False
            print(f"::[{self.room}] >> Fan is turn off now!", end='\n\n')

    def curtain_control(self):
        if not self._curtain_status:
            self._curtain_status = True
            print(f"::[{self.room}] >> Curtain is turn on now!")

            percent = 0
            for i in range(5):
                percent += 20
                print(f"::[{self.room}] >> Curtain turn on status <{percent}%...>")
                time.sleep(1)
            print(f"::[{self.room}] >> Curtain turn on status <Finish!>", end='\n\n')

        else:
            self._curtain_status = False
            print(f"::[{self.room}] >> Curtain is turn off now!")

            percent = 0
            for i in range(5):
                percent += 20
                print(f"::[{self.room}] >> Curtain turn off status <{percent}%...>")
                time.sleep(1)
            print(f"::[{self.room}] >> Curtain turn off status <Finish!>", end='\n\n')

    def music_control(self):
        if not self._music_status:
            self._music_status = True
            print(f"::[{self.room}] >> Music is turn on now!", end='\n\n')
        else:
            self._music_status = False
            print(f"::[{self.room}] >> Music is turn off now!", end='\n\n')

    def tv_control(self):
        if not self._tv_status:
            self._tv_status = True
            print(f"::[{self.room}] >> Television is turn on now!", end='\n\n')
        else:
            self._tv_status = False
            print(f"::[{self.room}] >> Television is turn off now!", end='\n\n')

    def light_color_control(self):
        if self._light_status:
            self._light_color_index += 1
            
            print(f"::[{self.room}] >> Room light color change to "
                  f"\"{self._light_color[self._light_color_index]}\"", end='\n\n')
        
            if self._light_color_index >= len(self._light_color):
                self._light_color_index = 0
