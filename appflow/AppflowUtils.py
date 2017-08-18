import base64
import hashlib
import operator
import os
import sys
from functools import reduce

import pymysql.cursors

from Crypto.Cipher import AES


def get_md5_sum(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        return hashlib.md5(data).hexdigest() + '\t' + file_name + '\n'


def write_md5_sum(file_name, md5_store_file):
    os.makedirs(os.path.dirname(md5_store_file), exist_ok=True)
    line = get_md5_sum(file_name)
    if (os.path.exists(md5_store_file)):
        open(md5_store_file, 'a').write(line)
    else:
        open(md5_store_file, 'w+').write(line)


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value


def rm_in_dict(branch, keys):
    if len(keys) > 1:
        empty = rm_in_dict(branch[keys[0]], keys[1:])
        if empty:
            del branch[keys[0]]
    else:
        del branch[keys[0]]
    return len(branch) == 0


def add_keys(d, key, value=None):
    if len(key) > 1:
        d[key[0]] = _d = {}
        d[key[0]] = d.get(key[0], {})
        add_keys(d[key[0]], key[1:], value)
    else:
        d[key[0]] = value


def check_string_in_file(file_name, string):
    found = False
    with open(file_name) as f:
        for line in f:
            if string in line:  # Key line: check if `w` is in the line.
                found = True
    return found


def diff_files(file1, file2):
    result = list()
    with open(file1) as f1:
        with open(file2) as f2:
            lines_file_1 = f1.readlines()
            lines_file_2 = f2.readlines()
            diff = [line for line in lines_file_1 if line not in lines_file_2]
            for line in diff:
                file_name = line.split('\t')[1].replace('\n', '')
                result.append(file_name)
            return result


def safe_remove(file_name):
    try:
        os.remove(file_name)
    except IOError:
        pass


def get_file_list(dir):
    file_list = list()
    for root, subdirs, files in os.walk(dir):
        for f in files:
            file_list.append(os.path.join(root, f))
    return file_list


RED = '\033[01;31m'
GREEN = '\033[01;32m'
YELLOW = '\033[01;33m'
BLUE = '\033[01;34m'
CYAN = '\033[01;36m'
WHITE = '\033[01;37m'
CLEAR = '\033[00m'


def get_provision_color_string(command, tenant, env):
    return '[' + CYAN + command + CLEAR + '][' + \
        WHITE + tenant + CLEAR + ']' + get_env_color_string(env)


def get_env_color_string(env):
    return {
        'development': '[' + GREEN + env + CLEAR + ']',
        'testing': '[' + BLUE + env + CLEAR + ']',
        'staging': '[' + YELLOW + env + CLEAR + ']',
        'production': '[' + RED + env + CLEAR + ']'
    }.get(env, 'development')


def get_tenant_dir(tenant):
    return os.getenv("HOME") + "/.appflow/tenant/" + tenant + "/"


def get_tenant_env_dir(tenant, env):
    return os.getenv("HOME") + "/.appflow/tenant/" + tenant + "/" + env


def get_vault_file(tenant, env):
    return os.getenv("HOME") + "/.appflow/vault/" + tenant + "/" + env


def get_md5_folder(tenant):
    return os.getenv("HOME") + "/.appflow/tmp/.appflow-" + os.getenv("USER") + "/" + tenant


def query_yes_no(question, default="yes"):
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


def aes_encrypt(string, password):
    block_size = 32
    padded_string = string + (block_size - len(string) %
                              block_size) * chr(block_size - len(string) % block_size)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(padded_string))


def aes_decrypt(enc, password):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    result = cipher.decrypt(enc[AES.block_size:])
    result = result[:-ord(result[len(result) - 1:])]
    return result.decode('utf-8')


def get_salt():
    result = base64.b64encode(os.urandom(32)).decode()
    while sql_check_if_present('salt', result):
        result = base64.b64encode(os.urandom(32)).decode()
    return result


def get_api_token():
    result = base64.urlsafe_b64encode(os.urandom(50)).decode()
    while sql_check_if_present('api_key', result):
        result = base64.urlsafe_b64encode(os.urandom(50)).decode()
    return result


def hash_string(plaintext):
    hashx = hashlib.sha512()
    hashx.update((plaintext).encode())
    return hashx.hexdigest()


# CREATE TABLE users(user VARCHAR(100), email VARCHAR(100), password VARCHAR(100), salt VARCHAR(100), tenant VARCHAR(100), api_key VARCHAR(100), api_quota INT);


def sql_check_if_present(field, search):
    return sql_query(field, search) != None


def sql_query(field, search):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    result = ''
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT `user`, `email`, `password` , `salt`, `tenant`, `api_key`, `api_quota`
            FROM `users` 
            WHERE `""" + field + "`=%s"
            cursor.execute(sql, (search,))
            result = cursor.fetchone()

    except Exception as exception:
        print(exception)
    finally:
        connection.close()
    return result


def sql_write(data):
    if sql_check_if_present('user', data[0]):
        # Entry exists, update only
        sql_update(data)
    else:
        # Entry does not exist; create it
        sql_insert(data)


def sql_insert(data):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO `users` (`user`, `email`, `password` , `salt`, `tenant`, `api_key`, `api_quota`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, data)
        connection.commit()
        success = True
    except Exception as exception:
        success = False
        print(exception)
    finally:
        connection.close()
    return success


def sql_update(data):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE `users`
                SET `user`=%s, `email`=%s, `password`=%s , `salt`=%s, `tenant`=%s, `api_key`=%s, `api_quota`=%s
                WHERE user=%s
                """
            cursor.execute(sql, (*data, data[0]))

        connection.commit()
        success = True
    except Exception as exception:
        success = False
        print(exception)
    finally:
        connection.close()
    return success

def sql_remove(field, search):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = """
            DELETE FROM `users`
            WHERE """ + field + "=%s"
            cursor.execute(sql, search)
        connection.commit()
        success = True
    except Exception as exception:
        success = False
        print(exception)
    finally:
        connection.close()
    return success
