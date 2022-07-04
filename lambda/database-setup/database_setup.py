import json
import sys
import logging
import json
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    # rds settings
    db_host  = event.host
    db_username = event.db_username
    db_password = event.db_password
    new_db_name = event.new_db_name

    conn = psycopg2.connect(host=db_host, port=5432, dbname='postgres', user=db_username, password=secret['password'])
    conn.set_session(autocommit=True)

    try:
      cursor = conn.cursor()

      cursor.execute(f'SELECT datname FROM pg_database WHERE datname = ""{new_db_name}""')
      found = cursor.fetchone()

      if found is not None:
        print('Database already exists')

      else:
        # cursor.execute(""SET ROLE ca_common"")

        # print(f'Creating {role} role')
        # cursor.execute(f'CREATE ROLE ""{role}"" WITH INHERIT; GRANT ""{role}"" TO ca_common;')

        # print(f'Creating {database} database')
        # cursor.execute(f'CREATE DATABASE ""{database}"" WITH OWNER = ""{role}""')

        cursor.execute(f'CREATE DATABASE ""{database}""')

        print('Completed')

    finally:
      cursor.close()
      conn.close()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(f'DB setup db_name=""{new_db_name}"" has finished successfully ')
    }