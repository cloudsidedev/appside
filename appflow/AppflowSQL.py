import base64
import hashlib
import os
import stat

import pymysql.cursors
from Crypto.Cipher import AES


def get_aes_password():
    file_name = "/etc/default/.appflow-key"
    if os.path.exists(file_name):
        with open(file_name, 'r') as pass_file:
            return pass_file.read().replace('\n', '')
    else:
        password = base64.b64encode(os.urandom(32)).decode()
        with open(file_name, "w") as pass_file:
            pass_file.write(password)
            os.chmod(file_name, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            return password


def aes_encrypt(string, password):
    block_size = 32
    padded_string = string + (block_size - len(string) %
                              block_size) * chr(block_size - len(string)
                                                % block_size)
    _iv = os.urandom(AES.block_size)
    cipher = AES.new(password, AES.MODE_CBC, _iv)
    return base64.b64encode(_iv + cipher.encrypt(padded_string))


def aes_decrypt(enc, password):
    enc = base64.b64decode(enc)
    _iv = enc[:AES.block_size]
    cipher = AES.new(password, AES.MODE_CBC, _iv)
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


def sql_check_if_present(field, search):
    return sql_query(field, search) is not None


def sql_write(data):
    if sql_check_if_present('username', data[0]):   # Entry exists, update only
        return sql_update(data)
    else:                                     # Entry does not exist; create it
        return sql_insert(data)


def sql_query(field, search):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT `username`, `mail`, `password` , `salt`, `tenant`, `api_key`, `api_quota`, `user_enc`, `mail_enc` , `api_key_enc`
            FROM `users`
            WHERE `""" + field + "`=%s"
            cursor.execute(sql, (search,))
            result = cursor.fetchone()
    except Exception as exception:
        result = None
        print(exception)
    finally:
        connection.close()
    return result


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
            INSERT INTO `users` (`username`, `mail`, `password` , `salt`, `tenant`, `api_key`, `api_quota`, `user_enc`, `mail_enc`, `api_key_enc`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                SET `username`=%s, `mail`=%s, `password`=%s , `salt`=%s, `tenant`=%s, `api_key`=%s, `api_quota`=%s , `user_enc`=%s, `mail_enc`=%s, `api_key_enc`=%s
                WHERE username=%s
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


def sql_util_register(username, mail, password, tenant):
    user_enc = aes_encrypt(username, get_aes_password())
    username = hash_string(username)
    mail_enc = aes_encrypt(mail, get_aes_password())
    mail = hash_string(mail)
    salt = get_salt()
    api_key = get_api_token()
    api_key_enc = api_key
    api_key = hash_string(api_key)
    password = hash_string(password + salt)
    crypted_password = aes_encrypt(password, get_aes_password())
    tenant = hash_string(tenant)
    return sql_write((username, mail, crypted_password,
                      salt, tenant, api_key, 0, user_enc, mail_enc, api_key_enc))


def sql_util_auth_username(username, password, tenant):
    username = hash_string(username)
    tenant = hash_string(tenant)
    if sql_check_if_present("username", username):
        sql_pass = sql_query("username", username)["password"]
        sql_pass = aes_decrypt(sql_pass, get_aes_password())
        salt = sql_query("username", username)["salt"]
        password = hash_string(password + salt)
        if sql_pass == password:
            sql_tenant = sql_query("username", username)["tenant"]
            if sql_tenant == tenant:
                print("Authenticated")
                return True
            else:
                print("Auth failed tenant")
                return False
        else:
            print("Auth failed pass")
            return False


def sql_util_auth_mail(mail, password, tenant):
    mail = hash_string(mail)
    tenant = hash_string(tenant)
    if sql_check_if_present("mail", mail):
        sql_pass = sql_query("mail", mail)["password"]
        sql_pass = aes_decrypt(sql_pass, get_aes_password())
        salt = sql_query("mail", mail)["salt"]
        password = hash_string(password + salt)
        if sql_pass == password:
            sql_tenant = sql_query("mail", mail)["tenant"]
            if sql_tenant == tenant:
                print("Authenticated")
                return True
            else:
                print("Auth failed tenant")
                return False
        else:
            print("Auth failed pass")
            return False


def sql_util_auth_api(api_key):
    api_key = hash_string(api_key)
    if sql_check_if_present('api_key', api_key):
        print("Auth passed")
        return True
    else:
        print("Auth failed pass")
        return False


def sql_util_recover_username(mail, password, tenant):
    if sql_util_auth_mail(mail, password, tenant):
        mail = hash_string(mail)
        sql_user_enc = sql_query('mail', mail)["user_enc"]
        sql_user_enc = aes_decrypt(
            sql_user_enc, get_aes_password())
        return sql_user_enc


def sql_util_recover_mail(username, password, tenant):
    if sql_util_auth_username(username, password, tenant):
        username = hash_string(username)
        sql_mail_enc = sql_query('mail', username)["mail_enc"]
        sql_mail_enc = aes_decrypt(
            sql_mail_enc, get_aes_password())
        return sql_mail_enc


def sql_util_recover_api_key(username, password, tenant):
    if sql_util_auth_username(username, password, tenant):
        username = hash_string(username)
        sql_api_key_enc = sql_query('username', username)[
            "api_key_enc"]
        sql_api_key_enc = aes_decrypt(sql_api_key_enc, get_aes_password())
        return sql_api_key_enc


def sql_util_change_pass(username, old_password, tenant, new_password):
    if sql_util_auth_username(username, old_password, tenant):
        sql_data = sql_query('username', hash_string(username))
        salt = sql_data["salt"]
        password = hash_string(new_password + salt)
        crypted_password = aes_encrypt(password, get_aes_password())
        sql_data['password'] = crypted_password
        return sql_update((sql_data["username"],
                           sql_data["mail"],
                           sql_data["password"],
                           sql_data["salt"],
                           sql_data["tenant"],
                           sql_data["api_key"],
                           sql_data["api_quota"],
                           sql_data["user_enc"],
                           sql_data["mail_enc"],
                           sql_data["api_key_enc"]))


def sql_util_change_mail(username, password, tenant, new_mail):
    if sql_util_auth_username(username, password, tenant):
        sql_data = sql_query('username', hash_string(username))
        mail_enc = aes_encrypt(new_mail, get_aes_password())
        mail = hash_string(new_mail)
        sql_data["mail"] = mail
        sql_data["mail_enc"] = mail_enc
        return sql_update((sql_data["username"],
                           sql_data["mail"],
                           sql_data["password"],
                           sql_data["salt"],
                           sql_data["tenant"],
                           sql_data["api_key"],
                           sql_data["api_quota"],
                           sql_data["user_enc"],
                           sql_data["mail_enc"],
                           sql_data["api_key_enc"]))


def sql_util_update_api_quota(username, password, tenant, quota):
    if sql_util_auth_username(username, password, tenant):
        sql_data = sql_query('username', hash_string(username))
        sql_data["api_quota"] = quota
        return sql_update((sql_data["username"],
                           sql_data["mail"],
                           sql_data["password"],
                           sql_data["salt"],
                           sql_data["tenant"],
                           sql_data["api_key"],
                           sql_data["api_quota"],
                           sql_data["user_enc"],
                           sql_data["mail_enc"],
                           sql_data["api_key_enc"]))
