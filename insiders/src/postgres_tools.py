import psycopg2
import time


class Postgres:

    def __init__(self, host='localhost',
                 dbname='postgres', user='postgres'):
        try:
            self.conn = psycopg2.connect(f"host={host} dbname={dbname} user={user}")
        except psycopg2.OperationalError:
            time.sleep(12)
            self.conn = psycopg2.connect(f"host={host} dbname={dbname} user={user}")

    def create_symbols_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE symbols(
            id SERIAL PRIMARY KEY,
            symbol NVARCHAR(8),
            company TEXT,
            country TEXT)
        """).commit()

    def create_insiders_table(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE symbols(
            id SERIAL PRIMARY KEY,
            insider TEXT,
            position TEXT,
            transaction_date DATE,
            operation NVARCHAR(5),
            shares INT,
            shares_change FLOAT,
            trade_price FLOAT,
            cost FLOAT,
            total_cost FLOAT,
            yield_pcte FLOAT,
            p_e FLOAT,
            market_cap = FLOAT,
            symbol NVARCHAR(8) REFERENCES symbols (symbol))
        """).commit()

    def query_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM tables;
        """).commit()
