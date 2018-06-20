import os
import copy


if __name__ == '__main__':
    print('It looks like I want to commit cleaned files, i.e. without comments and prints \n'
          'on the other hand for a developer version it is better that it has comments, \n'
          'a clean solution is to make an util that removes print() and comments # . \n'
          'It might be even possible to integrate it into workflow, so that a "clean commit" \n'
          'would clean source, check if it compiles as cleaning could break it and commit file')
    # NOTE this cleaning can break the code if we have stupid prints after for,
    # so you need to check that code is compiling after cleaning

    # clean source
    # if line starts with # or print( remove it
    input_full_path = r'D:\Literature\CASE\simple_parser.py'
    output_full_path = r'D:\Literature\CASE\clean_source_simple_parser.py'
    abs_file_path = os.path.join(input_full_path)
    with open(abs_file_path) as f:
        content = f.readlines()

    cleaned_version = []
    for line in content:
        no_tabs_and_spaces = copy.copy(line)
        no_tabs_and_spaces = no_tabs_and_spaces.replace('\r', '').replace('\n', '').strip()
        print(no_tabs_and_spaces)
        if not no_tabs_and_spaces:
            continue
        if no_tabs_and_spaces[0] == '#':
            continue
        print(no_tabs_and_spaces[:6])
        if no_tabs_and_spaces[:6] == 'print(':
            continue
        cleaned_version.append(line)

    for line in cleaned_version:
        print(line)

    with open(output_full_path , 'w') as file_handler:
        for item in cleaned_version:
            file_handler.write(item)