import os
import subprocess as sp
import sys
import json


def checkout(param_dict):
    bug_info = get_bug_info(param_dict)
    extract_repo(bug_info, param_dict["output"])

    checkout_cmd = None
    if(param_dict["version"] == "buggy"):
        checkout_cmd = "git checkout -f " + bug_info['buggy_commit_id']
    elif(param_dict["version"] == "fixed"):
        checkout_cmd = "git checkout -f " + bug_info['fixed_commit_id']
    elif(param_dict["version"] == "bug_with_test"):
        checkout_cmd = "git checkout -f " + bug_info['bug_with_test_commit_id']
    else:
        exit()
    sp.call(checkout_cmd, shell=True)


def get_bug_info(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    print(SCRIPTDIR)
    with open(os.path.join(SCRIPTDIR, "test_bug_metadata.json"), 'r') as infile:
        bug_list = json.load(infile)
        for bug in bug_list:
            if(param_dict["project"] == bug["owner"] + '--' + bug['repo_name'] and bug['bug_no'] == param_dict['bug-no']):
                return bug
    print("I can't find the bug in the json file")
    exit()


def extract_repo(bug_info, folder):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

    if os.path.isdir(folder):
        rm_cmd = "rm -R "+str(folder)
        sp.call(rm_cmd, shell=True)
    os.makedirs(folder)

    os.chdir(folder)
    extract_cmd = "7z x " + SCRIPTDIR + "/test_repositories.7z " + "-o" + folder + " " + os.path.join("test_repositories", bug_info['owner'] + "--" + bug_info['repo_name'], bug_info['repo_name']) + "/*.* -r -y"
    sp.call(extract_cmd, shell=True)

    move_cmd = "mv " + os.path.join(folder, 'test_repositories',
                                    bug_info['owner'] + "--" + bug_info['repo_name'], bug_info['repo_name']) + " " + folder
    sp.call(move_cmd, shell=True)

    delete_cmd = "rm -r " + os.path.join(folder, 'test_repositories')
    sp.call(delete_cmd, shell=True)

    os.chdir(os.listdir("./")[0])
