import os
import sys
import logging
import json
import cfnresponse
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    print(f' start service DB setup event=""{event}""')
    # rds env settings
    db_host = os.environ['DBHost']
    db_port = os.environ['DBPort']
    db_username = os.environ['DBUsername']
    db_password = os.environ['DBPassword']

    # rds new db name
    service_db_name = event.ResourceProperties.ServiceDBName

    conn = psycopg2.connect(host=db_host, port=db_port, dbname='postgres', user=db_username, password=db_password)
    conn.set_session(autocommit=True)

    try:
      cursor = conn.cursor()

      cursor.execute(f'SELECT datname FROM pg_database WHERE datname = ""{service_db_name}""')
      found = cursor.fetchone()

      if found is not None:
        print('Database already exists')

      else:
        cursor.execute(f'CREATE DATABASE ""{service_db_name}""')
        print('Completed')

    finally:
      cursor.close()
      conn.close()

    responseData = {}
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, event.LogicalResourceId)

    return {
        'statusCode': 200,
        'body': json.dumps(f'DB setup db_name=""{service_db_name}"" has finished successfully ')
    }