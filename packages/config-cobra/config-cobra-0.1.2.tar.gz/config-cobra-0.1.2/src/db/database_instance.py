import logging
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger("pipeline_data_deploy_logger")

class DatabaseInstance():

    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        logger.info("Creating a database instance")
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self._get_engine()

    def _get_engine(self):

        self.engine = create_engine(self.construct_uri())
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine) 

    def construct_uri(self):

        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def get_tables(self):
        insp = inspect(self.engine)
        return insp.get_table_names()
    
    def get_session(self) -> Session:
        return SessionManager(self.Session())
    
class SessionManager:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()