import sqlite3


class IntoLite:

    def __init__(self, db_file=None):
        if not db_file:
            db_file = get_data_path()
        self.conn = self.create_connection(db_file)

    def create_connection(self, db_file):
        """Creates a database connection to the SQLite db
            Args:
                db_file: str, path to file
            Returns:
                connection or None
        """
        try:
            return sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(str(e))
        return None

    def execute_sql_str(self, sql_str, return_obj=False):
        """Creates a table from the SQL statment
            Args:
                *self.connection to db
                sql_str: str, SQL statment
                return_obj: bool, returns cursor object
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql_str)
            if return_obj:
                return cur
        except sqlite3.Error as e:
            print(str(e))

    def execute_insert(self, table_name, values):
        cols_cur = self.execute_sql_str(f'SELECT * FROM {table_name}',
                                        return_obj=True)
        columns = [des[0] for des in cols_cur.description]

        interrogants = '?, '*len(columns)
        interrogants = interrogants.strip(', ')

        sql_str = ''' INSERT OR IGNORE INTO %s (%s)
        VALUES (%s)''' % (table_name,
                          ', '.join(columns),
                          interrogants)
        # print(sql_str)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql_str, values)
            return cur.lastrowid

    def create_symbols_table(self):
        self.execute_sql_str("""
            CREATE TABLE IF NOT EXISTS symbols(
            symbol TEXT PRIMARY KEY,
            company TEXT,
            country TEXT);
        """)

    def create_insiders_table(self):
        self.execute_sql_str("""
            CREATE TABLE IF NOT EXISTS insiders(
            symbol TEXT NOT NULL,
            insider TEXT,
            position TEXT,
            transaction_date TEXT,
            operation TEXT,
            shares INTEGER,
            shares_change REAL,
            trade_price REAL,
            cost REAL,
            total_cost REAL,
            yield_pcte REAL,
            p_e REAL,
            market_cap REAL,
            FOREIGN KEY (symbol) REFERENCES symbols (symbol));
        """)


def get_data_path():
    from pathlib import Path
    return str(Path(__file__).resolve().parent.parent) \
        + r'\data\insiders.db'


def main():
    table = 'symbols'
    values = ('APPLE', 'Apple Inc.', 'EEUU')
    data = get_data_path()
    print(data)

    a = IntoLite()

    # a.execute_sql_str("DROP TABLE IF EXISTS symbols")
    # a.execute_sql_str("DROP TABLE IF EXISTS insiders")
    # print('deleted')
    #
    # a.create_symbols_table()
    # a.create_insiders_table()

    # print('Printing tables in db: ')
    # cur = a.execute_sql_str("SELECT name FROM sqlite_master WHERE type='table';",
    #                         return_obj=True)
    # print(cur.fetchall())
    #
    # print('Insert values: ', values, ' :')
    # a.execute_insert(table, values)
    print(a.execute_sql_str('SELECT * FROM symbols', return_obj=True).fetchall())


if __name__ == '__main__':
    main()
