import mysql.connector
import json
import config

async  def insertion(databaseName):
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['host'] ,
        user= mysqlConector['user'],
        port =   mysqlConector['port'],
        password= mysqlConector['password'],
        database= databaseName
    )   
    cursor = cnx.cursor()
    with open('./dataBook/customer.json') as f:
        jsonData = json.load(f)
        for  customer in jsonData['customers']:
            query_customer = '''
                INSERT INTO  customer (
                name,             
                lastname,         
                lastname_2,      
                email,            
                password,         
                password_firebase,
                isActive,        
                is_reset_password,
                fan_id,            
                is_confirm,      
                provider 
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            '''
            val = (customer['name'], customer['lastname'], customer['lastname2'], customer['email'], customer['password'], customer['passwordFirebase'],customer['isActive'],  customer['fanId'], customer['isConfirm'], customer['isResetPassword'], customer['provider'] )
            cursor.execute(query_customer,val)     
    cnx.commit()
    cursor.close()
    cnx.close()
    return True