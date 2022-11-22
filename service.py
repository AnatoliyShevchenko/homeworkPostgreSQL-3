from typing import Any
import psycopg2
from psycopg2.extensions import (ISOLATION_LEVEL_AUTOCOMMIT, connection as Connection, cursor as Cursor)
from dotenv import load_dotenv

from config import (HOST, PORT, PASSWORD, USER,)

class Connection:
    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Connection Successful')
            cursor = self.connection.cursor()
            cursor.execute("CREATE DATABASE workonclass3;")
            print('Database is successful created!')
        except:
            try:
                self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database='workonclass3'
                )
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                print('Connection successful')
            except:
                print('all is created')

    def __new__(cls: type[Any]) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)

        return cls.instance

    def create_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(70), 
                    login VARCHAR(50) UNIQUE, 
                    password VARCHAR(50));

                CREATE TABLE IF NOT EXISTS articles(
                    id SERIAL PRIMARY KEY, 
                    title VARCHAR(70), 
                    content TEXT, 
                    user_id INTEGER);    
            """)
        self.connection.commit()
        print('[INFO] table is created!')

    def create_user(self, name: str, login: str, password: str) -> str:
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO users(name, login, password)
                VALUES ('{name}','{login}','{password}');
            """)
        self.connection.commit()
        print('[INFO] user is created!')

    def get_user(self) -> list[tuple]:
        data: list[tuple] 
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT * FROM users;""")
            data = cur.fetchall()
        self.connection.commit()
        print('[INFO] user is created!')
        return data

    def close_connection(self):
        # self.cursor.close()
        self.connection.close()
        print('[INFO] connection is close')
