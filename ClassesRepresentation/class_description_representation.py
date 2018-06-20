import class_description

class_description.ClassDescription.root_path = r'D:/Literature/CASE'

MethodDescription_representation = class_description.ClassDescription(class_name='MethodDescription',
                                                                      file_name=r'class_description.py',
                                                                      line_start=5,
                                                                      line_end=26)

ClassDescription_representation = class_description.ClassDescription(class_name='ClassDescription',
                                                                     file_name=r'class_description.py',
                                                                     line_start=27,
                                                                     line_end=71)

all_classes = [
               MethodDescription_representation,
               ClassDescription_representation,
              ]

method = class_description.MethodDescription(
                                             method_name='to_list',
                                             line_start=19,
                                             line_end=26,
                                             variables=[],
                                             )
MethodDescription_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             liner_start=6,
                                             line_end=18,
                                             variables=[('method_name', 'str = None'), ('line_start', 'int = None'), ('line_end', 'int = None'), ('variables', 'list = None')],
                                             )
MethodDescription_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='add_method',
                                             line_start=46,
                                             line_end=53,
                                             variables=[('method', 'MethodDescription')],
                                             )
ClassDescription_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='plot',
                                             line_start=54,
                                             line_end=71,
                                             variables=[('matrix', 'MathObjects.PixelMatrix'), ('rectangle', 'interface.IDrawableRectangle')],
                                             )
ClassDescription_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=29,
                                             line_end=45,
                                             variables=[('class_name', 'str = None'), ('file_name', 'str = None'), ('line_start', 'int = None'), ('line_end', 'int = None')],
                                             )
ClassDescription_representation.add_method(method)

