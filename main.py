import argument_parser
import myGit
import myTest

param_dict = argument_parser.arg_parser()
if(param_dict["task"] == "checkout"):
    myGit.checkout(param_dict)
elif(param_dict["task"] == "install"):
    myTest.install(param_dict)
elif(param_dict["task"] == "test"):
    myTest.run_all_test(param_dict)
elif(param_dict["task"] == "test-changed" and param_dict["file"]):
    myTest.run_test_file(param_dict)
elif(param_dict["task"] == "test-changed"):
    myTest.run_test_only_changed_test_files(param_dict)
