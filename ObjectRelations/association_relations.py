import random
import os

class Engine(object):

    def __init__(self,
                 engine_manufacturer : str,
                 start_probability : float):
        self._engine_manufacturer = engine_manufacturer
        self._start_probability = start_probability

    def startWorking(self):
        work_probability = random.uniform(0, 1)
        if work_probability < self._start_probability:
            print('Engine started working')
            return True
        else:
            print('Engine did not start working')
            return False
 # comment

    @property
    def engine_manufacturer(self):
        return self._engine_manufacturer

# comment
def some_stupid_function_doesnot_belong_to_class():
    print('LOL I am outside of the class')


class Automobile(object):

    def __init__(self, manufacturer: str):

        self._manufacturer = manufacturer

    def move(self, engine_to_launch: Engine) -> bool:
        print('Launching engine, produced by: ', engine_to_launch.engine_manufacturer)
        isWorking = engine_to_launch.startWorking()
        if isWorking:
            print('Automobile started moving')
            return True
        return False

    @property
    def manufacturer(self):
        return self._manufacturer

if __name__ == '__main__':

    print('Here will be aggregation relations examples')

    MyFirstAutoEngine = Engine(engine_manufacturer='Mercedes',
                               start_probability=0.5)
    MySecondAutoEngine = Engine(engine_manufacturer='Renault',
                                start_probability=0.9)
    MyAuto = Automobile(manufacturer='BMW')

    print('My auto manufacturer: ', MyAuto.manufacturer)
    started_moving = MyAuto.move( MyFirstAutoEngine)
    if not started_moving:
        MyAuto.move( MySecondAutoEngine)

    print(os.path.dirname(os.path.abspath(__file__)))

    some_stupid_function_doesnot_belong_to_class()