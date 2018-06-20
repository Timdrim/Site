import random

class Engine(object):

    def __init__(self, engine_manufacturer : str):
        self._engine_manufacturer = engine_manufacturer

    def startWorking(self):
        work_probability = random.uniform(0, 1)
        if work_probability>0.05:
            print('Engine started working')
            return True
        else:
            print('Engine did not start working')
            return False

    @property
    def engine_manufacturer(self):
        return self._engine_manufacturer

class Automobile(object):

    def __init__(self, manufacturer: str):
        """ If objects are used inside it's better to pass them as references,
        but sometimes it's impossible, i.e. too many of them, like vectors creation"""
        self._manufacturer = manufacturer
        self._engine = Engine('Renault')

    def move(self):
        print('Launching engine, produced by: ', self._engine.engine_manufacturer)
        isWorking = self._engine.startWorking()
        if isWorking:
            print('Automobile started moving')

    @property
    def manufacturer(self):
        return self._manufacturer


if __name__ == '__main__':

    print('Here will be composition relations examples')

    MyAuto = Automobile('BMW')
    print('My Auto manufacturer: ', MyAuto.manufacturer)
    MyAuto.move()