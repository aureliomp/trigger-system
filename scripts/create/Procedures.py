import mysql.connector
import config

# https://www.youtube.com/shorts/jN7WAU-r11Y
async def create(nameNewDatabase):
    mysqlConector = config.load_info()
    cnx  = mysql.connector.connect(
    host= mysqlConector['host'] ,
    user= mysqlConector['user'],
    port =   mysqlConector['port'],
    password= mysqlConector['password'],
    database=nameNewDatabase
    )
    cursor = cnx.cursor()
    query = '''
        #
        CREATE PROCEDURE sp_get_assistance_heat_map(
            idEvent INT
        )
        BEGIN
            ### get all chuncks 
            SELECT 
                ec.id_chunk AS idChunck,
                ec.name AS nameChunk,
                ec.id_svg AS idSVG,
                ec.row_total AS totalRows,
                ec.column_total AS totalColumns,
                0 AS soldSeat
            FROM enclosure_chunk ec 
            INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
            WHERE es.id_enclosure =@enclosure;
                
            ### get seats sold order by chunks 
            SELECT 
                ec.id_chunk AS idChunck,
                ec.name AS nameChunk,
                ec.id_svg AS idSVG,
                ec.row_total AS totalRows,
                ec.column_total AS totalColumns,
                COUNT(ert.id_ert) AS soldSeats
            FROM event_reservations er 
            INNER JOIN event_reservations_tickets ert  ON ert.id_reservation = er.id_reservation
            INNER JOIN enclosure_chunk ec ON ec.id_svg = ert.id_chunk 
            WHERE er.id_event = @id AND er.status = 'PAID'
            GROUP BY ec.id_chunk;

            ### get seats sold and  confirm  by chuncks
            SELECT 
                ec.id_chunk AS idChunck,
                ec.name AS nameChunk,
                ec.id_svg AS idSVG,
                ec.row_total AS totalRows,
                ec.column_total AS totalColumns,
                COUNT(ert.id_ert) AS soldSeats
            FROM event_reservations er 
            INNER JOIN event_reservations_tickets ert  ON ert.id_reservation = er.id_reservation
            INNER JOIN enclosure_chunk ec ON ec.id_svg = ert.id_chunk 
            WHERE er.id_event = @id AND er.status = 'PAID' AND ert.is_check 
            GROUP BY ec.id_chunk;
        END;

        CREATE PROCEDURE sp_get_assistance_per_event(
            idEvent INT
        )
        BEGIN
            SET @id =  idEvent;
            SET @enclosure = (SELECT e.id_enclosure  FROM events e WHERE e.id_event = @id);
            ### get all sections of event
            SELECT 
                es.id_section AS idSection,
                es.name  AS nameSection,
                0 AS totalTickets
            FROM enclosure_section es WHERE  es.id_enclosure = @enclosure;


            ### get all section with assitance
            SELECT 
                es.id_section AS idSection ,
                es.name AS nameSection,
                COUNT(ert.id_ert) AS totalTickets
            FROM  event_reservations er 
            LEFT JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation
            LEFT JOIN enclosure_section es ON es.id_section = ert.id_section 
            WHERE er.id_event = @id AND er.status = 'PAID'
            GROUP BY es.id_section;

            ### get assistance check
            SELECT 
                es.id_section AS idSection ,
                es.name AS nameSection,
                COUNT(ert.id_ert) AS totalTickets
            FROM  event_reservations er 
            LEFT JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation
            LEFT JOIN enclosure_section es ON es.id_section = ert.id_section 
            WHERE er.id_event = @id AND er.status = 'PAID' AND ert.is_check 
            GROUP BY es.id_section;

        END;

        CREATE PROCEDURE sp_get_event_data(
            idEvent int
        )
        BEGIN
            SET @id =idEvent;
            SET @enclouse = (SELECT e.id_enclosure FROM events e WHERE e.id_event = @id);
            
            ### general data 
            SELECT 
            e.id_event AS id,
            e.name,
            DATE_FORMAT(e.date_event, '%Y-%m-%d')  AS dateEvent,
            e.time_event AS timeEvent,
            e.is_public AS isPublic,
            e.situation ,
            e.status,
            e.share_path AS sharePath,
            e.post_sale AS postSale,
            se.id_enclosure AS idEnclosure,
            se.name AS encluse,
            se.enclosure_address AS address,
            sc.id_category AS idClasification,
            sc.name AS clasification,
            m.id_media AS idMedia,
            e.time_zone_name AS timeZone,
            m.url,
            (SELECT url FROM media WHERE id_event = @id AND name = 'Flayer' ORDER BY id_media DESC LIMIT 1) AS flayerUrl,
            (SELECT id_media FROM media WHERE id_event = @id AND name = 'Flayer' ORDER BY id_media DESC LIMIT 1) AS flayerIdMedia,
            (SELECT url FROM media WHERE id_event = @id AND name = 'mini_flayer' ORDER BY id_media DESC LIMIT 1) AS miniFlayerUrl,
            (SELECT id_media FROM media WHERE id_event = @id AND name = 'mini_flayer' ORDER BY id_media DESC LIMIT 1) AS miniFlayerIdMedia,
            me.id_media AS idMediaEnclosure,
            me.url AS urlEnclosure,
            sec.name AS nameClasification,
            et.id_type AS idType,
            et.name AS nameType,
            e.inbropi_fees AS inbropiFees
            FROM events e
            LEFT JOIN settings_enclosure se ON se.id_enclosure =  e.id_enclosure 
            LEFT JOIN settings_event_classification  sc ON sc.id_category = e.id_type_event 
            LEFT JOIN media m ON m.id_event = e.id_event
            LEFT JOIN media me ON me.id_enclosure = e.id_enclosure
            LEFT JOIN settings_event_classification sec ON sec.id_category = e.id_clasification 
            LEFT JOIN event_types et ON et.id_type = e.id_type_event
            WHERE  e.id_event = @id AND m.name = 'Flayer';


        ### get coupons
            SELECT 
                ec.id_coupon AS id,
                ec.type_coupon AS typeCounpon,
                ec.key_word,
                ec.value ,
                ec.amount_coupon AS amountCoupon,
                IFNULL(ec.start_date,'')  AS startDate,
                IFNULL(ec.end_date,'')  AS endDate
            FROM event_coupons ec
            WHERE ec.id_event = @id;

        ### ticket paid 
            SELECT 
                st.id_ticket AS idTicket,
                st.name ,
                et.price,
                es.class_name AS className
            FROM  settings_tickets st   
            INNER JOIN event_ticket et ON  et.id_ticket  = st.id_ticket
            INNER JOIN enclosure_section es ON es.id_section = st.id_section 
            WHERE st.id_enclosure = @enclouse AND et.id_event = @id
            ORDER BY et.create_at  ASC ; 

        #### all tickets
        SELECT 
            st.id_ticket AS idTicket,
            st.name ,
            et.price,
            es.class_name AS className
        FROM  event_ticket et
        LEFT JOIN settings_tickets st ON st.id_ticket = et.id_ticket 
        LEFT JOIN enclosure_section es ON es.id_section = st.id_section 
        WHERE  st.id_enclosure = @enclouse AND et.id_event = @id;


        ### event fees 
        SELECT 
            ef.id_event_fees  AS id,
            ef.amount ,
            ef.apply ,
            sf.type_fees AS typeFees,
            sf.title ,
            sf.subtitle ,
            sf.description,
            sf.type_application AS typeApplication,
            sf.forced AS forced,
            sfg.name AS groupName
        FROM  event_fees ef 
        INNER JOIN settings_fees sf ON sf.id_fees = ef.id_fees 
        INNER JOIN settings_fees_group sfg ON sfg.id_group = sf.id_group 
        WHERE sfg.is_active  AND  ef.id_event = @id;

        ### section to get Assistance reservation
        SELECT 
            er.id_reservation AS id,
            IFNULL(
                (
                    SELECT CONCAT_WS(' ', c.name, c.lastname, c.lastname_2 ) FROM customer c  WHERE c.id_user = er.fan_id LIMIT 1
                ), 'INVITADO'
            )  AS fullName,
            er.type_ticket AS typeTicket,
            DATE_FORMAT(er.create_at,'%Y/%m/%d %H:%i') AS  dateTicket,
            er.total_tickets  AS totalTickets
        FROM event_reservations er 
        WHERE  er.id_event = @id AND er.status = 'PAID';

        ### paid  tickets 
            SELECT 
                er.id_reservation AS idReservation,
                IFNULL(er.type_payment,'--')  AS typePayment,
                (SELECT ROUND((er.total),2)) AS amount ,
                er.status,
                DATE_FORMAT(er.create_at,'%Y/%m/%d   %H:%i')  AS createAt,
                'PAGADO'
            FROM event_reservations er
            WHERE er.id_event = @id AND er.status = 'PAID';

        ### get presales
        SELECT 
            ep.id_pre_sale AS idPresale,
            DATE_FORMAT(ep.date_start , '%Y-%m-%d') AS startDate ,
            DATE_FORMAT(ep.date_end , '%Y-%m-%d') AS endDate,
            ep.name ,
            ep.is_active AS isActive,
            epsz.id_zone ,
            epsz.price ,
            es.name,
            es.class_name AS className,
            st.id_ticket AS idTicket
        FROM  event_pre_sale ep 
        INNER JOIN event_pre_sale_zones epsz ON epsz.id_pre_sale = ep.id_pre_sale 
        INNER JOIN enclosure_section es ON es.id_section = epsz.id_zone 
        INNER JOIN settings_tickets st ON st.id_section = es.id_section 
        WHERE ep.id_event = @id AND ep.is_active;
    END; 
    
    CREATE  PROCEDURE sp_get_event_preview(
        idEvent INT
    )
    BEGIN
        SET @id = idEvent;

    ### get preview event info
    SELECT 
        e.share_path  AS sharePath,
        ( 
            CONCAT_WS(' ',
                DATE_FORMAT(e.date_event, '%Y-%m-%d'),
                DATE_FORMAT(e.time_event, '%H:%i') 
            ) 
        ) AS dateAndTime,
        sec.name AS clasification,
        se.name AS enclosure,
        m.url ,
        se.enclosure_address AS address
    FROM events e 
    LEFT JOIN settings_event_classification sec ON sec.id_category = e.id_clasification
    LEFT JOIN settings_enclosure se ON se.id_enclosure = e.id_enclosure 
    LEFT JOIN media m ON m.id_enclosure = se.id_enclosure 
    WHERE  e.id_event = @id;


    ### get preview tickets per event id
    SELECT 
        st.id_ticket AS idTicket,
        st.name ,
        et.price,
        es.class_name AS className
    FROM  event_ticket et
    LEFT JOIN settings_tickets st ON st.id_ticket = et.id_ticket 
    LEFT JOIN enclosure_section es ON es.id_section = st.id_section 
    WHERE  et.id_event = @id;

    ### get preview fees per event id
    SELECT 
        ef.id_event_fees  AS id,
        ef.amount ,
        ef.apply ,
        sf.type_fees AS typeFees,
        sf.title ,
        sf.subtitle ,
        sf.description,
        sf.type_application AS typeApplication,
        sf.forced AS forced,
        sfg.name AS groupName
    FROM  event_fees ef 
    INNER JOIN settings_fees sf ON sf.id_fees = ef.id_fees 
    INNER JOIN settings_fees_group sfg ON sfg.id_group = sf.id_group 
    WHERE sfg.is_active AND  ef.id_event = @id;
    END ;


    CREATE PROCEDURE sp_get_event_seats(
        idEvent INT,
        idZone  INT,
        chunk VARCHAR(50)
    )
    BEGIN
        SET @id = idEvent;
        SET @sectionID = idZone;
        SET @chunk = chunk;
        SET @enclosure = (SELECT e.id_enclosure  FROM events e WHERE e.id_event = @id);
        IF @sectionID IS NULL THEN 
            SET @sectionID = (SELECT es.id_section FROM enclosure_chunk ec INNER JOIN enclosure_section es ON ec.id_section = es.id_section WHERE ec.id_svg = @chunk);
        END IF;
        

    ### get all rows 
        SELECT 
            er.id_row AS idRow,	
            er.num_seat AS seat,
            er.row_name AS `row`,
            ec.id_svg  AS idChunk,
            er.`show`,
            ec.name AS chunk,
            es.id_section AS idSection,
            es.name AS `section`,
            'AVALIABLE' AS status
        FROM  enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section
        WHERE 
        es.id_enclosure = @enclosure AND 
        es.id_section = @sectionID AND 
        ec.id_svg = @chunk;


    ### get reserved rows
    SELECT 
        rowE.id_row AS idRow,
        rowE.num_seat AS seat,
        rowE.row_name AS `row`,
        ec.id_svg  AS idChunk,
        true AS `show`,
        ec.name AS chunk,
        es.id_section AS idSection,
        es.name AS `section`,
        er.status
    FROM  event_reservations er
    INNER JOIN events e ON e.id_event = er.id_event
    INNER JOIN event_reservations_tickets ert  ON ert.id_reservation = er.id_reservation 
    INNER JOIN enclosure_row rowE ON rowE.id_row = ert.id_row 
    INNER JOIN enclosure_chunk ec ON ec.id_chunk = rowE.id_chunk  
    INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
    WHERE er.id_event = @id AND ec.id_section  = @sectionID 
    -- AND rowE.id_svg_chunk = @chunk 
    AND NOT er.status = 'CANCEL';

    ### set MADMAX
            SET @DR_TAILOR = (
                        SELECT MAX(totalCounter) AS MAX_LENGTH FROM ( 
                    SELECT 
                        er.row_name AS nameRow,
                        COUNT(er.id_row) AS totalCounter
                    FROM enclosure_row er
                    INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
                    INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
                    INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
                    WHERE  se.id_enclosure = @enclosure
                    GROUP BY er.row_name
                ) AS c
            );
        
        
    ### total length row
        SELECT 
            er.row_name AS `row`,
            ec.column_total  AS `column`
        FROM enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk 
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
        WHERE  se.id_enclosure = 2
        GROUP BY er.row_name, ec.column_total 
    ;

    ### max 
        SELECT MAX(totalCounter) AS MAX_LENGTH FROM ( 
            SELECT 
                er.row_name AS nameRow,
                COUNT(er.id_row) AS totalCounter
            FROM enclosure_row er
            INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
            INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
            INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
            WHERE  se.id_enclosure = @enclosure
            GROUP BY er.row_name
        ) AS Macarov;


    ### get total column
        SELECT 
            er.row_name 	
        FROM  enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        WHERE es.id_enclosure = @enclosure AND  ec.id_svg = @chunk
        GROUP BY er.row_name
        ;
        
    END ;
    

    CREATE  PROCEDURE sp_get_event_seats_CTM(
        nameSection  INT
    )
    BEGIN
        SET @id = idEvent;
        SET @nameSection = nameSection;
        SET @enclosure = (SELECT e.id_enclosure  FROM events e WHERE e.id_event = @id);

        ## get all seats of table
    SELECT
        er.id_row AS idRow,
        er.num_seat AS seat,
        er.row_name AS `row`,
        es.id_section AS idSection,
        es.name AS `section`,
        er.id_chunk AS idChunk,
        'AVALIABLE' AS status,
        (TRUE) AS `show`,
        ec.id_chunk AS idChunk,
        ec.name AS chunk
    FROM events e 
    LEFT JOIN event_ticket et ON et.id_event = e.id_event 
    LEFT JOIN settings_enclosure se ON se.id_enclosure = e.id_enclosure 
    LEFT JOIN enclosure_section es ON es.id_enclosure = se.id_enclosure 
    LEFT JOIN enclosure_chunk ec ON ec.id_section = es.id_section 
    LEFT JOIN enclosure_row er ON er.id_chunk = ec.id_chunk 
    WHERE e.id_event = @id AND ec.name = @nameSection
    GROUP BY er.id_row,es.name,es.id_section, ec.id_chunk,ec.name;

    ## get seats resserved 

    SELECT 
        ert.id_chunk AS idChunk,
        ert.id_section AS idSection,
        ert.status,
        ert.id_event AS idEvent ,
        ert.id_row AS idRow,
        erow.row_name AS `row`,
        erow.num_seat AS seat,
        ec.id_chunk AS idChunk,
        ec.name AS chunk,
        es.id_section AS idSection,
        es.name AS `section`,
        (TRUE) AS `show`
    FROM  event_reservations er
    INNER JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation 
    INNER JOIN enclosure_row erow ON erow.id_row = ert.id_row 
    INNER JOIN enclosure_chunk ec ON ec.id_chunk = erow.id_chunk 
    INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
    WHERE er.id_event = @id AND NOT er.status = 'CANCEL' AND ec.name = @nameSection 
    ;
    END ;


    CREATE PROCEDURE sp_get_seats_checked(
        idEvent INT,
        idZone  INT,
        chunk INT
    )
    BEGIN
        SET @id = idEvent;
            SET @sectionID = idZone;
            SET @chunk = chunk;
            SET @enclosure = (SELECT e.id_enclosure  FROM events e WHERE e.id_event = @id);
            IF @sectionID IS NULL THEN 
                SET @sectionID = (SELECT es.id_section FROM enclosure_chunk ec INNER JOIN enclosure_section es ON ec.id_section = es.id_section WHERE ec.id_svg = @chunk);
            END IF;
    #### get all tickets
        SELECT 
            er.id_row AS idRow,	
            er.num_seat AS seat,
            er.row_name AS `row`,
            ec.id_svg  AS idChunk,
            er.`show`,
            ec.name AS chunk,
            es.id_section AS idSection,
            es.name AS `section`,
            (FALSE) AS isCheck,
            (NULL) AS idTicket
        FROM  enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section
        WHERE es.id_enclosure = @enclosure AND es.id_section = @sectionID AND ec.id_svg = @chunk;

    ### get tickets with status checkin 
    SELECT 
        rowE.id_row AS idRow,
        ert.seat_num  AS seat,
        rowE.row_name AS `row`,
        ec.id_svg  AS idChunk,
        true AS `show`,
        ec.name AS chunk,
        es.id_section AS idSection,
        es.name AS `section`,
        er.status,
        ert.is_check AS isCheck,
        ert.id_ert AS idTicket
    FROM  event_reservations er
    INNER JOIN events e ON e.id_event = er.id_event
    INNER JOIN event_reservations_tickets ert  ON ert.id_reservation = er.id_reservation 
    INNER JOIN enclosure_row rowE ON rowE.id_row = ert.id_row 
    INNER JOIN enclosure_chunk ec ON ec.id_chunk = rowE.id_chunk  
    INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
    WHERE er.id_event = @id AND ec.id_section  = @sectionID AND rowE.id_svg_chunk = @chunk AND ert.is_check ;

    ### set MADMAX
            SET @DR_TAILOR = (
                        SELECT MAX(totalCounter) AS MAX_LENGTH FROM ( 
                    SELECT 
                        er.row_name AS nameRow,
                        COUNT(er.id_row) AS totalCounter
                    FROM enclosure_row er
                    INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
                    INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
                    INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
                    WHERE  se.id_enclosure = @enclosure
                    GROUP BY er.row_name
                ) AS c
            );
        
        
    ### total length row
        SELECT 
            er.row_name AS `row`,
            @DR_TAILOR AS `column`
        FROM enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk 
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
        WHERE  se.id_enclosure = @enclosure
        GROUP BY er.row_name
    ;

    ### max 
        SELECT MAX(totalCounter) AS MAX_LENGTH FROM ( 
            SELECT 
                er.row_name AS nameRow,
                COUNT(er.id_row) AS totalCounter
            FROM enclosure_row er
            INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
            INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
            INNER JOIN settings_enclosure se ON se.id_enclosure = es.id_enclosure  
            WHERE  se.id_enclosure = @enclosure
            GROUP BY er.row_name
        ) AS Macarov;


    ### get total column
        SELECT 
            er.row_name 	
        FROM  enclosure_row er
        INNER JOIN enclosure_chunk ec ON ec.id_chunk  = er.id_chunk
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        WHERE es.id_enclosure = @enclosure AND  ec.id_chunk = @sectionID
        GROUP BY er.row_name
        ;
    END ;
    

    CREATE PROCEDURE sp_get_table_financial(
        monthNumber INT, 
        currentYear INT
    )
    BEGIN
        SET @m = monthNumber;
        SET @y = currentYear;
        SET @costs = (
            SELECT  
                (
                    IFNULL(SUM(er.sub_total),0)  + IFNULL(SUM(er.total_fees),0) 
                ) AS total
            FROM event_reservations er
            WHERE  MONTH(er.create_at) = @m AND YEAR(er.create_at) = @y
        );
        SET @expenses = (
        SELECT 
            IFNULL(SUM(eb.amount),0)  AS total 
        FROM events_bill eb WHERE MONTH(eb.create_at) = @m AND YEAR(eb.create_at) = @y
        );
        SET @grossMargin = @costs - @expenses;
        # total earnings
        SELECT  
            (
                IFNULL(SUM(er.sub_total) + SUM(er.total_fees),0) 
            ) AS total
        FROM event_reservations er
        WHERE  MONTH(er.create_at) = @m AND YEAR(er.create_at) = @y
        ;
        
        
        ## total tickets 
        SELECT 
            IFNULL(SUM(er.sub_total),0)  AS total
        FROM event_reservations er 
        WHERE er.status = 'PAID' 
        AND er.mpp_transaction  NOT LIKE  '%A%' 
        AND MONTH(er.create_at) = @m 
        AND YEAR(er.create_at) = @y;
        
        
        ## total gateway
        SELECT 
            IFNULL(SUM(er.fee_payment_gateway),0)  AS totalGateway
        FROM event_reservations er WHERE MONTH(er.create_at) = @m AND YEAR(er.create_at) = @y;
        
        ### total expences 
        SELECT 
            IFNULL(SUM(eb.amount),0)  AS total 
        FROM events_bill eb WHERE MONTH(eb.create_at) = @m AND YEAR(eb.create_at) = @y;
        
        ### grossMargin
        SELECT @grossMargin AS grossMargin;
        
        ### url 
        SELECT bm.url AS url  FROM bill_media bm WHERE bm.`month` = @m AND bm.`year` = @y;
        
    END;

    CREATE PROCEDURE sp_get_tickets(
        idReservation INT
    )
    BEGIN
        SET @id = idReservation; 
        SELECT 
            er.id_reservation  AS idReservation,
            er.id_event AS idEvent,
            erow.num_seat  AS seatNum,
            ert.id_ert AS idTicket,
            erow.row_name AS rowName,
            ert.price,
            ert.id_row AS idRow,
            ec.name AS chunk,
            es.name AS nameSection,
            ert.id_fan AS idFan,
            e.name,
            e.time_event AS timeEvent,
            DATE_FORMAT(e.date_event,'%Y/%m/%d') AS dateEvent,
            se.name AS enclosure,
            er.total_fees AS totalFees,
            se.enclosure_address AS enclosureAddress,
            m.url AS mediaEvent,
            (
                SELECT sf.title  FROM event_fees e
                LEFT JOIN settings_fees sf ON e.id_fees = sf.id_fees 
                WHERE id_event_fees IN (SELECT id_fees FROM event_fees_reservation WHERE id_reservation = @id AND sf.id_fees IN (3,4))

    
            ) AS typeTicket
        FROM event_reservations er
        INNER JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation
        INNER JOIN enclosure_row erow ON erow.id_row = ert.id_row 
        INNER JOIN enclosure_chunk ec ON ec.id_chunk = erow.id_chunk 
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        INNER JOIN events e ON e.id_event = er.id_event 
        INNER JOIN settings_enclosure se ON se.id_enclosure = e.id_enclosure 
        INNER JOIN media m ON m.id_event = e.id_event 
        WHERE er.id_reservation = @id AND 
        NOT ert.has_printed  AND er.status = 'PAID' AND m.name = 'Flayer';

    END;

    CREATE PROCEDURE sp_get_tickets_by_id_ticket(
        idTicket INT
    )
    BEGIN
        
        SET @id = idTicket;
        SET lc_time_names = 'es_ES';
    SELECT 
            er.id_reservation  AS idReservation,
            erow.num_seat  AS seatNum,
            ert.id_ert AS idTicket,
            erow.row_name AS rowName,
            ert.price,
            ert.price AS unitPrice,
            ert.id_event AS idEvent,
            ert.id_reservation AS idReservation,
            ert.id_row AS idRow,
            ec.name AS chunk,
            es.name AS nameSection,
            ert.id_fan AS idFan,
            e.name AS nameEvent,
            e.time_event AS timeEvent,
            DATE_FORMAT(e.date_event,'%W %e %M %Y') AS dateEvent,
            se.name AS enclosure,
            se.enclosure_address AS enclosureAddress,
            m.url AS mediaEvent,
            er.type_ticket AS typeTicket
        FROM event_reservations er
        INNER JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation
        INNER JOIN enclosure_row erow ON erow.id_row = ert.id_row 
        INNER JOIN enclosure_chunk ec ON ec.id_chunk = erow.id_chunk 
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        INNER JOIN events e ON e.id_event = er.id_event 
        INNER JOIN settings_enclosure se ON se.id_enclosure = e.id_enclosure 
        INNER JOIN media m ON m.id_event = e.id_event 
        WHERE ert.id_ert  = @id AND NOT ert.has_printed  AND er.status = 'PAID' AND m.name = 'Flayer';
        
    END;

    CREATE PROCEDURE sp_get_tickets_from_las_event(idEnclosure int)
    BEGIN
        SET @enclouse = idEnclosure;
        SET @LAST_ID_EVENT = (SELECT MAX(e.id_event) AS lastId FROM events e);

    ### tickets paid
    SELECT 
        st.id_ticket AS idTicket,
        st.name ,
        et.price,
        es.class_name AS className
    FROM  settings_tickets st   
    INNER JOIN event_ticket et ON  et.id_ticket  = st.id_ticket
    INNER JOIN enclosure_section es ON es.id_section = st.id_section 
    WHERE st.id_enclosure = @enclouse AND et.id_event =  @LAST_ID_EVENT
    ORDER BY et.create_at  ASC ; 

    #### all tickets
    SELECT 
        st.id_ticket AS idTicket,
        st.name ,
        0 AS price  
    FROM  settings_tickets st   
    WHERE  st.id_enclosure = @enclouse;
    END ;

    CREATE PROCEDURE sp_get_ticket_by_id_reservation(
        idReservation INT
    )
    BEGIN
        SET @id = idReservation;
        SET lc_time_names = 'es_ES';
        SELECT 
            er.id_reservation  AS idReservation,
            erow.num_seat  AS seatNum,
            ert.id_ert AS idTicket,
            erow.row_name AS rowName,
            ( 
                (
                    SELECT 
                        IFNULL(SUM(ef.amount),0)
                    FROM event_fees_reservation efr 
                    INNER JOIN event_fees ef ON ef.id_event_fees = efr.id_fees 
                    INNER JOIN settings_fees sf ON sf.id_fees = ef.id_fees 
                    WHERE  efr.id_reservation = @id  AND sf.type_application = 'TICKET' AND sf.type_fees = 'CASH'
                ) + ert.price
            ) AS price,
            ert.price AS unitPrice,
            ert.id_row AS idRow,
            ec.name AS chunk,
            es.name AS nameSection,
            ert.id_fan AS idFan,
            e.name AS nameEvent,
            e.time_event AS timeEvent,
            DATE_FORMAT(e.date_event,'%W %e %M %Y') AS dateEvent,
            se.name AS enclosure,
            se.enclosure_address AS enclosureAddress,
            m.url AS mediaEvent,
            er.type_ticket AS typeTicket,
            er.fee_payment_gateway  AS totalFees
        FROM event_reservations er
        INNER JOIN event_reservations_tickets ert ON ert.id_reservation = er.id_reservation
        INNER JOIN enclosure_row erow ON erow.id_row = ert.id_row 
        INNER JOIN enclosure_chunk ec ON ec.id_chunk = erow.id_chunk 
        INNER JOIN enclosure_section es ON es.id_section = ec.id_section 
        INNER JOIN events e ON e.id_event = er.id_event 
        INNER JOIN settings_enclosure se ON se.id_enclosure = e.id_enclosure 
        INNER JOIN media m ON m.id_event = e.id_event 
        WHERE er.id_reservation = @id AND NOT ert.has_printed  AND er.status = 'PAID' AND m.name = 'Flayer';

    ### get all fees that typpe ticket and type percent
    SELECT
        IFNULL(ef.amount,0) AS amount
    FROM event_fees_reservation efr 
    INNER JOIN event_fees ef ON ef.id_event_fees = efr.id_fees 
    INNER JOIN settings_fees sf ON sf.id_fees = ef.id_fees 
    WHERE  efr.id_reservation = @id  AND sf.type_application = 'TICKET' AND sf.type_fees = 'PERCENT';
        
    END ;

    CREATE PROCEDURE sp_login_user(
        email varchar(200)
    )
    BEGIN
        SET @emailUser = email;
        SET @rol = (SELECT su.id_rol AS idRol  FROM  settings_users su WHERE su.email = @emailUser);
        SELECT 
            su.id_user AS id,
            CONCAT_WS(' ', su.name,su.lastname,su.lastname_2) AS userName,
            su.name,
            su.lastname,
            su.lastname_2 AS lastname2 
        FROM  settings_users su 
        WHERE  su.user_type  = 'ADMIN' AND su.email = @emailUser;

    SELECT 
        sr.id_rol AS id,
        sr.name
    FROM settings_roles sr 
    WHERE sr.id_rol = @rol; 

    SELECT 
        srp.id_rol ,
        srp.id_permition AS idPermition
    FROM  settings_role_permitions srp
    WHERE  srp.id_rol  = @rol;

    SELECT 
        sa.id_action AS id,
        sa.name,
        (false) AS assigned
    FROM settings_actions sa;

    SELECT 
        sm.id_module AS id,
        sm.name 
    FROM settings_modules sm;

    SELECT 
        ss.id_submodule AS id,
        ss.name ,
        ss.id_module AS idModule
    FROM settings_submodules ss; 

    END ;


    #
    '''
    cursor.execute(query)
    cursor.close()
    cnx.close()
    return 'success'