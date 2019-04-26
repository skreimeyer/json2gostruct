#! /usr/bin/env python3

"""
json2struct reads a json file and attempts to generate sensible structs
for the go language. When dealing with unfamiliar APIs that produce deeply
nested responses, defining a data structure to unmarshal the response into is
really a nuisance. Ideally, this script will provide reasonably named structs
that require minimal tweaking for use in go source code.

if executed as main, json2gostruct will read from stdin and write to stdout for
pipelining.

Basic usage:

curl "http://some.api" | json2gostruct.py >> program.go

"""

import sys
import json
import argparse


types = {
    "int": "int",
    "float": "float64",
    "str": "string",
    "bool": "bool",
    "dict": "map[string]interface{}",
    "NoneType": "int",  # This is wrong, but nil is not a valid type in go
    "list": "[]interface{}",
}


class StructFactory:
    """
    StructFactory holds the methods for the basic functionality of the script.
    This class exists to allow the functions below to share variables passed
    through the command line.

    Use cases might arise where it is desirable to prefix the structs with a
    short string to prevent name-collision where structs generated from multiple
    JSON files with overlapping keys need to be used in the same Go package
    """
    def __init__(self, args):
        if args.prefix:
            self.prefix = args.prefix
        else:
            self.prefix = ""

    def make_struct(self, name, data):
        """
        make_struct is the core functionality of this script. It uses
        recursion to traverse a nested data-structure (ie "data" arg). JSON
        does not by nature have any consistent structure, so at each level
        handling must be provided for the different possible types.

        In brief, an empty list which becomes populated with formatted
        strings is made at the head of the function, and the end of the loop
        returns the joined string which will look something like:

        type name struct {
            JsonKeyName type `json:\"raw_json_key_name\"`
        }
        """
        struct_lines = []
        struct_lines.append(f"type {self.prefix}{name} struct {{")
        if isinstance(data, list):
            struct_lines.append(self.make_list_field(None, data))
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    struct_lines.append(
                        f'{k.lower().title().replace("_","").replace(".","")} {self.prefix}{k} `json:"{k}"`'
                    )
                    self.make_struct(k, v)
                elif isinstance(v, list):
                    struct_lines.append(self.make_list_field(k, v))
                else:
                    field_name = k.lower().title().replace("_", "").replace(".", "")
                    gotype = types[type(v).__name__]
                    annotation = f'`json:"{k}"`'
                    struct_lines.append(
                        f"{field_name} {gotype} {annotation}"
                    )
        struct_lines.append("}")
        [print(l) for l in struct_lines]
        print("\n")
        return None

    def make_list_field(self, keyname, listobj):
        """
        Lists are a real problem for creating reasonable structs. Objects are not
        required to be uniform within a JSON array, so you could potentially have
        the problem of trying to describe a struct field which contains different
        primitive or nested types. This means that we ideally need a field
        which is an array of empty interfaces but also allows unmarshaling of the
        JSON array objects into appropriate structs.

        I don't see a clear solution to this, so for now, all this will do is
        check the list types and make an appropriate array
        """
        # Case: List of homogenous objects
        if not keyname:
            keyname = "node"
            annotation = '`json:""`'
        else:
            annotation = None  # avoid reference before assignment
        if len(set([type(l) for l in listobj])) == 1 and isinstance(listobj[0], dict):
            # We aren't actually testing if all keys are the same.
            self.make_struct(keyname, listobj[0])
            # we're just going to ignore divergent nesting
            gotype = keyname
            annotation = f'`json:"{keyname}"`' if not annotation else annotation
            return f'{keyname.lower().title().replace("_","").replace(".","")} []{gotype} {annotation}'
        # Case: Disparate types
        elif len(set([type(l) for l in listobj])) > 1:
            field_name = keyname
            gotype = "interface{}"
            annotation = '`json:""`'
            return f'{field_name.lower().title().replace("_","").replace(".","")} []{gotype} {annotation}'
        # Case: List of lists
        elif not False in [isinstance(i, list) for i in listobj]:
            recursed_field = self.make_list_field(keyname, listobj[0])
            insert_index = len(keyname) + 1
            return recursed_field[:insert_index] + "[]" + recursed_field[insert_index:]
        # Case: Same type primitives or maps with dissimilar keys
        else:
            field_name = keyname
            gotype = types[type(listobj[0]).__name__]
            annotation = f'`json:"{keyname}"`' if not annotation else annotation
            return f'{field_name.lower().title().replace("_","").replace(".","")} []{gotype} {annotation}'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a JSON from stdin and write Golang structs to stdout"
    )
    parser.add_argument(
        "-p",
        "--prefix",
        help="""
        add a short prefix to all struct names (this is helpful when you're making structs from multiple JSON files that have the same keynames
        """,
    )
    args = parser.parse_args()
    try:
        data = json.load(sys.stdin)
    except:
        print("Invalid json data read from std input!", file=sys.stderr)
        exit()
    SF = StructFactory(args)
    SF.make_struct("root", data)
    exit()
