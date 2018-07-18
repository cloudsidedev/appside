"""
Appflow Utilities.
This contains all the generic functions
needed to support the rest of the library.
"""
import hashlib
import os
import sys
import asyncio
from asyncio.subprocess import PIPE


def get_md5_sum(file_name):
    """
    Return the md5 checksum of the specified file.

    :type  file_name: string
    :param file_name: The name of the file to hash.

    :rtype:   string
    :return:  the function returns the md5 hash of the file.
    """
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        return hashlib.md5(data).hexdigest() + '\t' + file_name + '\n'


def write_md5_sum(file_name, md5_store_file):
    """
    Write the modified md5 filename to the md5_store_file

    :type  file_name: string
    :param file_name: The name of the file to hash.

    :type  md5_store_file: string
    :param md5_store_file: The name of the file where to write the hash.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    os.makedirs(os.path.dirname(md5_store_file), exist_ok=True)
    line = get_md5_sum(file_name)
    if os.path.exists(md5_store_file):
        open(md5_store_file, 'a').write(line)
    else:
        open(md5_store_file, 'w+').write(line)


def check_string_in_file(file_name, searched_string):
    """
    Check if string is in file

    :type  file_name: string
    :param file_name: The file name where to search the string.

    :type  searched_string: string
    :param searched_string: The string to search.

    :rtype:   bool
    :return:  the function returns if the string is found or not.
    """
    found = False
    with open(file_name) as file:
        for line in file:
            if searched_string in line:
                found = True
    return found


def diff_files(file1, file2):
    """
    Returns different lines between file1 and file2.
    Returned data is a list of strings.

    :type  file1: string
    :param file1: The name of the first file.

    :type  file2: string
    :param file2: The name of the second file.

    :rtype:   list
    :return:  the function returns a list containing the different lines between
                the 2 files.
    """
    result = list()
    if os.path.exists(file1):
        with open(file1) as file_1:
            if os.path.exists(file2):
                with open(file2) as file_2:
                    lines_file_1 = file_1.readlines()
                    lines_file_2 = file_2.readlines()
                    diff = [line.split('\t')[1].replace('\n', '')
                            for line in lines_file_1
                            if line not in lines_file_2]
                    return diff
            else:
                return result
    else:
        return result


def safe_remove(file_name):
    """
    Gracefully delete a file.

    :type  file_name: string
    :param file_name: The name of the file to delete.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    try:
        os.remove(file_name)
    except IOError:
        pass


def get_file_list(_dir):
    """
    Returns a list of files in a directory.

    :type  _dir: string
    :param _dir: The name of the directory to explore.

    :rtype:   list
    :return:  the function returns the list of files in the folder.
    """
    file_list = list()
    for root, subdirs, files in os.walk(_dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


RED = '\033[01;31m'
GREEN = '\033[01;32m'
YELLOW = '\033[01;33m'
BLUE = '\033[01;34m'
CYAN = '\033[01;36m'
WHITE = '\033[01;37m'
CLEAR = '\033[00m'

TASK_SUCCESS = 'Task Completed Successfully!'
TASK_FAIL = 'Task Failed!'
TASK_RUNNING = 'Task is Running...'
TASK_START = 'Task is Starting...'
OK = 200
ACCEPTED = 202
NO_CONTENT = 204
INVALID_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
INTERNAL_ERROR = 500


def get_status_code(response):
    """
    Return the correct response code
    based on the content of the text error.
    """
    if 'Error' in response:
        if 'Invalid' in response:
            return INVALID_REQUEST
        elif 'Bad Syntax' in response:
            return METHOD_NOT_ALLOWED
        elif 'Not Found' in response:
            return NOT_FOUND
        else:
            return INTERNAL_ERROR
    else:
        return OK


def get_provision_color_string(command, tenant, env):
    """
    Color code for the provision string

    :type  command: string
    :param command: The command to execute.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   string
    :return:  the function returns the color coded string to print
                before the execution of the ansible command.
    """
    return '[' + CYAN + command + CLEAR + '][' + \
        WHITE + tenant + CLEAR + ']' + get_env_color_string(env)


def get_env_color_string(env):
    """
    Color code for the environment variable
    Needed in provision string.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   string
    :return:  the function returns the color needed for the corresponding env.
    """
    return {
        'development': '[' + GREEN + env + CLEAR + ']',
        'testing': '[' + BLUE + env + CLEAR + ']',
        'staging': '[' + YELLOW + env + CLEAR + ']',
        'production': '[' + RED + env + CLEAR + ']'
    }.get(env, 'development')


def get_appflow_folder():
    """
    Get directory or appflow.

    :type  _file: string
    :param _file: The name of the script file executed internally.

    :rtype:   string
    :return:  the function returns the root of appflow. Needed to then search
                for playbooks.
    """
    return os.getenv("HOME") + "/.appflow"


def get_tenant_dir(tenant):
    """
    Get directory for the specified tenant.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :rtype:   string
    :return:  the function returns the tenant folder.
    """
    return os.getenv("HOME") + "/.appflow/tenant/appflow-" + tenant + "/"


def get_tenant_env_dir(tenant, env):
    """
    Get directory for the specified tenant/environment.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the environment.

    :rtype:   string
    :return:  the function returns the tenant/environment folder.
    """
    return os.getenv("HOME") + "/.appflow/tenant/appflow-" + tenant + "/" + env


def get_vault_file(tenant, env):
    """
    Get vault file for the specified tenant/environment.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the environment.

    :rtype:   string
    :return:  the function returns the vault file searched.
    """
    return os.getenv("HOME") + "/.appflow/vault/" + tenant + "/" + env


def get_md5_folder(tenant):
    """
    Get directory for the specified tenant md5 files.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :rtype:   string
    :return:  the function returns the md5_folder searched.
    """
    return (os.getenv("HOME") + "/.appflow/tmp/.appflow-" +
            os.getenv("USER") + "/" + tenant)


def format_string_argument(argument):
    """
    Fire takes multiple arguments (comma separated) as list or tuple.
    Check argument type and put it to string.

    :type  argument: tuple or list
    :param argument: The argument passed.

    :rtype:   string
    :return:  Separated comma strings convertion for lists and tuples.
    """
    if argument is None:
        return None
    elif isinstance(argument, (list, tuple)):
        return ','.join(argument)
    return argument


@asyncio.coroutine
def read_stream_and_display(stream, task):
    """
    Read from stream line by line until EOF, display, and capture the lines.
    """
    output = []
    while True:
        line = yield from stream.readline()
        if not line:
            break
        output.append(line)
        # display(line)  # assume it doesn't block
        task.update_state(state='PROGRESS',
                          meta={'status': TASK_RUNNING,
                                'output': b'\n'.join(output)})
    return b''.join(output)


@asyncio.coroutine
def read_and_display(loop, *cmd, task):
    """Capture cmd's stdout, stderr while displaying them as they arrive
    (line by line).

    """
    # start process
    print(*cmd, type(cmd))
    process = yield from asyncio.create_subprocess_exec(
        *cmd, stdout=PIPE, stderr=PIPE, loop=loop)

    # read child's stdout/stderr concurrently (capture and display)
    try:
        stdout = yield from asyncio.gather(
            read_stream_and_display(process.stdout, task))
    except Exception:
        process.kill()
        raise
    finally:
        # wait for the process to exit
        rc = yield from process.wait()
    return rc, stdout


def yes_no(question, default="yes"):
    """
    Get a prompt for asking a question with y/N as accepted answer.

    :type  question: string
    :param question: The question to ask.

    :type  default: string
    :param default: The default answer. (default Yes)

    :rtype:   bool
    :return:  the function returns if the answer was yes or no.
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
