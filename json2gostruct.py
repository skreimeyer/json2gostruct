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
import pdb
from random import randint


types = {
    "int": "int",
    "float": "float64",
    "str": "string",
    "bool": "bool",
    "dict": "map[string]interface{}",
    "NoneType": "int", # This is wrong, but nil is not a valid type in go
    "list":"[]interface{}"
}


def make_struct(name, data):
    # pdb.set_trace()
    struct_lines = []
    struct_lines.append(f"type {name} struct {{")
    if isinstance(data, list):
        struct_lines.append(make_list_field(None, data))
    if isinstance(data,dict):
        for k, v in data.items():
            if isinstance(v, dict):
                struct_lines.append(f'{k.lower().title().replace("_","").replace(".","")} {k} `json:"{k}"`')
                make_struct(k, v)
            elif isinstance(v, list):
                struct_lines.append(make_list_field(k, v))
            else:
                field_name = k.lower().title().replace("_","").replace(".","")
                gotype = types[type(v).__name__]
                annotation = f'`json:"{k}"`'
                struct_lines.append(f"{field_name} {gotype} {annotation}")
    struct_lines.append("}")
    [print(l) for l in struct_lines]
    print("\n")
    return None


def make_list_field(keyname, listobj):
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
    # pdb.set_trace()
    if not keyname:
        keyname = "node"
        annotation = '`json:""`'
    else:
        annotation = None # avoid reference before assignment
    if len(set([type(l) for l in listobj])) == 1 and isinstance(listobj[0],dict):
        # We aren't actually testing if all keys are the same.
        make_struct(keyname,listobj[0])
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
    elif not False in [isinstance(i,list) for i in listobj]:
        recursed_field = make_list_field(keyname,listobj[0])
        insert_index = len(keyname)+1
        return recursed_field[:insert_index]+"[]"+recursed_field[insert_index:]
    # Case: Same type primitives or maps with dissimilar keys
    else:
        field_name = keyname
        gotype = types[type(listobj[0]).__name__]
        annotation = f'`json:"{keyname}"`' if not annotation else annotation
        return f'{field_name.lower().title().replace("_","").replace(".","")} []{gotype} {annotation}'


if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)
    except:
        print("Invalid json data read from std input!", file=sys.stderr)
        exit()
    make_struct("root", data)
    exit()
