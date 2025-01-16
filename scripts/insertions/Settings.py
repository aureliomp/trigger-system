import mysql.connector
import config 
import json


async def fillMainTables(nameDataBase): 
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['host'] ,
        user= mysqlConector['user'],
        port =   mysqlConector['port'],
        password= mysqlConector['password'],
        database= nameDataBase
    )   
    cursor = cnx.cursor()
    with open('./dataBook/settings.json') as f:
        jsonData = json.load(f)
        for action in jsonData['actions']:
            query_action = '''
                INSERT INTO settings_actions (name, description) VALUES (%s, %s);
            '''
            val = ( action['name'],action['description'])
            cursor.execute(query_action,val)
        
        for module in jsonData['modules']:
            query_module = '''
                INSERT INTO settings_modules (name, description, isActive, createAt) VALUES
                (%s,%s, %s,%s);
            '''
            val = (module['name'],module['description'],module['isActive'],module['createAt'])
            cursor.execute(query_module,val)
        
        for rol in jsonData['roles']:
            query_rol = ' INSERT INTO settings_roles (name, description, isActive, createAt) VALUES (%s, %s, %s, %s);'
            val = (rol['name'],rol['descrition'],rol['isActive'],rol['createAt'])
            cursor.execute(query_rol,val)
        
        for feeGroup in jsonData['feesGroup']:
            query_fee_group = '''
                INSERT INTO settings_fees_group ( name, description)
                VALUES(%s,%s);
            '''
            val = ( feeGroup['name'],feeGroup['description'] )
            cursor.execute(query_fee_group,val)

        for billConcept in jsonData['billConcepts']:
            query_bill_concept = '''
                INSERT INTO settings_bill_concept (name, description, is_active)
                VALUES(%s, %s, %s);
            '''
            val = (billConcept['name'],billConcept['description'],billConcept['isActive'])
            cursor.execute(query_bill_concept,val)
        
        for gateway in jsonData['gateways']:
            query_gatewal = '''
                INSERT INTO settings_gateway (name, description, value_percent, value_cash, is_active, create_at, update_at)
                VALUES(%s, %s, %s, %s, %s, %s, %s);
            '''
            val = (gateway['name'], gateway['description'], gateway['valuePercent'], gateway['valueCash'],gateway['isActive'], gateway['createAt'], gateway['updateAt'])
            cursor.execute(query_gatewal,val)
        
        for stage in jsonData['stages']:
            query_stage = '''
                INSERT INTO settings_stage (name, description, value, create_at, is_active)
                VALUES(%s, %s, %s, %s, %s);
            '''
            val = (stage['name'], stage['descrition'], stage['value'], stage['createAt'],stage['isActive'])
            cursor.execute(query_stage,val)

        """
        for  permition in jsonData['permitions']:
            query_permition = '''  
                INSERT INTO settings_permitions (id_module, id_submodule, id_action, id_user)
                VALUES (%s, %s, %s, %s);
            '''
            val = (permition['idModule'], permition['idSubmodule'], permition['idAction'], permition['idUser'])
            print(query_permition,val)
            cursor.execute(query_permition,val)
        
        
        for permitionRole in jsonData['rolePermitions']:
            query_role_permition = '''
                INSERT INTO settings_role_permitions (id_rol, id_permition)
                VALUES(%s,%s);
            '''            
            val  =(permitionRole['idRol'], permitionRole['idPermition'])
            cursor.execute(query_role_permition,val)


        for fee in jsonData['fees']:
            query_fee = '''
                INSERT INTO settings_fees ( name, value, type_fees, title, subtitle, description, type_application, forced, is_active, id_group)
                VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s,%s);
            '''
            val = (fee['name'], fee['value'], fee['typeFees'], fee['title'], fee['subtitle'], fee['description'], fee['typeApplication'], fee['forced'], fee['isActive'], fee['idGroup'])
            cursor.execute(query_fee,val)

        for eventClassification in jsonData['eventClasifications']:
            query_event_clasification = '''
                INSERT INTO settings_event_classification  name, description, isActive)
                VALUES(%s,%s,%s);
            '''
            val = (eventClassification['name'], eventClassification['description'], eventClassification['isActive'])
            cursor.execute(query_event_clasification,val)
        

        for ticket in jsonData['tickets']:
            query_ticket = '''
                INSERT INTO settings_tickets (name, description, path, id_enclosure, available_seats, isActive, id_section)
                VALUES(%s, %s, %s, %s, %s, %s, %s);
            '''
            val = (ticket['name'], ticket['descrition'], ticket['path'], ticket['idEnclosure'], ticket['availableSeats'], ticket['isActive'], ticket['idSection'])
            cursor.execute(query_ticket,val) """
    cnx.commit()
    cursor.close()
    cnx.close()
    return True

async  def fillChildTables(nameDataBase):
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['host'] ,
        user= mysqlConector['user'],
        port =   mysqlConector['port'],
        password= mysqlConector['password'],
        database= nameDataBase
    )   
    cursor = cnx.cursor()
    with open('./dataBook/settings.json') as f:
        jsonData = json.load(f)
        for user in jsonData['users']:
            query_users = '''
                INSERT INTO settings_users (name, lastname, lastname_2, email, `password`, phone_number, id_rol, isActive, createAt, is_reset_password, user_type, fan_id)VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            val = (user['name'],user['lastname'],user['lastname2'],user['email'],user['password'],user['phoneNumber'],user['idRol'],user['isActive'],user['createAt'],user['isResetPassword'],user['userType'],user['idFan'])
            cursor.execute(query_users,val)
            cnx.commit()

        
        for submodule in jsonData['submodules']:
            query_submodule = '''
                    INSERT INTO settings_submodules (name, description, isActive, createAt, id_module, id_user)
                    VALUES(%s, %s, %s, %s, %s, %s);
            '''
            val = (submodule['name'], submodule['descrition'], submodule['isActive'], submodule['createAt'], submodule['idModule'], submodule['idUser'])
            cursor.execute(query_submodule,val)
            cnx.commit()

        for  permition in jsonData['permitions']:
            query_permition = '''  
                INSERT INTO settings_permitions (id_module, id_submodule, id_action, id_user)
                VALUES (%s, %s, %s, %s);
            '''
            val = (permition['idModule'], permition['idSubmodule'], permition['idAction'], permition['idUser'])
            cursor.execute(query_permition,val)
            cnx.commit()
        
        
        for permitionRole in jsonData['rolePermitions']:
            query_role_permition = '''
                INSERT INTO settings_role_permitions (id_rol, id_permition)
                VALUES(%s,%s);
            '''            
            val  =(permitionRole['idRol'], permitionRole['idPermition'])
            cnx.commit()

        for fee in jsonData['fees']:
            query_fee = '''
                INSERT INTO settings_fees ( name, value, type_fees, title, subtitle, description, type_application, forced, is_active, id_group)
                VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s,%s);
            '''
            val = (fee['name'], fee['value'], fee['typeFees'], fee['title'], fee['subtitle'], fee['description'], fee['typeApplication'], fee['forced'], fee['isActive'], fee['idGroup'])
            cursor.execute(query_fee,val)
            cnx.commit()

        for eventClassification in jsonData['eventClasifications']:
            query_event_clasification = '''
                INSERT INTO settings_event_classification  (name, description, isActive)
                VALUES(%s,%s,%s);
            '''
            val = (eventClassification['name'], eventClassification['description'], eventClassification['isActive'])
            cursor.execute(query_event_clasification,val)
            cnx.commit()
        

        for ticket in jsonData['tickets']:
            query_ticket = '''
                INSERT INTO settings_tickets (name, description, path, id_enclosure, available_seats, isActive, id_section)
                VALUES(%s, %s, %s, %s, %s, %s, %s);
            '''
            val = (ticket['name'], ticket['descrition'], ticket['path'], ticket['idEnclosure'], ticket['availableSeats'], ticket['isActive'], ticket['idSection'])
            cursor.execute(query_ticket,val)
            cnx.commit() 
    
    cursor.close()
    cnx.close()
    return True


async def insertions (nameDataBase):   
    await fillMainTables(nameDataBase)
    await fillChildTables(nameDataBase)




