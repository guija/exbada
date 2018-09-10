import argparse
import os
import re
import json
import csv
import itertools

class DotWriter:

    def __init__(self, file_path):
        self.file_path = file_path        

    def writeAnalyzer(self, analyzer):

        with open(self.file_path, 'a+') as file:

            file.write("digraph {\n")

            for program in analyzer.programs:
                file.write('\t%s [type="program"];\n'% program)

            for data_element in analyzer.data_elemets:
                file.write('\t%s [type="data_element"];\n'% data_element)

            for interface in analyzer.interfaces:
                file.write('\t%s [type="interface"];\n'% interface)

            file.write("\n")

            for connection in analyzer.connections:
                file.write("\t%s -> %s;\n" % connection)

            file.write("}\n")        

class Analyzer:
    
    def __init__(self):
        self.data_elemets = set()
        self.programs = set()
        self.interfaces = set()
        self.connections = [] # list of tuples meaning edges between interfaces programs etc.
        self.node_attributes = {} # dictionary with nodes names (eg. program, interface or data_element) keys and lists as values

    def analyze(self, file_path, content):
        # TODO replace with logging
        print("Analyzing %s" % file_path)
        self.extractProgramDependencies(file_path, content)
        self.extractDataDependencies(file_path, content)
        self.extractInterfaceDependiencies(file_path, content)

    def get_program_name(self, file_path, content):
        return os.path.basename(file_path)

    def extractDataDependencies(self, file_path, content):
        pass

    def extractProgramDependencies(self, file_path, content):
        pass

    def extractInterfaceDependiencies(self, file_path, content):
        pass

# TODO
class Pl1Analyzer(Analyzer):
    pass

class CobolAnalyzer(Analyzer):
    
    helper_programs = {}

    technical_data_fields = {}

    def get_program_name(self, file_path, content):
        return os.path.basename(file_path).replace(".cbl", "")

    def extractDataDependencies(self, file_path, content):

        caller_name = self.get_program_name(file_path, content)
        matches = re.finditer(r'(\w+-\w+-\w+)', content)

        for match in matches:

            data_field_name = match.group(1)

            # replace "-" because dot doesnt like "-"
            data_field_name = data_field_name.replace("-", "_")

            if data_field_name in CobolAnalyzer.technical_data_fields:
                continue

            self.data_elemets.add(data_field_name)
            self.connections.append((caller_name, data_field_name))

    def extractProgramDependencies(self, file_path, content):

        caller_name = self.get_program_name(file_path, content)
        self.programs.add(caller_name)
        matches = re.finditer(r'CALL\s+(\w+)', content)

        for match in matches:

            callee_name = match.group(1)
            callee_name = "B1%s" % callee_name

            if callee_name in CobolAnalyzer.helper_programs:
                continue

            self.connections.append((caller_name, callee_name))

    def extractInterfaceDependiencies(self, file_path, content):
        pass

def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def main():

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("folder_paths", nargs='+', help="Input folders with sources", type=str)
    argument_parser.add_argument("--dot", required=True, help="Dot output file name", type=str)
    args = argument_parser.parse_args()

    remove_file_if_exists(args.dot)

    analyzer = CobolAnalyzer()

    # todo recursive or multiple input?

    for folder_path in args.folder_paths:

        for file_name in os.listdir(folder_path):

            file_path = os.path.join(folder_path, file_name)

            with open(file_path, 'r') as file:

                content = file.read()
                analyzer.analyze(file_path, content)

    dot_writer = DotWriter(args.dot)
    dot_writer.writeAnalyzer(analyzer)

if __name__ == '__main__':
    main()