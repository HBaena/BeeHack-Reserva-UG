from psycopg2 import sql
from typing import Any, Callable
import logging
from icecream import ic
logging.basicConfig(filename='model.log', level=logging.ERROR)

class Model:
    def __init__(self, pool):
        self.pool = pool


    def execute(self, query: str, data: Any=None, commit: bool=False, 
                formatting: Callable=lambda response: response ) -> Any:
        """
        Function: execute(self, query: sql.SQL, data: Any(tuple, dict)) -> Any
        Summary: Execute an sql query mannaging exceptions and pool connections
        Examples: execute("DELETE * FROM %s", (data, ))
        Attributes: 
            @param (query): query to execute
            @param (data): data to insert in execution  
        Returns: Tuple if execution result without errors or a false if a exception was raised
        """
        try:
            connection = self.pool.get_connection()  # Get a connection from the pool
            connection.autocommit = commit  # set 
            cursor = connection.cursor()
            if data: 
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            try:
                response = cursor.fetchall()
                response = formatting(response)
            except Exception as e:
                ic(e)
                response = True
            self.pool.release_connection(connection)
            return  response
        except Exception as e:
            logging.error(str(e))
            ic(str(e))
            self.pool.release_connection(connection)
            return False


    def get_image_base64(self, data: dict) -> str:
        """
        Function: get_image
        Summary: Return an image in base 64 from databe
        Examples: get_image("rf_foto", 'miros."miroscn"', "user_id='hbaena'")
        Attributes: 
            @param (column_name:str): column name in table
            @param (table_name:str): table name (with schema name)
            @param (where_statment:str): statement to difference
        Returns: image in base 64
        """
        query = """
                    SELECT encode( "%(field)s", 'base64') AS %(field)s
                    FROM %(table)s
                    WHERE %(where)s
                """ % data
        return response[0][0] if (response := self.execute(query)) else None


    def get_image_bloob(self, data: dict) -> str:
        """
        Function: get_image_bloob
        Summary: Return an image in base 64 from databe
        Examples: get_image("rf_foto", 'miros."miroscn"', "user_id='hbaena'")
        Attributes: 
            @param (column_name:str): column name in table
            @param (table_name:str): table name (with schema name)
            @param (where_statment:str): statement to difference
        Returns: image in base 64
        """
        query = """
                    SELECT %(field)s
                    FROM %(table)s
                    WHERE %(where)s
                """ % data
        return response if (response := self.execute(query)) else None

