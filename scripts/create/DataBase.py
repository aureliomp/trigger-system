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
      host= mysqlConector['host'] ,
      user= mysqlConector['user'],
      port =   mysqlConector['port'],
      password= mysqlConector['password']
    )
    cursor = cnx.cursor()

    cursor.execute(query)

    cursor.close()
    cnx.close()
    return 'success'
 
