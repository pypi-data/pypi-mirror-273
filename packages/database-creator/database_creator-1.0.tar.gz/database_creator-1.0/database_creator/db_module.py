import sqlite3

class Database:
    def __init__(self, title: str = "base") -> None:
        self.db = sqlite3.connect(f"{title}.db", check_same_thread = False)
        self.cursor = self.db.cursor()

    class Info:
        def getTables(database: object) -> list:
            "Return list with info about of tables in database"

            database.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table'")

            list = []
            for i in database.cursor.fetchall():
                list.append(i[2])

            return list
        
        def getColumns(database: object, table: str) -> list:
            "Return list with info about of columns in table"

            database.cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table}')")

            list = []
            for i in database.cursor.fetchall():
                list.append(i[0])

            return list

    class Table:
        def create(database: object, table: str, columns: list, types: list) -> None:
            "create table in database"
            str = ""

            for i in range(len(columns)):
                str += columns[i] + " " + types[i]
                str += "," if i != len(columns) - 1 else ""

            database.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({str})")
            database.db.commit()

        def drop(database: object, table: str) -> None:
            "Delete table in database"

            database.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            database.db.commit()

        def write(database: object, table: str, *args) -> None:
            "Set a write in database"

            def get_id_key(database: object, tableName: str):
                return f"{len(database.Table.get(database, tableName)) + 1},"
            
            string = get_id_key(database, table) if len(args) != len(database.Info.getColumns(database, table)) else ""

            for i in range(len(args)):
                string += f"'{args[i]}'"
                string += ", " if i != len(args) - 1 else ""

            database.cursor.execute(f"INSERT INTO {table} VALUES ({string})")
            database.db.commit()

        def get(database: object, table: str, columns: list = "*", request: str = None, fetchone: bool = False) -> list:
            "Return data in table with request sorting"

            database.cursor.execute(f"SELECT {columns} FROM {table} {request}")

            return database.cursor.fetchone() if fetchone else database.cursor.fetchall()

        def delete(database: object, table: str, request: str) -> None:
            "Delete data in table with request sorting"

            database.cursor.execute(f"DELETE FROM {table} Where {request}")
            database.db.commit()