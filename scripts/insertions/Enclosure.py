import mysql.connector
import config
import json

async def insertions (nameDataBase):   
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['host'] ,
        user= mysqlConector['user'],
        port =   mysqlConector['port'],
        password= mysqlConector['password'],
        database= nameDataBase
    ) 
    cursor = cnx.cursor()
    with open('./dataBook/enclosure.json') as f:
        jsonData = json.load(f)
        for enclosure in  jsonData['enclosures']:
            query_enclosure = f'''
                INSERT INTO settings_enclosure  (name,enclosure_address,isActive) VALUES ('{enclosure['name']}','{enclosure['enclosureAddress']}',1) ;         
            '''
            cursor.execute(query_enclosure)

        for section in jsonData['sections']:
            query_section = '''
                INSERT INTO enclosure_section (name,description,class_name, id_enclosure ) VALUES (%s,%s,%s,%s);
            '''
            val = (section['name'],section['description'],section['className'],section['idEnclosure'])
            cursor.execute(query_section,val)

        
        for chunk in jsonData['chunks']:
            query_chunk = '''
                INSERT INTO enclosure_chunk (name, id_section, row_total, column_total, id_svg)VALUES(%s,%s,%s,%s,%s);
            ''' 
            values = (chunk['name'],chunk['idSection'],chunk['rowTotal'],chunk['TotalColum'],chunk['idSvg'])
            cursor.execute(query_chunk,values)
        
        for row in jsonData['rows']:
            query_row = '''
                INSERT INTO enclosure_row (id_chunk, row_name, num_seat, `show`, id_svg_chunk) VALUES (%s, %s, %s, %s, %s);
            '''
            values = (row['chunk'] ,row['rowName'] ,row['seatNum'] ,row['show'] ,row['idSvg'])
            cursor.execute(query_row,values)

    cnx.commit()
    cursor.close()
    cnx.close()   
    return True
