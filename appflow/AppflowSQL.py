import base64
import hashlib
import os
import pymysql.cursors

from Crypto.Cipher import AES

AES_PASSWORD = "C+sh5HgO2AzWCDWnGiqj0P3nJqRvqNvt"


def sqlWrite(username, mail, password, tenant):
    username_recover = aes_encrypt(username, AES_PASSWORD)
    username = hash_string(username)
    mail = hash_string(mail)
    salt = get_salt()
    api_key = get_api_token()
    api_key_recover = api_key
    api_key = hash_string(api_key)
    password = hash_string(password + salt)
    crypted_password = aes_encrypt(password, AES_PASSWORD)
    tenant = hash_string(tenant)
    sql_write((username, mail, crypted_password,
               salt, tenant, api_key, 0, username_recover, api_key_recover))
    return (api_key_recover)


def sqlUpdate(username, field, search):
    sql_data = sql_query('username', hash_string(username))
    accepted_strings = {"username", "mail", "tenant"}
    if (field in accepted_strings):
        search = hash_string(search)
        sql_data[field] = search
    elif (field == 'password'):
        salt = sql_data["salt"]
        password = hash_string(search + salt)
        crypted_password = aes_encrypt(password, AES_PASSWORD)
        sql_data['password'] = crypted_password
    elif (field == 'api_quota'):
        sql_data['api_quota'] = search
    sql_update((sql_data["username"],
                sql_data["mail"],
                sql_data["password"],
                sql_data["salt"],
                sql_data["tenant"],
                sql_data["api_key"],
                sql_data["api_quota"],
                sql_data["user_recover"],
                sql_data["api_key_recover"]))


def sqlAuth(query, search, password, tenant):
    search = hash_string(search)
    tenant = hash_string(tenant)
    if (sql_check_if_present(query, search)):
        sql_pass = sql_query(query, search)["password"]
        sql_pass = aes_decrypt(sql_pass, AES_PASSWORD)
        salt = sql_query(query, search)["salt"]
        password = hash_string(password + salt)
        if(sql_pass == password):
            sql_tenant = sql_query(query, search)["tenant"]
            if(sql_tenant == tenant):
                print("Authenticated")
                return True
            else:
                print("Auth failed tenant")
                return False
        else:
            print("Auth failed pass")
            return False


def sqlRecoverUsername(mail, password, tenant):
    if sqlAuth('mail', mail, password, tenant):
        mail = hash_string(mail)
        sql_user_recover = sql_query('mail', mail)["user_recover"]
        sql_user_recover = aes_decrypt(
            sql_user_recover, AES_PASSWORD)
        print(sql_user_recover)


def sqlRecoverApiKey(username, password, tenant):
    if sqlAuth('username', username, password, tenant):
        username = hash_string(username)
        sql_api_key_recover = sql_query('username', username)[
            "api_key_recover"]
        print(sql_api_key_recover)


def sqlChangePass(username, old_password, new_password, tenant):
    if sqlAuth('username', username, old_password, tenant):
        sqlUpdate(username, 'password', new_password)


def sqlRead(field, search):
    search = hash_string(search)
    print(sql_query(field, search))


def sqlRemove(field, search):
    search = hash_string(search)
    sql_remove(field, search)


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

# use db;
# select * from users \G;
# CREATE TABLE users(username TEXT, mail TEXT, password TEXT, salt TEXT, tenant TEXT, api_key TEXT, api_quota INT, user_recover TEXT, api_key_recover TEXT);


def sql_check_if_present(field, search):
    return sql_query(field, search) != None


def sql_write(data):
    if sql_check_if_present('username', data[0]):   # Entry exists, update only
        sql_update(data)
    else:                                           # Entry does not exist; create it
        sql_insert(data)


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
            SELECT `username`, `mail`, `password` , `salt`, `tenant`, `api_key`, `api_quota`, `user_recover`, `api_key_recover`
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
            INSERT INTO `users` (`username`, `mail`, `password` , `salt`, `tenant`, `api_key`, `api_quota`, `user_recover`, `api_key_recover`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                SET `username`=%s, `mail`=%s, `password`=%s , `salt`=%s, `tenant`=%s, `api_key`=%s, `api_quota`=%s , `user_recover`=%s, `api_key_recover`=%s
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
