from configparser import ConfigParser
import psycopg2


class Database:

    def __init__(self):
        conn, cur = self.__connect_open()
        self.__create_table(cur)
        self.__connect_close(cur, conn)

    def insert_data_for_search(self, name, content):
        conn, cur = self.__connect_open()
        insert_query = """ INSERT INTO data (name, content) VALUES (%s,%s)"""
        record_to_insert = (name, content)
        cur.execute(insert_query, record_to_insert)
        self.__connect_close(cur, conn)

    def get_all_data(self):
        conn, cur = self.__connect_open()
        cur.execute('SELECT * FROM data')
        result = cur.fetchall()
        self.__connect_close(cur, conn)
        return result

    def delete_data(self):
        conn, cur = self.__connect_open()
        delete_query = """DROP TABLE IF EXISTS data"""
        cur.execute(delete_query)
        self.__create_table(cur)
        self.__connect_close(cur, conn)

    @staticmethod
    def get_all_sentences(result_data):
        all_sentences = []

        for index, item in enumerate(result_data):
            all_sentences.append(result_data[index][2])

        return all_sentences

    def add_user(self, name, login, password):
        conn, cur = self.__connect_open()
        insert_query = """ INSERT INTO customer (name, login, password) VALUES (%s,%s,%s)"""
        record_to_insert = (name, login, password)
        cur.execute(insert_query, record_to_insert)
        self.__connect_close(cur, conn)

    @staticmethod
    def __create_table(cur):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS data
            (
                    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                    name text COLLATE pg_catalog."default" NOT NULL,
                    content text COLLATE pg_catalog."default" NOT NULL,
                    CONSTRAINT data_pkey PRIMARY KEY (id),
                    CONSTRAINT uq_data_name UNIQUE (name)
            );
            """
        )

    def __connect_open(self):
        try:
            params = self.__config()
            conn = psycopg2.connect(**params)
            return conn, conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def __connect_close(cur, conn):
        try:
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def __config(filename='db/database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        db = {}

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
