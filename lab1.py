
import psycopg2
import psycopg2.errorcodes
import csv
import itertools
import time
import datetime
import logging



logger = logging.getLogger(__name__)
logging.basicConfig(filename="Lab1.log", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='admin', host='localhost')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS zno_table;')
conn.commit()


def create_table():
    with open("Odata2019File.csv", "r", encoding="cp1251") as csv_file:
        header = csv_file.readline().split(';')
        header = [word.strip('"') for word in header]
        header[-1] = header[-1].rstrip('"\n')
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS zno_table (
            Year INT,
            OUTID VARCHAR(255) PRIMARY KEY,
            Birth NUMERIC,
            SEXTYPENAME VARCHAR(255),
            REGNAME VARCHAR(255),
            AREANAME VARCHAR(255),
            TERNAME VARCHAR(255),
            REGTYPENAME VARCHAR(255),
            TerTypeName VARCHAR(255),
            ClassProfileNAME VARCHAR(255),
            ClassLangName VARCHAR(255),
            EONAME VARCHAR(255),
            EOTYPENAME VARCHAR(255),
            EORegName VARCHAR(255),
            EOAreaName VARCHAR(255),
            EOTerName VARCHAR(255),
            EOParent VARCHAR(255),
            UkrTest VARCHAR(255),
            UkrTestStatus VARCHAR(255),
            UkrBall100 NUMERIC,
            UkrBall12 NUMERIC,
            UkrBall NUMERIC,
            UkrAdaptScale NUMERIC,
            UkrPTName VARCHAR(255),
            UkrPTRegName VARCHAR(255),
            UkrPTAreaName VARCHAR(255),
            UkrPTTerName VARCHAR(255),
            histTest VARCHAR(255),
            HistLang VARCHAR(255),
            histTestStatus VARCHAR(255),
            histBall100 NUMERIC,
            histBall12 NUMERIC,
            histBall NUMERIC,
            histPTName VARCHAR(255),
            histPTRegName VARCHAR(255),
            histPTAreaName VARCHAR(255),
            histPTTerName VARCHAR(255),
            mathTest VARCHAR(255),
            mathLang VARCHAR(255),
            mathTestStatus VARCHAR(255),
            mathBall100 NUMERIC,
            mathBall12 NUMERIC,
            mathBall NUMERIC,
            mathPTName VARCHAR(255),
            mathPTRegName VARCHAR(255),
            mathPTAreaName VARCHAR(255),
            mathPTTerName VARCHAR(255),
            physTest VARCHAR(255),
            physLang VARCHAR(255),
            physTestStatus VARCHAR(255),
            physBall100 NUMERIC,
            physBall12 NUMERIC,
            physBall NUMERIC,
            physPTName VARCHAR(255),
            physPTRegName VARCHAR(255),
            physPTAreaName VARCHAR(255),
            physPTTerName VARCHAR(255),
            chemTest VARCHAR(255),
            chemLang VARCHAR(255),
            chemTestStatus VARCHAR(255),
            chemBall100 NUMERIC,
            chemBall12 NUMERIC,
            chemBall NUMERIC,
            chemPTName VARCHAR(255),
            chemPTRegName VARCHAR(255),
            chemPTAreaName VARCHAR(255),
            chemPTTerName VARCHAR(255),
            bioTest VARCHAR(255),
            bioLang VARCHAR(255),
            bioTestStatus VARCHAR(255),
            bioBall100 NUMERIC,
            bioBall12 NUMERIC,
            bioBall NUMERIC,
            bioPTName VARCHAR(255),
            bioPTRegName VARCHAR(255),
            bioPTAreaName VARCHAR(255),
            bioPTTerName VARCHAR(255),
            geoTest VARCHAR(255),
            geoLang VARCHAR(255),
            geoTestStatus VARCHAR(255),
            geoBall100 NUMERIC,
            geoBall12 NUMERIC,
            geoBall NUMERIC,
            geoPTName VARCHAR(255),
            geoPTRegName VARCHAR(255),
            geoPTAreaName VARCHAR(255),
            geoPTTerName VARCHAR(255),
            engTest VARCHAR(255),
            engTestStatus VARCHAR(255),
            engBall100 NUMERIC,
            engBall12 NUMERIC,
            engDPALevel VARCHAR(255),
            engBall NUMERIC,
            engPTName VARCHAR(255),
            engPTRegName VARCHAR(255),
            engPTAreaName VARCHAR(255),
            engPTTerName VARCHAR(255),
            fraTest VARCHAR(255),
            fraTestStatus VARCHAR(255),
            fraBall100 NUMERIC,
            fraBall12 NUMERIC,
            fraDPALevel VARCHAR(255),
            fraBall NUMERIC,
            fraPTName VARCHAR(255),
            fraPTRegName VARCHAR(255),
            fraPTAreaName VARCHAR(255),
            fraPTTerName VARCHAR(255),
            deuTest VARCHAR(255),
            deuTestStatus VARCHAR(255),
            deuBall100 NUMERIC,
            deuBall12 NUMERIC,
            deuDPALevel VARCHAR(255),
            deuBall NUMERIC,
            deuPTName VARCHAR(255),
            deuPTRegName VARCHAR(255),
            deuPTAreaName VARCHAR(255),
            deuPTTerName VARCHAR(255),
            spaTest VARCHAR(255),
            spaTestStatus VARCHAR(255),
            spaBall100 NUMERIC,
            spaBall12 NUMERIC,
            spaDPALevel VARCHAR(255),
            spaBall NUMERIC,
            spaPTName VARCHAR(255),
            spaPTRegName VARCHAR(255),
            spaPTAreaName VARCHAR(255),
            spaPTTerName VARCHAR(255)
        )
    '''

    cursor.execute(create_table_query)
    conn.commit()
    return header

header = create_table()



def insert_from_csv(f, year, conn, cursor):
 
    start_time = datetime.datetime.now() 
    logger.info(str(start_time) + " opening file " + f + '\n')
    
    with open(f, "r", encoding="cp1251") as csv_file:
        print("Reading " + f  )
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        batches_inserted = 0
        batch_size = 50
        inserted_all = False


        while not inserted_all:
            try:
                insert_query = '''INSERT INTO zno_table (year, ''' + ', '.join(header) + ') VALUES '
                count = 0
                for row in csv_reader:
                    count += 1
                    for key in row:
                        if row[key] == 'null':
                            pass
                        elif key.lower() != 'birth' and 'ball' not in key.lower():
                            row[key] = "'" + row[key].replace("'", "''") + "'"
                        elif 'ball100' in key.lower():
                            row[key] = row[key].replace(',', '.')
                    insert_query += '\n\t(' + str(year) + ', ' + ','.join(row.values()) + '),'

                    if count == batch_size:
                        count = 0
                        insert_query = insert_query.rstrip(',') + ';'
                        cursor.execute(insert_query)
                        conn.commit()
                        batches_inserted += 1
                        insert_query = '''INSERT INTO zno_table (year, ''' + ', '.join(header) + ') VALUES '

                if count != 0:
                    insert_query = insert_query.rstrip(',') + ';'
                    cursor.execute(insert_query)
                    conn.commit()
                inserted_all = True
            except psycopg2.OperationalError as e:
                if e.pgcode == psycopg2.errorcodes.ADMIN_SHUTDOWN:
                    
                    logger.info(str(datetime.datetime.now()) + " lost connection\n")
                    connection_restored = False
                    while not connection_restored:
                        try:
                            conn = psycopg2.connect(dbname='postgres', user='postgres', 
                                password='admin', host='localhost', )
                            cursor = conn.cursor()
                            logger.info(str(datetime.datetime.now()) + " reconecting\n")
                            connection_restored = True
                        except psycopg2.OperationalError as e:
                            pass

                    
                    csv_file.seek(0,0)
                    csv_reader = itertools.islice(csv.DictReader(csv_file, delimiter=';'), 
                        batches_inserted * batch_size, None)
            

    end_time = datetime.datetime.now()
    logger.info(str(end_time) + " -- finished ops\n")
    logger.info('time -- ' + str(end_time - start_time) + '\n\n')

    return conn, cursor

     
conn, cursor = insert_from_csv("Odata2019File.csv", 2019, conn, cursor)
conn, cursor = insert_from_csv("Odata2020File.csv", 2020, conn, cursor)    

def statistical_query():
    query = '''
    SELECT 
        Year, 
        ROUND(avg(engBall100)), 
        REGNAME
    FROM zno_table 
    WHERE physTestStatus = 'Зараховано' 
    GROUP BY Year, REGNAME
'''
    cursor.execute(query)

    with open('result1.csv', 'w', encoding="utf-8") as new_csv_file:
        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerow(["Рік","Бал","Область"])
        for row in cursor:
            csv_writer.writerow(row)


statistical_query()

cursor.close()
conn.close()