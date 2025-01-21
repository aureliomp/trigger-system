import mysql.connector
import config

async def create(nameNewDatabase):
    chain_database = str(nameNewDatabase)
    mysqlConector = config.load_info()
    query = f'''
      DROP DATABASE IF EXISTS {chain_database};
      CREATE DATABASE {chain_database};
    '''

    cnx  = mysql.connector.connect(
      host= mysqlConector['mysql']['host'] ,
      user= mysqlConector['mysql']['user'],
      port =   mysqlConector['mysql']['port'],
      password= mysqlConector['mysql']['password']
    )
    cursor = cnx.cursor()

    cursor.execute(query,multi=True)
    cursor.close()
    cnx.close()
    return 'success'
 
