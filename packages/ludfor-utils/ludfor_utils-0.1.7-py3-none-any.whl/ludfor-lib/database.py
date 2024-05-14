import psycopg2
from psycopg2.extras import execute_batch
from typing import List, Tuple

class Database():
    """
    Módulo que contem funções de banco de dados usadas com recorrência.
    
    :pararm dbname str
    :param host str
    :param port str
    :param user str
    :param password str
    """
    def __init__(self, dbname: str, host: str, port: str, user: str, password: str):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self._conn = self._open_connection()
        self._cursor = self._conn.cursor()
    
    def _open_connection(self):
        return psycopg2.connect(
                            dbname = self.dbname,
                            host = self.host,
                            port = self.port,
                            user = self.user,
                            password = self.password
                            )

    def data_query(self, statement: str):
        """
        Função para execução de consultas.

        eg: SELECT * FROM table;
        """
        try:
            self._cursor.execute(statement)
            return self._cursor
        except Exception as e:
            raise Exception(e)
    
    def data_manipulation(self, statement: str):
        """
        Função para queries de manipulação de dados em banco.

        eg: INSERT INTO table (column) VALUE (val);
        """
        try:
            self._cursor.execute(statement)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def data_manipulation_with_return(self, statement: str):
        """
        Função para queries de manipulação de dados em banco com retorno.

        eg: INSERT INTO table (column) VALUE (val) RETURNING id;
        """
        try:
            self._cursor.execute(statement)
            self._conn.commit()
            return self._cursor
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def data_manipulation_in_batches(self, statement: str, values: List[Tuple]):
        """
        Função para queries de manipulação de dados em banco por lotes.

        eg: INSERT INTO table (column1, column2) VALUE (%s, %s);
        values: [(val1, val2), (val3, val4)]
        """
        try:
            execute_batch(self._cursor, statement, values)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def close_conn(self):
        self._conn.close()


