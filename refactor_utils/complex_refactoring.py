

if __name__ == '__main__':

    print('Idea is to make complex refactoring, i.e. not just renaming, '
          'but template matching, example: \n' +
          """upper_left_of_rectangle_for_class_name = MathObjects.Point(
                                      np.array([majour_upper_left_point.x + line_thickness,
                                                majour_upper_left_point.y - line_thickness])
                                                       )
          into:
          upper_left_of_rectangle_for_class_name = MathObjects.Point.init_x_y(
                                                 x=majour_upper_left_point.x + line_thickness,
                                                 y=majour_upper_left_point.y - line_thickness)
          We decrease cognitive load a little bit by that.""")