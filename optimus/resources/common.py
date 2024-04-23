import json
import requests


def get_db_object_to_list(db_object):
    db_data = []
    if db_object:
        for rows in db_object:
            db_data.append(rows)
        return db_data
    else:
        return False


def get_db_object_to_list_for_db(db_object):
    db_data = []
    if db_object:
        for rows in db_object:
            db_data.append(rows[0])
        return db_data
    else:
        return False


def get_db_object_to_dict(db_object):
    db_data = {}
    count = 1
    if db_object:
        for rows in db_object:
            db_data[str(count)] = tuple(rows)
            count += 1
        return db_data
    else:
        return False


def validate_token(token):
    if token:
        token_validation_url = "http://9.30.221.213:8000/api/auth/validate_token/"
        token_plus_url = token_validation_url + token
        response = requests.post(token_plus_url)
        if response.status_code == 200:
            return True
        else:
            return False
    else:
        return False


def validate_table_access(token, table_name):
    if token:
        table_access_validation_url = "http://9.30.221.213:8000/api/auth/validate_table_access/"
        final_validation_url = table_access_validation_url+token+"/"+table_name
        response = requests.post(final_validation_url)
        if response.status_code == 200:
            return True
        else:
            return False
    else:
        return False

