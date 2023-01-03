import argparse
import sys
import os
import json


def arg_parser():
    parser = argparse.ArgumentParser(description='   ')
    parser.add_argument('-p', '--project',  required=True, type=str, choices=get_projects(), help='')
    parser.add_argument('-b', '--bug-no',   required=True, type=int, help='')
    parser.add_argument('-t', '--task',     required=True, type=str, choices=['checkout', 'install', 'test', 'test-changed'], help='')
    parser.add_argument('-f', '--file',     required=False, type=str, help='')
    parser.add_argument('-v', '--version',  required=True, type=str, choices=['buggy', 'fixed', 'bug_with_test'], help='')
    parser.add_argument('-o', '--output',   required=False, type=str, help='output folder')

    param_dict = {}
    args = parser.parse_args()
    param_dict["project"] = args.project
    param_dict["bug-no"] = args.bug_no
    param_dict["version"] = args.version
    param_dict["task"] = args.task
    param_dict["file"] = args.file
    param_dict["output"] = args.output
    return param_dict


def get_projects():
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    projects_set = set()
    bug_file = open(os.path.join(SCRIPTDIR, "test_bug_metadata.json"), "r")
    bug_list = json.load(bug_file)
    for bug in bug_list:
        projects_set.add(bug["owner"] + '--' + bug['repo_name'])
    bug_file.close()
    return list(projects_set)
