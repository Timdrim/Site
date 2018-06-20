import class_description

class_description.ClassDescription.root_path = r'D:/Literature/CASE'

Engine_representation = class_description.ClassDescription(class_name='Engine',
                                                           file_name=r'ObjectRelations\association_relations.py',
                                                           line_start=3,
                                                           line_end=25)

Automobile_representation = class_description.ClassDescription(class_name='Automobile',
                                                               file_name=r'ObjectRelations\association_relations.py',
                                                               line_start=30,
                                                               line_end=47)

all_classes = [
               Engine_representation,
               Automobile_representation,
              ]

# TODO
def __init__(self,
                 engine_manufacturer : str,
                 start_probability : float):
# need to add text form, otherwise it's impossible to debug, i.e. too complex
# make a template

    ClassDescription_representation.add_method(method_name='add_method',
                                               # TODO add @!!! static_method!!!
                                               line_start=25,
                                               line_end=43,
                                               variables=[
                                                   ('method_name', 'str'),
                                                   ('line_start', 'int'),
                                                   ('line_end', 'int'),
                                                   ('variables', 'list'),
                                               ]
                                               )