import class_description

class_description.ClassDescription.root_path = r'D:/Literature/CASE'

ManufacturedObject_representation = class_description.ClassDescription(class_name='ManufacturedObject',
                                                                       file_name=r'ObjectRelations\inheritance_relations.py',
                                                                       line_start=3,
                                                                       line_end=12,
                                                                       child_of='object')

ObjectWithInternalEngine_representation = class_description.ClassDescription(class_name='ObjectWithInternalEngine',
                                                                             file_name=r'ObjectRelations\inheritance_relations.py',
                                                                             line_start=13,
                                                                             line_end=27,
                                                                             child_of='ManufacturedObject')

Engine_representation = class_description.ClassDescription(class_name='Engine',
                                                           file_name=r'ObjectRelations\inheritance_relations.py',
                                                           line_start=28,
                                                           line_end=41,
                                                           child_of='ObjectWithInternalEngine')

Automobile_representation = class_description.ClassDescription(class_name='Automobile',
                                                               file_name=r'ObjectRelations\inheritance_relations.py',
                                                               line_start=42,
                                                               line_end=58,
                                                               child_of='ManufacturedObject')

all_classes = [
               ManufacturedObject_representation,
               ObjectWithInternalEngine_representation,
               Engine_representation,
               Automobile_representation,
              ]

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=4,
                                             line_end=8,
                                             variables=[('manufacturer_name', 'str')],
                                             )
ManufacturedObject_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='manufacturer_name',
                                             line_start=9,
                                             line_end=12,
                                             variables=[],
                                             )
ManufacturedObject_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=15,
                                             line_end=20,
                                             variables=[('manufacturer_name', 'str'), ('start_probability', 'float')],
                                             )
ObjectWithInternalEngine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='launch_engine',
                                             line_start=21,
                                             line_end=27,
                                             variables=[],
                                             )
ObjectWithInternalEngine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=29,
                                             line_end=33,
                                             variables=[('manufacturer_name', 'str'), ('start_probability', 'float')],
                                             )
Engine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='start_working',
                                             line_start=34,
                                             line_end=41,
                                             variables=[],
                                             )
Engine_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='__init__',
                                             line_start=44,
                                             line_end=49,
                                             variables=[('manufacturer_name', 'str'), ('internal_engine', 'Engine')],
                                             )
Automobile_representation.add_method(method)

method = class_description.MethodDescription(
                                             method_name='move',
                                             line_start=50,
                                             line_end=58,
                                             variables=[],
                                             )
Automobile_representation.add_method(method)

