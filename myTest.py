import myProject
import os
import subprocess as sp
import sys


def get_installed_php_version():
    out, err = sp.Popen('php -v', shell=True, universal_newlines=True, stdin=sp.PIPE,
                        stdout=sp.PIPE, stderr=sp.PIPE).communicate()
    if(err):
        return None
    else:
        version = out.split(' ')[1].split('.')[0] + '.' + out.split(' ')[1].split('.')[1]
        return version


def install_php(bug):
    installed_php_version = get_installed_php_version()

    if(installed_php_version == bug['version']['php']):
        return
    elif(installed_php_version):
        uninstall_cmd = "apt --purge autoremove php{version} php{version}-mbstring php{version}-xml php{version}-curl php{version}-xdebug php{version}-redis php{version}-mysql php{version}-dev".format(version=installed_php_version)
        sp.call(uninstall_cmd, shell=True)

        install_cmd = "apt install php{version} php{version}-mbstring php{version}-xml php{version}-curl php{version}-redis php{version}-mysql".format(version=bug['version']['php'])
        sp.call(install_cmd, shell=True)
        sp.call("phpenmod pdo_mysql", shell=True)
    else:
        sp.call("add-apt-repository ppa:ondrej/php -y", shell=True)
        sp.call("apt install software-properties-common", shell=True)

        install_cmd = "apt install php{version} php{version}-mbstring php{version}-xml php{version}-curl php{version}-redis php{version}-mysql".format(version=bug['version']['php'])
        sp.call(install_cmd, shell=True)
        sp.call("phpenmod pdo_mysql", shell=True)


def install(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name'])):
        print("can't find the project folder")
        exit()

    install_php(bug_info)

    os.chdir(os.path.join(param_dict['output'], bug_info['repo_name']))

    sp.call("""php -r 'copy("https://getcomposer.org/installer", "composer-setup.php");'""", shell=True)
    sp.call("""if (hash_file('sha384', 'composer-setup.php') === '55ce33d7678c5a611085589f1f3ddf8b3c52d662cd01d4ba75c0ee0459970c2200a51f492d557530c71c15d8dba01eae') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;""", shell=True)
    sp.call("php composer-setup.php", shell=True)
    sp.call("""php -r 'unlink("composer-setup.php");'""", shell=True)
    sp.call("php composer.phar config --no-plugins allow-plugins true", shell=True)

    if(bug_info['version']['composer'].startswith('1.')):
        sp.call("php composer.phar self-update 1.10.26", shell=True)
        sp.call("php composer.phar install --no-interaction --no-cache --no-progress --quiet", shell=True)
    else:
        sp.call("php composer.phar self-update 2.5.1", shell=True)
        sp.call("php composer.phar install --no-interaction --no-cache --no-progress --quiet --ignore-platform-req=ext-foobar --ignore-platform-req=ext-pcre --ignore-platform-req=ext-foobar --ignore-platform-req=ext-pcre", shell=True)


def run_all_test(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if(not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name']))):
        print("can't find the project folder")
        exit()

    os.chdir(os.path.join(param_dict['output'], bug_info['repo_name']))

    test_script_cmd = ''
    if(bug_info['test_script'][param_dict['version']]):
        test_script_cmd = 'php composer.phar run-script --timeout 0 ' + bug_info['test_script'][param_dict['version']]
    else:
        test_script_cmd = 'vendor/bin/phpunit ' + os.path.join(param_dict['output'], bug_info['repo_name'], bug_info['test_folder'])

    try:
        print(test_script_cmd)
        sp.call(test_script_cmd, shell=True)
    except Exception as e:
        print(e)


def run_test_only_changed_test_files(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if(not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name']))):
        print("can't find the project folder")
        exit()

    os.chdir(os.path.join(param_dict['output'], bug_info['repo_name']))

    for test_file_path in bug_info['test_file_paths']:
        print("=============== Running test", test_file_path, "===============")
        test_script_cmd = ''
        if(bug_info['test_script'][param_dict['version']]):
            test_script_cmd = 'php composer.phar run-script --timeout 0 ' + bug_info['test_script'][param_dict['version']] + ' ' + test_file_path
        else:
            test_script_cmd = 'vendor/bin/phpunit ' + os.path.join(param_dict['output'], bug_info['repo_name'], test_file_path)

        try:
            print(test_script_cmd)
            sp.call(test_script_cmd, shell=True)
        except Exception as e:
            print(e)


def run_test_file(param_dict):
    SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    bug_info = myProject.get_bug_info(param_dict)

    if(not os.path.isdir(os.path.join(param_dict['output'], bug_info['repo_name']))):
        print("can't find the project folder")
        exit()

    os.chdir(os.path.join(param_dict['output'], bug_info['repo_name']))

    test_script_cmd = ''
    if(bug_info['test_script'][param_dict['version']]):
        test_script_cmd = 'php composer.phar run-script --timeout 0 ' + bug_info['test_script'][param_dict['version']] + ' ' + param_dict['file']
    else:
        test_script_cmd = 'vendor/bin/phpunit ' + os.path.join(param_dict['output'], bug_info['repo_name'], param_dict['file'])

    try:
        print(test_script_cmd)
        sp.call(test_script_cmd, shell=True)
    except Exception as e:
        print(e)
