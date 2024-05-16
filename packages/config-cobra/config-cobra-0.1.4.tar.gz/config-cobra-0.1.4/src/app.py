import argparse
import logging
from src.db import DatabaseInstance
from src.settings import settings
from src.runner import UpdateRunner

logger = logging.getLogger("pipeline_data_deploy_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def main():

    logger.info("Starting the update process")

    parser = argparse.ArgumentParser(description="Update the database with from yaml file")
    parser.add_argument('--yaml_file', '-y', type=str, help="The yaml file to update the database with", required=True)

    args = parser.parse_args()

    db = DatabaseInstance(
        db_user=settings.DB_USER,
        db_password=settings.DB_PASSWORD,
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
        db_name=settings.DB_NAME
    )

    update_runner = UpdateRunner(db)

    if "yaml_file" in args:
        update_runner.process_yaml(args.yaml_file)


    print(db.get_tables())

if __name__ == '__main__':
    main()