import json
import sys
import logging
import json
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    print(f' start service DB setup event=""{event}""')
    # rds settings
    db_host  = event.DBHost
    db_username = event.DBUsername
    db_password = event.DBPassword
    service_db_name = event.ServiceDBName

    conn = psycopg2.connect(host=db_host, port=5432, dbname='postgres', user=db_username, password=db_password)
    conn.set_session(autocommit=True)

    try:
      cursor = conn.cursor()

      cursor.execute(f'SELECT datname FROM pg_database WHERE datname = ""{service_db_name}""')
      found = cursor.fetchone()

      if found is not None:
        print('Database already exists')

      else:
        cursor.execute(f'CREATE DATABASE ""{database}""')
        print('Completed')

    finally:
      cursor.close()
      conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(f'DB setup db_name=""{service_db_name}"" has finished successfully ')
    }