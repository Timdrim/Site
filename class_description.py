import ObjectOrientedMath.MathObjects as MathObjects
import Interfaces.interface as interface
import cv2
import numpy as np
import copy

class MethodDescription(object):
    def __init__(self,
                 method_name: str = None,   # actual name of the method, ex. __init__
                 line_start: int = None,   # line at which starts the class descriptions, ex. 3
                 line_end: int = None,     # line at which ends the class description, ex. 22
                 variables: list = None    # list of variables as tuples [('var1': 'type1'), ('var2': 'type2'), .. ]
                 ):
        # planning to store info about methods inside them
        self._rectangle = None # MathObjects.Rectangle2D()

        # Accessible properties
        self.method_name = method_name
        self.line_start = line_start
        self.line_end = line_end
        self.variables = variables
        # self.variables = [ ('a', 'int'), ('b', 'class_sth.SomeClass')]

        self.graphic_const_init()

    def to_list(self)->list:
        list_of_str=[]
        list_of_str.append(('method_name=', str(self.method_name)))
        list_of_str.append(('line_start=', self.line_start))
        list_of_str.append(('line_end=', self.line_end))
        list_of_str.append(('variables=', self.variables))
        return list_of_str

    def plot(self,
             matrix: MathObjects.PixelMatrix,
             rectangle: MathObjects.Rectangle2D):
        """ Plotting a single method, with first plot we will
        pass info about its position for connections plotting"""
        self._rectangle = rectangle
        text_rectangle = MathObjects.Rectangle2D(upper_left_point=self._rectangle.upper_left_point,
                                                 bottom_right_point=self._rectangle.bottom_right_point
                                                                    + self.shift_vector_gap)
        matrix.add_text(text_rectangle, self.method_name)
        matrix.add_rectangle(self._rectangle, line_thickness=1)
        # Adding input-output images
        icon = cv2.imread(r'Icons/methods_io_2.png')
        upper_right_point = MathObjects.Point.init_x_y( x=self._rectangle.bottom_right_point.x,
                                                        y=self._rectangle.upper_left_point.y)
        matrix.add_image(icon,
                         high_point=upper_right_point,
                         low_point=self._rectangle.bottom_right_point)

    def graphic_const_init(self):
        gap = 4
        self.shift_vector_gap = MathObjects.Point.init_x_y(x=0,
                                                           y=gap)

class ClassDescription(object):
    root_path = None
    def __init__(self,
                 class_name: str = None,   # actual name of the class, ex. Engine
                 file_name: str = None,    # name of the file, where class resides,
                                           # i.e. ObjectsRelations\association_relations.py
                 line_start: int = None,   # line at which starts the class descriptions, ex. 3
                 line_end: int = None,      # line at which ends the class description, ex. 22
                 child_of: str = None
                 ):
        self._rectangle = MathObjects.Rectangle2D()

        # Accessible properties
        self.class_name = class_name
        self.file_name = file_name
        self.line_start = line_start
        self.line_end = line_end
        self.child_of = child_of

        self.methods = {}
        self.number_of_methods = 0

    def add_method(self, method: MethodDescription):
        """

        :param method: method description
        :return:
        """
        self.methods.update({method.method_name: method})
        self.number_of_methods += 1



    # FIXME plot method is too big
    def plot(self,
             matrix: MathObjects.PixelMatrix,
             rectangle:interface.IDrawableRectangle):
        """ Later I can refactor it into, font resizing, etc. For the moment let it be simple
            matrix: where we draw everything
            rectangle: all the space for a given class
        """
        font_size = 16
        line_thickness = 4
        small_line_thickness = 1
        gap = 4

        half_vector = MathObjects.Point.init_x_y(x=-rectangle.size.x/2, y=rectangle.size.y/2)
        majour_upper_left_point = rectangle.center_position + half_vector
        majour_bottom_right_point = rectangle.center_position - half_vector

        # plot rectangle for class and save it for later access
        self._rectangle.upper_left_point = majour_upper_left_point
        self._rectangle.bottom_right_point = majour_bottom_right_point
        matrix.add_rectangle(self._rectangle)

        # plot class name
        upper_left_of_rectangle_for_class_name = MathObjects.Point.init_x_y(
                                                 x=majour_upper_left_point.x + line_thickness,
                                                 y=majour_upper_left_point.y - line_thickness)
        bottom_right_of_rectangle_for_class_name = MathObjects.Point.init_x_y(
                                                 x=majour_bottom_right_point.x,
                                                 y=majour_upper_left_point.y - font_size)
        class_name_rectangle = MathObjects.Rectangle2D(upper_left_point=upper_left_of_rectangle_for_class_name,
                                                       bottom_right_point=bottom_right_of_rectangle_for_class_name)
        matrix.add_text(class_name_rectangle, self.class_name)

        # PLOT METHODS and arrows for them
        # plot methods box
        upper_left_of_methods = MathObjects.Point.init_x_y(x=majour_upper_left_point.x + gap,
                                                           y=bottom_right_of_rectangle_for_class_name.y - gap)
        methods_heigth = self.number_of_methods * (font_size + gap + small_line_thickness)
        bottom_right_of_methods = MathObjects.Point.init_x_y(x=majour_bottom_right_point.x,
                                                             y=upper_left_of_methods.y - methods_heigth - gap)
        upper_left_of_methods_boundary = MathObjects.Point.init_x_y(x=upper_left_of_methods.x - gap,
                                                                    y=upper_left_of_methods.y)
        methods_rectangle = MathObjects.Rectangle2D(upper_left_point=upper_left_of_methods_boundary,
                                                    bottom_right_point=bottom_right_of_methods)
        matrix.add_rectangle(methods_rectangle, line_thickness=small_line_thickness)
        # plot single method
        # print('For class {0}, we plot the following methods: '.format(self.class_name))
        shift_vector_y = MathObjects.Point.init_x_y(x=0,
                                                    y=font_size + small_line_thickness + gap)
        shift_vector_x = MathObjects.Point.init_x_y(x=bottom_right_of_methods.x - upper_left_of_methods.x,
                                                    y=0)
        for index, method_name in enumerate(sorted(self.methods)):
            current_upper_left = upper_left_of_methods - index * shift_vector_y
            method_end_point = current_upper_left + shift_vector_x - shift_vector_y
            method_bounding_rectangle = MathObjects.Rectangle2D(upper_left_point=current_upper_left,
                                                            bottom_right_point=method_end_point)
            self.methods[method_name].plot(matrix, method_bounding_rectangle)

if __name__ == '__main__':

    print('Test new functionality')

    NewDescription = ClassDescription( class_name='ClassDescription',
                                       line_start=6,
                                       line_end=60,
                                       file_name='class_description.py')
    print(NewDescription.class_name)


    NewMethod = MethodDescription(method_name='__init__',
                                  line_start=25,
                                  line_end=43,
                                  variables= [('method_name', 'str'), ('line_start', 'int'), ('line_end', 'int'), ('variables', 'list'), ]
                                 )

    NewDescription.add_method(NewMethod)
    print(NewDescription.methods['__init__'].variables)
