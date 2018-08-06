# -*- coding: utf-8 -*-
"""
Helper script to translate a problem_instance or a solution from German into English or the other way around.

Usage:
- Execute as script to translate files, or a whole directory, and get back translated files. Type 'python translate.py -h' for usage instructions.
- For interactive use in a Python session, import the module and use the 'translate_scenario_file' function to translate deserialized JSON-instances.
"""
import json
import csv
import collections.abc
import pathlib
import argparse
import sys




# build the translation dicts
############################################################################################################
def setup_translation_table(file):
    GER_2_ENG = dict()
    ENG_2_GER = dict()
    with open(file, encoding='utf-8') as fp:
        a = csv.reader(fp, skipinitialspace=True)
        next(a)  # skip first line
        for ger, eng in a:
            GER_2_ENG[ger] = eng
            ENG_2_GER[eng] = ger
    return GER_2_ENG, ENG_2_GER
############################################################################################################

# main function that does the translation recursively
############################################################################################################
def translate(d, translation_function):
    """
    Convert a problem_instance or a solution from German into English, or vice-versa


    Args:
        d (dict): The deserialized JSON of a problem_instance or a solution. E.g. as obtained from json.load(path-to-problem-instance)
        translation_function (func): function that translates a key into another language. Either 'translate_to_eng' or 'translate_to_ger'
    Returns:
        Dictionary with the translated keys.
    """
    new = dict()
    for k, v in d.items():
        new_v = v
        if k == "parameters":  # do not translate parameters
            new[k] = v
            continue

        if isinstance(v, collections.abc.Mapping):
            new_v = translate(v, translation_function)

        elif isinstance(v, collections.abc.MutableSequence) and len(v) > 0 and isinstance(v[0], dict):  # we have some "trivial" lists, like abschnittskennzeichen = ["C"]. Don't call recursion for these
            new_v = list()
            for x in v:
                new_v.append(translate(x, translation_function))
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

def translate_to_ger(key):
    #print(f"translating {key}")
    try:
        return ENG_2_GER[key]
    except KeyError:
        print(f"WARNING: don't know how to translate {key}. I will leave it as is.")
        return key

def translate_message_to_eng(key):
    #print(f"translating {key}")
    try:
        return GER_2_ENG_MESSAGE[key]
    except KeyError:
        # print(f"WARNING: don't know how to translate '{key}''. I will leave it as is. [Message]")
        return key
############################################################################################################

# translate functions for the message
############################################################################################################
def translate_message_word_for_word(validation_result):
    i = 0
    for violation in validation_result['business_rules_violations']:
        validation_result['business_rules_violations'][i]['message_original'] = violation['message']
        for word in violation['message'].split():
            validation_result['business_rules_violations'][i]['message'] = violation['message'].replace(word, translate_message_to_eng(word))
        i += 1

    return validation_result

############################################################################################################

# Helper function
def write_json(d, path, suffix=""):
    out_file = path.parent / (str(path.stem) + out_suffix + str(path.suffix))
    with out_file.open("w") as fp:
        json.dump(d, fp, indent="\t")
    print(f"Wrote file {out_file}")


GER_2_ENG, ENG_2_GER = setup_translation_table("translation_table.csv")
GER_2_ENG_MESSAGE, ENG_2_GER_MESSAGE = setup_translation_table("translation_message_table.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='translate.py')
    parser.add_argument("path", help="path to directory (or individual file) to be translated. If a directory, each path in it will be translated (non-recursively). For this to work each path must be a JSON-path conforming to either the challenge input or output data model")
    parser.add_argument("from_into",
                        choices=["GER->ENG", "ENG->GER"],
                        help="tuple (from-language -> into-language) of the languages. Allowed are GER->ENG for translating German into English and vice-versa ENG->GER")
    args = parser.parse_args()

    try:
        path = pathlib.Path(args.path)
    except Exception as e:
        print(f"Error: Can't create path for {args.path}. \n {e}")
        sys.exit(1)
    else:  # determine all files to be translated
        if path.is_dir():
            to_translate = path.glob('*.json')
        elif path.is_file():
            to_translate = [path]  # make it iterable by turning it into a one-element-list

        # translate each file
        for s in to_translate:
            try:
                with open(s) as fp:
                    d = json.load(fp)
            except Exception as e:
                print(f"Unable to deserialize {args.path}. Is it a valid JSON?")
                sys.exit(1)
            else:  # everything's fine, can translate
                print(f"Translating {s}: {args.from_into}...")
                if args.from_into == "GER->ENG":
                    out_suffix = "_eng"
                    translated = translate(d, translate_to_eng)
                else:  # translate to German
                    out_suffix = "_ger"
                    translated = translate(d, translate_to_ger)

                write_json(translated, path=s, suffix=out_suffix)
