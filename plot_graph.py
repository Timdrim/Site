import cv2
import numpy as np
import class_description
import Interfaces.interface as interface
import ClassesRepresentation.integral_representation as integral_representation
import ClassesRepresentation.inheritance_representation as inheritance_representation
import ClassesRepresentation.class_description_representation as class_description_representation
import ObjectOrientedMath.MathObjects as MathObjects

all_classes_access_handler = integral_representation.all_classes
# all_classes_access_handler = inheritance_representation.all_classes
# all_classes_access_handler = class_description_representation.all_classes
# TODO plot simple association block

class GUIHandler(object):
    """ Main idea is to be able in perspective to port the development onto
        another GUI engine. Currently I plan to use OpenCV, but realisation should be
        GUI layer independent.
    """
    def __init__(self):
        self._added_class_objects = []
        self._rectangles_postions = []

    def add_class(self, one_class : class_description.ClassDescription):
        self._added_class_objects.append(one_class)

    def compile_graphic_representation(self):
        # self.img = np.zeros((600, 1024, 3), np.uint8)

        self.matrix = MathObjects.PixelMatrix( length=1024,
                                               height=600)

        self.compile_rectagles_representation()


        # cv2.rectangle(self.img, (100, 100), (200, 200), color=(255, 255, 255), thickness=3)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(self.img, 'Engine', (120, 120), font,
        #             fontScale=0.5, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        #
        # cv2.rectangle(self.img, (300, 100), (400, 200), color=(255, 255, 255), thickness=3)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(self.img, 'Automobile', (310, 120), font,
        #             fontScale=0.5, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

        # compile connections
        # go through the list of classes and make a list of connections, with their types

        # plot connections
        # pt1 = (200, 150)
        # pt2 = (300, 150)
        # cv2.arrowedLine(self.img, pt1, pt2, (0, 255, 0), 2, tipLength=0.2)

    def compile_rectagles_representation(self):
        """ We plot information that corresponds to a class in an icon"""
        # plot rectangles
        current_point = MathObjects.Point(np.array([250, 350]))
        shift_x_vector = MathObjects.Point(np.array([400, 0]))
        rectangle_size = MathObjects.Point(np.array([150, 300]))


        for item in self._added_class_objects:

            rectangle_specification = interface.IDrawableRectangle( current_point,
                                                                    rectangle_size)
            item.plot( self.matrix, rectangle_specification)
            current_point = current_point + shift_x_vector

    def compile_connections(self):
        """ """
        pass

    def show_graphic_representation(self):
        # cv2.imshow('Diagram', self.img)
        self.matrix.display()
        # cv2.waitKey()

    def _optimize_rectangle_positions(self):
        """ We can start with a simple algorithm, like taking fixed positions fro rectangles,
            in a square grid, later we can improve it"""
        pass

    def save(self, file_name: str):
        self.matrix.save(file_name)

if __name__ == '__main__':

    print('Here we make some simple graphs using openCV')

    FirstGUI = GUIHandler()

    # FIXME uncomment and plot the whole thing
    # commented for ease of developing, change it later
    for item in all_classes_access_handler:
        print(item.class_name)
        FirstGUI.add_class(item)

    FirstGUI.compile_graphic_representation()
    FirstGUI.show_graphic_representation()
    # FirstGUI.save(r'Icons\Goal.png')

    # TODO making a simple automatic connection parser
    # make a dict of class names, to search inside
    dict_of_class_names = {}
    for indi_class in all_classes_access_handler:
        dict_of_class_names.update({indi_class.class_name: indi_class})
    print(dict_of_class_names)

    for indi_class in all_classes_access_handler:
        print(indi_class.class_name)
        print('Class_name: {0}, parent_name: {1}, methods: {2}'.
              format(indi_class.class_name, indi_class.child_of, indi_class.methods))

        for key in sorted(indi_class.methods):
            print('Key: {0}, variables {1}'.format(key, indi_class.methods[key].variables))
            for indi_variable in indi_class.methods[key].variables:
                variable_type = indi_variable[1]
                if variable_type in dict_of_class_names:
                    print('Found class: {0}, reference {1}'.format(variable_type, dict_of_class_names[variable_type]))
                    print('Whole connection: class: {0} -> method: {1} -> another class: {2}'.
                          format(indi_class.class_name, key, variable_type) )
