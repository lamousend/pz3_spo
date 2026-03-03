import mysql.connector

class SQLTable:
    def __init__(self, db_config, table_name):
        self.db_config = db_config
        self.table_name = table_name
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.columns = []

        if self._check_table_exists():
            self._update_column_names()

    def _check_table_exists(self):
        query = f"SHOW TABLES LIKE '{self.table_name}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def _update_column_names(self):
        query = f"SHOW COLUMNS FROM {self.table_name}"
        self.cursor.execute(query)
        self.columns = [row[0] for row in self.cursor.fetchall()]

                    # создание таблицы
    def create_table(self, columns):
        column_definition = ', '.join(f"`{name}` {type}" for name, type in columns.items())
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            {column_definition}
        )
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        finally:
            cursor.close()
        self._update_column_names()

                #insert
    def insert(self, data):
        columns = ', '.join(f"`{k}`" for k in data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO `{self.table_name}` ({columns}) VALUES ({values})"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
        finally:
            cursor.close()

                #select
    def select(self):
        cursor = self.connection.cursor()
        try:
            query = f'SELECT * FROM `{self.table_name}`'
            cursor.execute(query)
            films = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            # сделаем вывод в консоль для наглядности
            result = []
            for row in films:
                row_dict = dict(zip(col_names, row))
                result.append(row_dict)
                print(row_dict)
        finally:
            cursor.close()

            # добавление столбцов + проверка на существование
    def add_column(self, column_name, data_type):
            if column_name in self.columns:
                print(f'column `{column_name}` already exist in table')
                return
            query = f'ALTER TABLE `{self.table_name}` ADD COLUMN `{column_name}` {data_type}'
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                self.connection.commit()
            finally:
                cursor.close()
            print(f"Column `{column_name}` of type '{data_type}' added to table '{self.table_name}'.")
            self._update_column_names()

            # update
    def update(self, data, where):
        set_part = ', '.join(f"`{k}`=%s" for k in data)
        where_part = ' AND '.join(f"`{k}`=%s" for k in where)

        query = f"""
        UPDATE `{self.table_name}`
        SET {set_part}
        WHERE {where_part}
        """

        params = tuple(data.values()) + tuple(where.values())
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
        finally:
            cursor.close()

                # delete
    def delete(self, where):
        where_part = ' AND '.join(f"`{k}`=%s" for k in where)
        query = f"DELETE FROM `{self.table_name}` WHERE {where_part}"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(where.values()))
            self.connection.commit()
        finally:
            cursor.close()
                # использование

films_table = SQLTable(db_config, 'films')
films_table.create_table(columns= {
    'title': 'VARCHAR(255)',
    'age limit': 'INT'
})
films_table.add_column('genre', 'VARCHAR(255)')
films_table.add_column('film_score', 'INT')

films_table.insert({
    'title': 'Game of Thrones',
    'age limit': 18,
    'genre': 'fantasy',
    'film_score': 9
})

films_table.select()

films_table.update(
    data={
        'film_score': 10,
        'genre': 'epic fatasy'
    },
    where={
        'title': 'Game of Thrones'
    }
)

films_table.delete({
    'title': 'Game of Thrones'
})
