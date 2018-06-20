import random

# inheritance
class ManufacturedObject(object):
    def __init__(self, manufacturer_name : str):

        self._manufacturer_name = manufacturer_name

    @property
    def manufacturer_name(self):
        return self._manufacturer_name


class ObjectWithInternalEngine(ManufacturedObject):

    def __init__(self,
                 manufacturer_name : str,
                 start_probability: float):
        super().__init__(manufacturer_name)
        self._start_probability = start_probability

    def launch_engine(self):
        work_probability = random.uniform(0, 1)
        if work_probability < self._start_probability:
            return True
        else:
            return False

class Engine(ObjectWithInternalEngine):
    def __init__(self,
                 manufacturer_name : str,
                 start_probability: float):
        super().__init__(manufacturer_name, start_probability)

    def start_working(self):
        launched = self.launch_engine()
        if launched:
            print('Engine started working')
        else:
            print('Need to restart the engine')
        return launched

class Automobile(ManufacturedObject):

    def __init__(self,
                 manufacturer_name : str,
                 internal_engine : Engine):
        super().__init__(manufacturer_name)
        self._engine = internal_engine

    def move(self):
        print('Launching engine, produced by: ', self._engine.manufacturer_name)
        is_working = self._engine.start_working()
        if is_working:
            print('Automobile started moving')
            return True
        return False


if __name__ == '__main__':

    print('Here will be inheritance relations examples')

    MyAutoEngine = Engine(manufacturer_name='Renault',
                          start_probability=0.9)
    MyAuto = Automobile(manufacturer_name='BMW',
                        internal_engine=MyAutoEngine)

    print('My auto manufacturer: ', MyAuto.manufacturer_name)
    started_moving = MyAuto.move()