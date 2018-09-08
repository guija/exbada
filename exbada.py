import argparse
import os
import re

graph_file_name = 'graph.dot'

def write_dot(line):
    with open(graph_file_name, 'a+') as dot_file:
        dot_file.writelines([line + "\n"])

def remove_dot_file():
    if os.path.exists(graph_file_name):
        os.remove(graph_file_name)

def main():

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("source_folder", help="Input folder with sources", type=str)
    args = argument_parser.parse_args()

    remove_dot_file()
    process_source_folder(args.source_folder)

def process_source_folder(source_folder):

    # todo recursive digging? maybe depending on an argument

    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        process_file(file_path)

def process_file(file_path):

    processed_program_name = get_program_name_from_path(file_path)

    print(processed_program_name)

    with open(file_path, 'r') as file:

        content = file.read()

        for match in re.finditer(r'CALL\s+WXX-(\w+)', content):
            called_program_name = match.group(1)
            called_program_name = "B1%s" % called_program_name
            print("\t", called_program_name)
            write_dot("%s -> %s" % (processed_program_name, called_program_name))

# todo in parser file / module eigene klasse extrahieren
def get_program_name_from_path(path):
    file_name = os.path.basename(path)
    m = re.match(r'(\w+)\.cbl', file_name)
    return m.group(1)

if __name__ == '__main__':
    main()