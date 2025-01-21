import mysql.connector
import config


async def create (nameNewDatabase):
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
        host= mysqlConector['mysql']['host'] ,
        user= mysqlConector['mysql']['user'],
        port =   mysqlConector['mysql']['port'],
        password= mysqlConector['mysql']['password'],
        database=nameNewDatabase
    )
    cursor = cnx.cursor()
    query = '''
        CREATE  TRIGGER `create_event_tickets` AFTER INSERT ON `events` FOR EACH ROW INSERT INTO event_ticket (id_event,id_ticket,price)SELECT new.id_event,st.id_ticket,0 FROM settings_tickets st INNER JOIN settings_enclosure se ON se.id_enclosure = st.id_enclosure
        INNER JOIN events e  ON e.id_enclosure = se.id_enclosure 
        WHERE st.id_enclosure = e.id_enclosure AND st.isActive AND e.id_event = new.id_event;

        CREATE  TRIGGER `create_event_fees` AFTER INSERT ON `events` FOR EACH ROW INSERT INTO event_fees (id_event,id_fees,amount)SELECT new.id_event, sf.id_fees,sf.value  FROM settings_fees sf WHERE sf.is_active;
        
        CREATE  TRIGGER `add_reservations` AFTER INSERT ON `customer` FOR EACH ROW UPDATE event_reservations er SET 
            er.fan_id = new.id_user
        WHERE er.email = new.email ;
    '''
    cursor.execute(query)
    cursor.close()
    cnx.close()
    return 'success'
