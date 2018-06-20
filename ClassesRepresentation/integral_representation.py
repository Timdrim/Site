import class_description

class_description.ClassDescription.root_path = r'C:/My_CASE1'

Engine_representation = class_description.ClassDescription(class_name='Engine',
                                                           file_name=r'ObjectRelations\association_relations.py',
                                                           line_start=3,
                                                           line_end=25,
                                                           child_of='object')

Automobile_representation = class_description.ClassDescription(class_name='Automobile',
                                                               file_name=r'ObjectRelations\association_relations.py',
                                                               line_start=30,
                                                               line_end=47,
                                                               child_of='object')

all_classes = [
               Engine_representation,
               Automobile_representation,
              ]

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=5,
                                             line_end=10,
                                             variables=[('engine_manufacturer', 'str'), ('start_probability', 'float')],
                                             )
Engine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='engine_manufacturer',
                                             line_start=22,
                                             line_end=25,
                                             variables=[],
                                             )
Engine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='startWorking',
                                             line_start=11,
                                             line_end=21,
                                             variables=[],
                                             )
Engine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=32,
                                             line_end=35,
                                             variables=[('manufacturer', 'str')],
                                             )
Automobile_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='manufacturer',
                                             line_start=45,
                                             line_end=47,
                                             variables=[],
                                             )
Automobile_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='move',
                                             line_start=36,
                                             line_end=44,
                                             variables=[('engine_to_launch', 'Engine')],
                                             )
Automobile_representation.add_method(method)

