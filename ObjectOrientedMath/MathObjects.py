"""
Motivation: When using OpenCV with Python we have to deal with
numpy arrays. It has a downside of lower readability, for example, when we define
p = np.array([2, 5]) we define an object that has properties of a vector point, but in many ways
it is non-intuitive to use, we can't access x-coordinate as p.x, we need to use p[0].
Moreover we have incompatibility with openCV definition of x and y coordinates.
I hope to write an object oriented wrapper that would make it intuitive to use.
for example p3 = p2 + p1 looks intuitive. Numpy supports this, but if we use multiplication:
p3 = p2*p1 it returns neither vector nor scalar product, as it normally should,
it returns vector (p2.x*p1.x, p2.y*p1.y). Which is not at all intuitive.
We use:
       p1*p2 as scalar product, i.e. returns scalar
       p1@p2 as vector product, i.e. returns vector product # @ is python operator for matrix multiplication
       abs(p) = sqrt(p*p)
"""
import numpy as np
import cv2
import collections
import typing

class Base3DPoint(object):
    def __init__(self, numpy_1d_array : np.ndarray=None):
        if numpy_1d_array is None:
            self.asArray = np.array([0, 0, 0])
        else:
            if numpy_1d_array.shape[0] == 2:
                self.asArray = np.array([numpy_1d_array[0], numpy_1d_array[1], 0])
            else:
                self.asArray = numpy_1d_array

    @property
    def asArray(self) -> np.ndarray:
        return self._vector
    @asArray.setter
    def asArray(self, value):
        if not isinstance(value, np.ndarray):
            raise ValueError('Should be initialised with numpy 1d array')
        else:
            if len(value.shape)!=1 or value.shape[0]>3:
                raise ValueError('Expected 1d array with max 3 dimension')
        self._vector = np.append(value, np.zeros(3 - value.shape[0]))
    @property
    def x(self):
        return self._vector[0]
    @x.setter
    def x(self, value):
        self._vector[0] = value
    @property
    def y(self):
        return self._vector[1]
    @y.setter
    def y(self, value):
        self._vector[1] = value
    @property
    def z(self):
        return self._vector[2]
    @z.setter
    def z(self, value):
        self._vector[2] = value


class Point(Base3DPoint):

    @classmethod
    def init_x_y(cls, x: float, y: float):
        """Initialize Point from x, y values
            usage: Point.init_x_y( x=1.0, y=2.5)"""
        array = np.array([x, y])
        return cls(array)

    def __abs__(self):
        sum_of_squares = np.sum(self.asArray ** 2)
        return np.sqrt(sum_of_squares)

    def __add__(self, p : Base3DPoint):
        return Point(self.asArray + p.asArray)

    def __sub__(self, p : Base3DPoint):
        return Point(self.asArray - p.asArray)

    def __mul__(self, p):
        """ We return scalar or vector depending on second argument, as in normal math"""
        if isinstance(p, Base3DPoint):
            return np.dot(self.asArray, p.asArray)
        elif isinstance(p, (int, float)):
            return Point(self.asArray*p)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float or int):
        return Point(self.asArray / scalar)

    def __matmul__(self, p : Base3DPoint):
        """ We return vector product as in notmal math,
            see: http://mathworld.wolfram.com/CrossProduct.html"""
        x = self.y*p.z - self.z * p.y
        y = -self.x*p.z + self.z * p.x
        z = self.x*p.y - self.y*p.x
        return Point(np.array([x, y, z]))

class Rectangle2D(object):

    def __init__(self,
                 upper_left_point : Point=None,
                 bottom_right_point : Point=None):
        if upper_left_point is None:
            self._upper_left_point = Point()
        else:
            if isinstance(upper_left_point, Point):
                self._upper_left_point = upper_left_point
            else:
                raise ValueError('Wrong initialisation type')

        if bottom_right_point is None:
            self._bottom_right_point = Point()
        else:
            if isinstance(bottom_right_point, Point):
                self._bottom_right_point = bottom_right_point
            else:
                raise ValueError('Wrong initialisation type')

    @property
    def upper_left_point(self):
        return self._upper_left_point

    @upper_left_point.setter
    def upper_left_point(self, value:Point):
        self._upper_left_point = value

    @property
    def bottom_right_point(self):
        return self._bottom_right_point

    @bottom_right_point.setter
    def bottom_right_point(self, value:Point):
        self._bottom_right_point = value


class PixelMatrix(object):
    """ Wrapper around openCV and numpy library access, otherwise need to think in wrong
        reference frame. Here we have a bottom left as (0, 0), and normal coordinate axes,
        provided by numpy. Display is done by openCV with stupid reference frames.
        All interface with this object is in normal reference frame, what happens inside is
        internal business.
        Might be neccesary to switch to another library, rather than openCV, for a better look."""
    def __init__(self,
                 length: int,
                 height: int,
                 name: str=None):

        self.length = length
        self.height = height
        self.original_matrix = np.zeros((height, length, 3), np.uint8)
        self.name = name
        if self.name is None:
            self.name = 'Matrix'


    def add_rectangle(self,
                      rect: Rectangle2D,
                      line_thickness : int=2):
        # Need to think how to hanlde discrepancy in coordinate frame
        # surely I prefer mathematical coordinate frame better suited to humans, than computers

        rectangle_color = (255, 255, 255)
        rectangle_thickness = line_thickness
        # cv2.rectangle(self.swaped_matrix, (100, 100), (200, 200), color=(255, 255, 255), thickness=3)

        # correct transformation when adding points with numpy
        self.original_matrix[int(self.height - rect.bottom_right_point.y), int(rect.bottom_right_point.x)] = (255, 255, 255)
        self.original_matrix[int(self.height - rect.upper_left_point.y), int(rect.upper_left_point.x)] = (0, 255, 0)

        # correct transformation when adding points and shapes with openCV
        rect_bottom_right= self._point_to_cv2(rect.bottom_right_point)
        rect_upper_left = self._point_to_cv2(rect.upper_left_point)
        cv2.rectangle(self.original_matrix,
                      rect_bottom_right,
                      rect_upper_left,
                      color=(255, 255, 255),
                      thickness=rectangle_thickness)
        # cv2.rectangle(self.original_matrix, (100, 100), (120, 200), color=(255, 255, 255), thickness=3)

        print('bottom_right: ', int(rect.bottom_right_point.x), int(rect.bottom_right_point.y))
        print('upper_left: ', int(rect.upper_left_point.x), int(rect.upper_left_point.y))

        pass

    def add_text(self, box_for_text: Rectangle2D, text:str):
        rect_bottom_right = (int(box_for_text.bottom_right_point.x), int(self.height - box_for_text.bottom_right_point.y))
        rect_upper_left = (int(box_for_text.upper_left_point.x), int(self.height - box_for_text.upper_left_point.y))

        bottom_left_openCV = (rect_upper_left[0], rect_bottom_right[1])
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.original_matrix, text, bottom_left_openCV, font,
                    fontScale=0.5, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

    def add_line(self, start: Point, end: Point, line_thickness: int=1):
        cv2.line(self.original_matrix,
                 self._point_to_cv2(start),
                 self._point_to_cv2(end),
                 (255, 255, 255), line_thickness)

    def add_image(self, icon: np.ndarray,
                     high_point: Point,
                     low_point: Point):
        # low_point - not use ??
        """ Need to resize to fit, at the moment put as is"""
        x_offset, y_offset = self._point_to_cv2(high_point)
        print('ICON SIZE: ', icon.shape[0], icon.shape[1], x_offset, y_offset)
        # self.original_matrix[x_offset:x_offset + icon.shape[0], y_offset:y_offset + icon.shape[1]] = icon
        self.original_matrix[y_offset: y_offset + icon.shape[0], x_offset: x_offset + icon.shape[1]] = icon

    def display(self):
        # self._synchronise_matrixes()
        cv2.imshow(self.name, self.original_matrix)
        cv2.waitKey()

    def _point_to_cv2(self, point: Point) -> tuple:
        x = int(point.x)
        y = int(self.height - point.y)
        return x, y

    def save(self, file_name: str):
        cv2.imwrite(file_name, self.original_matrix)
