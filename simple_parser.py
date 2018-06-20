import os
import class_description

# TODO Make object with global info, i.e. with such things as
# todo # all_classes_access_handler = integral_representation.all_classes
# todo # all_connections_access_handler - > represents connections, method to class,
# todo # such that it is easy to use for plotting: all_classes_access_handler[indi_class]._rectangle =>
# todo # all_classes_access_handler[indi_class].methods[key]
# todo # by having this we can extract positions from objects and plot everything

class GlobalStructureDescription(object):
    """ Should be a singltone, i.e. check design patterns"""
    def __init__(self):
        self.classes_access_handler = None
        self.connection_access_handler = None

        # fixme instead of this should be something more concise
        # import ClassesRepresentation.integral_representation as integral_representation
        # import ClassesRepresentation.inheritance_representation as inheritance_representation
        # import ClassesRepresentation.class_description_representation as class_description_representation
        #
        # all_classes_access_handler = integral_representation.all_classes
        # # all_classes_access_handler = inheritance_representation.all_classes
        # # all_classes_access_handler = class_description_representation.all_classes

# TODO Encapsulate in object
class ConnectionParser(object):
    """ Will operate on the results of File parser,
        I do not want to complicate the matter"""
    pass

class FileParser(object):
    """ Takes file as an input and parses it into representation of classes, found in it"""
    def __init__(self,
                 root_path: str,
                 relative_filename: str,
                 output_folder: str,
                 output_filename: str,
                 class_description_filename: str = 'class_description'):

        self.root_path = root_path
        self.input_filename = relative_filename
        self.output_folder = output_folder
        self.output_filename = output_filename
        self.class_description_filename = class_description_filename

        # read input as lines from file
        abs_file_path = os.path.join(self.root_path, self.input_filename)
        with open(abs_file_path) as f:
            self.content = f.readlines()

        # self.parsed_classes -> [ ClassDescription_representation, etc]
        # ClassDescription_representation = class_description.ClassDescription(class_name='ClassDescription',
        #                                                                      file_name=r'class_description.py',
        #                                                                      line_start=5,
        #                                                                      line_end=61)
        self.parsed_classes = self.classes_description_from_file(self.content, self.root_path)

        # Making an intermediate text representation with which it is easier to work with
        # in principle we can pickle objects and do not create these .py files, but
        # it would get too abstract for me
        self.lines_in_generated_file = []
        self.append_import_and_base_classes_description(self.class_description_filename)
        self.append_classes_as_a_list()

        # writing parsed representation to file
        self.filepath = os.path.join(self.root_path, self.output_folder, self.output_filename)
        # self.write_to_output_file(filepath)

    def write_to_output_file(self):
        with open(self.filepath, 'w') as file_handler:
            for item in self.lines_in_generated_file:
                file_handler.write("{}\n".format(item))

    def append_import_and_base_classes_description(self, import_filename_with_class_description:str):
        header = 'import ' + import_filename_with_class_description
        empty_spaces = ''
        self.lines_in_generated_file.append(header)
        self.lines_in_generated_file.append(empty_spaces)
        zero_string = empty_spaces + \
                      "class_description.ClassDescription.root_path = r'{0}'".format(self.parsed_classes[0].root_path)
        first_object_name = "{0}_representation".format(self.parsed_classes[0].class_name)
        self.lines_in_generated_file.append(zero_string)
        self.lines_in_generated_file.append(empty_spaces)
        for item in self.parsed_classes:
            first_string_part = empty_spaces + "{0}_representation = class_description.ClassDescription(".format(item.class_name)
            first_string = first_string_part + "class_name='{0}',".format(item.class_name)
            offset = ' ' * len(first_string_part)
            second_string = offset + "file_name=r'{0}',".format(item.file_name)
            third_string = offset + "line_start={0},".format(item.line_start)
            fourth_string = offset + "line_end={0},".format(item.line_end)
            fifth_string = offset + "child_of='{0}')".format(item.child_of)
            self.lines_in_generated_file.append(first_string)
            self.lines_in_generated_file.append(second_string)
            self.lines_in_generated_file.append(third_string)
            self.lines_in_generated_file.append(fourth_string)
            self.lines_in_generated_file.append(fifth_string)
            self.lines_in_generated_file.append(empty_spaces)

    def append_classes_as_a_list(self):
        class_line_first = 'all_classes = ['
        self.lines_in_generated_file.append(class_line_first)
        offset = '              '
        for item in self.parsed_classes:
            new_class_addition = offset + ' ' + item.class_name + '_representation' + ','
            self.lines_in_generated_file.append(new_class_addition)
        class_line_last = offset + ']'
        self.lines_in_generated_file.append(class_line_last)

        self.lines_in_generated_file.append('')

    def append_methods_description(self):
        new_lines = []
        for printed_class in self.parsed_classes:
            # print('Printing methods for class: ', printed_class.class_name)
            first_string = 'method = class_description.MethodDescription('
            offset = len(first_string) * ' '
            last_string = offset + ')'
            string_with_addition = printed_class.class_name + '_representation.add_method(' + 'method' + ')'
            for key in sorted(printed_class.methods): # as we want to have the same order all the time
                new_lines.append(first_string)
                for item in printed_class.methods[key].to_list():
                    right_format = "'{0}'".format(item[1]) if isinstance(item[1], str) else "{0}".format(item[1])
                    temp_string = offset + item[0] + right_format + ','
                    new_lines.append(temp_string)
                new_lines.append(last_string)
                new_lines.append(string_with_addition)
                new_lines.append('')

        self.lines_in_generated_file.extend(new_lines)

    def extract_methods_description_for_classes(self):
        # somehow need to take into account possibility of tabs and spaces
        # at the moment require 4 spaces
        method_starter = '    def'

        for current_class in self.parsed_classes:
            method_started = False
            current_method = None
            methods_information = []
            for index, line in enumerate(self.content[current_class.line_start: current_class.line_end]):
                check_result = self.line_parser(method_starter, line)
                if check_result == 'start':
                    if method_started:  # need to take into account, that start can represent another class start, i.e. end
                        current_method.line_end = index - 1 + current_class.line_start
                        methods_information.append(current_method)
                        method_started = False
                    method_started = True
                    method_name = self.name_extractor(method_starter, line)
                    current_method = class_description.MethodDescription(method_name=method_name,
                                                                         line_start=(index + current_class.line_start)
                                                                         )

                elif check_result == 'end' and method_started:
                    current_method.line_end = index - 1 + current_class.line_start
                    methods_information.append(current_method)
                    method_started = False

            if method_started:  # need to add the last one if class finishes, but we still have methods to add
                current_method.line_end = current_class.line_end
                methods_information.append(current_method)

            # print(methods_information)

            for method in methods_information:
                current_class.add_method(method)

    def extract_variables_description_for_methods(self):
        for printed_class in self.parsed_classes:
            for key in printed_class.methods:
                # current_method = printed_class.methods[key]
        #printed_class = self.parsed_classes[0]
        #key = '__init__'
                current_method = printed_class.methods[key]
                # print(current_method.to_list())
                # I have line where it starts
                # find parentesis there, then move on lines, till corresponding closing one(i.e. count additional open ones)
                # transform it into a line
                # transform it into the right format
                # append to variables
                # todo refactor it later as a function, i.e. restructure
                combined_line=''
                for line in self.content[current_method.line_start: current_method.line_end]:
                    # taking into account comments
                    comment_starts = line.find('#')
                    if comment_starts == -1:
                        shortened_line = line
                    else:
                        shortened_line = line[:comment_starts]
                    combined_line += shortened_line.replace('\r', '').replace('\n', '').strip()
                # print(combined_line)
                # finding open and closed brackets
                first_open_bracket_position, corresponding_close_bracket_position = \
                    self.extract_brackets_position(combined_line)

                if corresponding_close_bracket_position is None:
                    raise ValueError('Looks like not compilable file, no corresponding closed bracket'
                                     'for method on line {0} in file {1}'.format(current_method.line_start,
                                                                                 self.input_filename))
                # print('Closed bracket: ', corresponding_close_bracket_position,
                #                           combined_line[corresponding_close_bracket_position])
                # now transform (self,engine_manufacturer : str,start_probability : float)
                # to pairs [('engine_manufacturer', 'str'), ('start_probability', 'float')]
                separated_by_commas = [x.strip() for x in
                                       combined_line[first_open_bracket_position + 1:
                                       corresponding_close_bracket_position].split(',')]
                # print(separated_by_commas)
                # parsing into correct methods
                first_variable = separated_by_commas[0]
                finding_self = first_variable.find('self')
                if finding_self == -1:
                    raise ValueError('Self is not found for method on line {0} in file {1}'.format(current_method.line_start,
                                                                                                   self.input_filename))
                variables_list = []
                for line in separated_by_commas[1:]:
                    colon_position = line.find(':')
                    if colon_position == -1:
                        variable_name = line.strip()
                        variable_type = 'None'
                        variables_list.append((line.strip(), 'None'))
                    else:
                        variable_name = line[:colon_position].strip()
                        variable_type = line[colon_position + 1:].strip()
                    variables_list.append((variable_name, variable_type))
                # print(variables_list)
                # next line actually adds
                current_method.variables = variables_list
                # print(current_method.to_list())

    @staticmethod
    def line_parser(line_starts_with: str, line: str) -> str:  # pure function
        """ Checks it it starts with class, space, tab, comment or other"""

        if line is None:
            return 'empty'
        elif line.startswith(line_starts_with):
            return 'start'
        elif line[0] in [' ', '\t', '#', '\n']:
            return 'empty'
        else:
            print('End works: ', line)
            return 'end'

    @staticmethod
    def name_extractor(line_starter : str, line: str) -> str:  # pure function
        """ extracts class or method name from line:
            ex: class Example(SomeClass):  -> 'Example'
            ex: def some_method(self, params):  -> 'some_method'
        """
        line_length = len(line_starter)
        assert line[0:line_length] == line_starter
        i = line_length
        class_name = ''
        while line[i] != '(':
            if line[i] != ' ':
                class_name += line[i]
            i += 1
        return class_name

    @staticmethod
    def extract_brackets_position(line: str) -> (int, int):
        # finding open and closed brackets
        first_open_bracket_position = line.find('(')
        # print('Open bracket: ', first_open_bracket_position)
        open_brackets_number = 0
        corresponding_close_bracket_position = None
        for index, symbol in enumerate(line[first_open_bracket_position:]):
            if symbol == '(':
                open_brackets_number += 1
            if symbol == ')':
                open_brackets_number -= 1
            if open_brackets_number == 0:
                corresponding_close_bracket_position = index + first_open_bracket_position
                break

        return first_open_bracket_position, corresponding_close_bracket_position

    def classes_description_from_file(self, content_as_lines : list, root_path:str)-> list:  # pure function # -> list of ClassDescription
        """ Takes root_path where we have our project and relative filename of .py file
            produces classes description which are found there"""

        class_started = False
        classes_information = []
        current_class = None
        class_description.ClassDescription.root_path = root_path
        for index, line in enumerate(content_as_lines):
            check_result = self.line_parser('class', line)
            if check_result == 'start':
                if class_started:  # need to take into account, that start can represent another class start, i.e. end
                    current_class.line_end = index - 1
                    classes_information.append(current_class)
                    class_started = False
                class_started = True
                class_name = self.name_extractor('class', line)
                start, end = self.extract_brackets_position(line)
                parent_name = line[start + 1:end].strip()
                current_class = class_description.ClassDescription(class_name=class_name,
                                                                   file_name=relative_filename,
                                                                   line_start=index,
                                                                   child_of=parent_name)
            elif check_result == 'end' and class_started:
                current_class.line_end = index - 1
                classes_information.append(current_class)
                class_started = False
                print("This condition works!")

        return classes_information


if __name__ == '__main__':

    print('Here I add a simple parser, that transforms file into object init')

    # Input INFO for generation
    relative_filename = 'ObjectRelations\\association_relations.py'
    # relative_filename = 'ObjectRelations\\composition_relations.py'
    # relative_filename = 'ObjectRelations\\inheritance_relations.py'
    # relative_filename = 'class_description.py'
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # output files for generation
    # we will generate .py files
    output_folder = 'ClassesRepresentation'
    output_filename = 'integral_representation.py'
    # output_filename = 'inheritance_representation.py'
    # output_filename = 'class_description_representation.py'

    ObjToParseAFile = FileParser(
                             root_path=script_dir,
                             relative_filename=relative_filename,
                             output_folder=output_folder,
                             output_filename=output_filename)

    # TODO add methods description parsing
    ObjToParseAFile.extract_methods_description_for_classes()
    ObjToParseAFile.extract_variables_description_for_methods()
    ObjToParseAFile.append_methods_description()


    ObjToParseAFile.write_to_output_file()
    # TODO add connections compilation