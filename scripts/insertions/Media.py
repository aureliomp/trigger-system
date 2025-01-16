import mysql.connector
import config
import json


async def  insert(nameDataBase):
      
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
    host= mysqlConector['host'] ,
    user= mysqlConector['user'],
    port =   mysqlConector['port'],
    password= mysqlConector['password'],
    database= nameDataBase
    ) 
    cursor = cnx.cursor()
    query = ''
    with open('./dataBook/media.json') as f:
        jsonData = json.load(f)
        for enclosure in  jsonData['enclosures']:
            query= '''
                INSERT INTO media (name, url, id_enclosure)
                VALUES (%s,%s,%s);
            '''
            val = (enclosure['name'], enclosure['url'],enclosure['idEnclosure'])
            cursor.execute(query,val)
    cnx.commit()
    cursor.close()
    cnx.close()  
    return True
# end def