from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .db import Db
from configparser import ConfigParser
from urllib.parse import quote
import json
from .common import validate_token, validate_table_access

# Read config.ini file
config = ConfigParser()
config.read('resources/config.ini')

blp = Blueprint("stores", __name__, description="retrieve the data")


@blp.route("/store/<string:table_name>/<string:token>")
class CollectTableData(MethodView):
    def get(self, table_name, token):
        if validate_token(token):
            if validate_table_access(token,table_name):
                global my_db
                try:
                    my_db = Db(f"mysql+mysqlconnector://{config['DATABASE']['DB_USER']}:%s@{config['DATABASE']['DB_HOST']}/"
                               f"{config['DATABASE']['DB_NAME']}" % quote(config['DATABASE']['DB_PASSWORD']))
                except KeyError:
                    abort(404, message="Please check database configuration file ")
                db_engine = my_db.create_db_connection()
                if db_engine:
                    data = my_db.get_table_data(db_engine, table_name)
                    if isinstance(data, list):
                        final_data = json.dumps(data, indent=4, sort_keys=True, default=str)
                        return final_data
                    else:
                        abort(404, message=data)
                else:
                    abort(404, message="Failed to connect to the database")
            else:
                abort(400, message="User have no access to read this table")
        else:
            abort(400, message="Invalid token")


@blp.route("/store/<string:table_name>/<string:column_array>/<string:token>")
class CollectColumnDataFromTable(MethodView):
    def get(self, table_name, column_array, token):
        if validate_token(token):
            if validate_table_access(token, table_name):
                global my_db
                try:
                    my_db = Db(f"mysql+mysqlconnector://{config['DATABASE']['DB_USER']}:%s@{config['DATABASE']['DB_HOST']}/"
                               f"{config['DATABASE']['DB_NAME']}" % quote(config['DATABASE']['DB_PASSWORD']))
                except KeyError:
                    abort(400, message="Please check database configuration file ")
                db_engine = my_db.create_db_connection()
                if db_engine:
                    if "," in column_array:
                        column_list = column_array.split(',')
                    else:
                        column_list = [column_array]
                    column_list_exists_status = my_db.check_column_exists(db_engine, table_name, column_list)
                    if column_list_exists_status==True:
                        data = my_db.get_column_data_from_table(db_engine, table_name, column_list)
                        if isinstance(data, list):
                            final_data = json.dumps(data, indent=4, sort_keys=True, default=str)
                            return final_data
                        else:
                            abort(400, message=data)
                    else:
                        abort(400, message=column_list_exists_status)
                else:
                    abort(400, message="Failed to connect to the database")
            else:
                abort(400, message="User have no access to read this table")
        else:
            abort(400, message="Invalid token")
