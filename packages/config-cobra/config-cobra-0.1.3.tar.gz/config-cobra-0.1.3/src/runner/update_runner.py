from sqlalchemy.exc import IntegrityError
import yaml
import logging
from src.db.database_instance import DatabaseInstance
from sqlalchemy import text

logger = logging.getLogger("pipeline_data_deploy_logger")

def validate_local_fields(func):
    """
    Decorator to check data is as described in yaml file
    """
    def decorator(self, *args, **kwargs):
        
        if not all(key in self.columns for key in kwargs['data'].keys()):
            logger.error(f"Data does not match yaml file, expected fields: {self.columns}")
            return None
        
        if not all(key in kwargs['data'].keys() for key in self.columns):
            logger.error(f"Data does not match yaml file, expected fields: {self.columns}")
            return None

        return func(self, *args, **kwargs)
    
    return decorator
    
class UpdateRunner():

    def __init__(self, db: DatabaseInstance):
        self.db = db
        self.yaml_data = None
        self.was_table_updated = False
        self.columns = None

    def process_yaml(self, yaml_file):

        self.yaml_data = self._load_yaml(yaml_file)

        for deploy in self.yaml_data["deploy"]:

            self.columns = deploy["columns"]

            if self._check_table_exists(deploy["table"]):
                logger.info("Table exists, updating table")

                if deploy["action"] == "insert":
                    for data in deploy["data"]:
                        self._is_insert(data=data, table=deploy["table"])
                elif deploy["action"] == "update":
                    for data in deploy["data"]:
                        self._is_update(data=data, table=deploy["table"], pk_column=deploy["pk"])
                elif deploy["action"] == "update_or_insert":
                    for data in deploy["data"]:
                        self._is_update_or_insert(data=data, table=deploy["table"], pk_column=deploy["pk"])
                elif deploy["action"] == "delete":
                    for data in deploy["data"]:
                        self._is_delete(data=data, table=deploy["table"], pk_column=deploy["pk"])

                self.was_table_updated = True
            else:
                logger.warn("Table does not exist, will not update table")

    @validate_local_fields
    def _is_insert(self, data:dict, table:str):

        with self.db.get_session() as session:
            try:
                query = text(f"INSERT INTO {table} ({','.join(data.keys())}) VALUES ({','.join(':' + key for key in data.keys())})")
                session.execute(query, params=data)
                session.commit()
            except IntegrityError as e:
                logger.error(f"Error inserting data: {e}")
                session.rollback()

    @validate_local_fields
    def _is_update(self, data:dict, table:str, pk_column:str="id"):
            
        with self.db.get_session() as session:
            try:
                logger.info(f"Updating data in table {table} where {pk_column} = {data[pk_column]}")
                query = text(f"UPDATE {table} SET {','.join(f'{key} = :{key}' for key in data.keys())} WHERE {pk_column} = :{pk_column}")
                session.execute(query, params=data)
                session.commit()
            except IntegrityError as e:
                logger.error(f"Error updating data: {e}")
                session.rollback()

    @validate_local_fields
    def _is_update_or_insert(self, data:dict, table:str, pk_column:str="id"):
            
            with self.db.get_session() as session:
                try:
                    logger.info(f"Updating or inserting data into table {table} where {pk_column} = {data[pk_column]}")
                    query = text(f"INSERT INTO {table} ({','.join(data.keys())}) VALUES ({','.join(':' + key for key in data.keys())}) ON CONFLICT ({pk_column}) DO UPDATE SET {','.join(f'{key} = :{key}' for key in data.keys())}")
                    session.execute(query, params=data)
                    session.commit()
                except IntegrityError as e:
                    logger.error(f"Error updating or inserting data: {e}")
                    session.rollback()

    @validate_local_fields
    def _is_delete(self, data:dict, table:str, pk_column:str="id"):
            
        with self.db.get_session() as session:
            try:
                logger.info(f"Deleting data from table {table} where {pk_column} = {data[pk_column]}")
                query = text(f"DELETE FROM {table} WHERE {pk_column} = :{pk_column}")
                session.execute(query, params=data)
                session.commit()
            except IntegrityError as e:
                logger.error(f"Error deleting data: {e}")
                session.rollback()

    def _check_table_exists(self, table_name:str):

        if table_name in self.db.get_tables():
            return True
        
        return False

    def _load_yaml(self, yaml_file):
        with open(yaml_file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return None