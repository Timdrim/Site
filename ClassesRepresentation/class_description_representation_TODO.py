import class_description

class_description.ClassDescription.root_path = r'D:/Literature/CASE'

ClassDescription_representation = class_description.ClassDescription(class_name='ClassDescription',
                                                                     file_name=r'class_description.py',
                                                                     line_start=5,
                                                                     line_end=61)

all_classes = [
               ClassDescription_representation,
              ]

# TODO
ClassDescription_representation.add_method(method_name='add_method',
                                           #TODO add @!!! static_method!!!
                                           line_start=25,
                                           line_end=43,
                                           variables=[
                                                      ('method_name', 'str'),
                                                      ('line_start', 'int'),
                                                      ('line_end', 'int'),
                                                      ('variables', 'list'),
                                                     ]
                                           )


