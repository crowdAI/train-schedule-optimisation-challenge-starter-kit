import json
import csv
import collections.abc
import pathlib
import argparse
import sys


# build the translation dicts
############################################################################################################
GER_2_ENG = dict()
ENG_2_GER = dict()
with open("translation_table.csv") as fp:
    a = csv.reader(fp, skipinitialspace=True)
    next(a)  # skip first line
    for ger, eng in a:
        GER_2_ENG[ger] = eng
        ENG_2_GER[eng] = ger
############################################################################################################

# main function that does the translation recursively
############################################################################################################
def translate_scenario_file(d, translation_function):
    """
    Convert a nested dictionary from one language to another.
    Args:
        d (dict): SBB scenario file to be converted.
        translation_function (func): function that translates a key into another language
    Returns:
        Dictionary with the new keys.
    """
    new = dict()
    for k, v in d.items():
        new_v = v
        if k == "parameters":  # do not translate parameters
            # print("i'm in parameters, skip them")
            new[k] = v
            continue

        if isinstance(v, collections.abc.Mapping):
            # print(f"treating a {k}, it has a dict as value")
            # print(v)
            new_v = translate_scenario_file(v, translation_function)

        elif isinstance(v, collections.abc.MutableSequence) and len(v) > 0 and isinstance(v[0], dict):  # we have some "trivial" lists, like abschnittskennzeichen = ["C"]. Don't call recursion for these
            # print(f"treating {k}, it has a list as value")
            # print(v)
            new_v = list()
            for x in v:
                new_v.append(translate_scenario_file(x, translation_function))
        new[translation_function(k)] = new_v
    return new
############################################################################################################

# translation functions
############################################################################################################
def translate_to_eng(key):
    #print(f"translating {key}")
    try:
        return GER_2_ENG[key]
    except KeyError:
        print(f"WARNING: don't know how to translate '{key}''. I will leave it as is.")
        return key
        # raise Exception(f"cant' translate {key}")

def translate_to_ger(key):
    #print(f"translating {key}")
    try:
        return ENG_2_GER[key]
    except KeyError:
        print(f"WARNING: don't know how to translate {key}. I will leave it as is.")
        return key
        # raise Exception(f"cant' translate {key}")
############################################################################################################

# convert a single scenario
############################################################################################################
# file = pathlib.Path("../sample_files/sample_scenario.json")
#
# with open(file) as fp:
#     to_translate = json.load(fp)
#
# translated = translate_scenario_file(to_translate, translate_to_eng)
#
# # dump the json if desired
# out_suffix = "_eng"  # e.g. filename.json will be translated into filename_eng.json
# out_file = file.parent / (str(file.stem) + out_suffix + str(file.suffix))
#
# with out_file.open("w") as fp:
#     json.dump(translated, fp)
############################################################################################################

# convert all json-files in a directory.
############################################################################################################
# directory = pathlib.Path.cwd()/"samples"/"problem_instances"
# out_directory = directory  # write translated scenarios into this directory
# out_suffix = "_eng"  # e.g. filename.json will be translated into filename_eng.json
# g = directory.glob('*.json')
#
# for file in g:
#     print("translating " + file.name)
#     with file.open() as fp:
#         to_translate = json.load(fp)
#     translated = translate_scenario_file(to_translate, translate_to_eng)
#
#     out_file = directory / (str(file.stem) + out_suffix + str(file.suffix))
#     with out_file.open("w") as fp:
#         json.dump(translated, fp)
############################################################################################################

if __name__ == "__main__":
    print("entering main")
    parser = argparse.ArgumentParser(prog='translate.py')
    parser.add_argument("file", help="path to the file to be translated. Must be a JSON in problem instance or solution data format")
    parser.add_argument("from_into",
                        choices=["GER->ENG", "ENG->GER"],
                        help="tuple (from-language -> into-language) of the languages to be translated. Allowed are GER->ENG for translating German into English and vice-versa ENG->GER")
    args = parser.parse_args()

    try:
        with open(args.file) as fp:
            d = json.load(fp)
    except Exception as e:
        print(f"Unable to deserialize {args.file}. Is it a valid JSON?")
        sys.exit(1)

    if args.from_into == "GER->ENG":
        print("translating German to English")
        translated = translate_scenario_file(d, translate_to_eng)

    else:
        print("Translateing English to German")
        translated = translate_scenario_file(args.file, translate_to_ger)

    # ToDo: Dump it out