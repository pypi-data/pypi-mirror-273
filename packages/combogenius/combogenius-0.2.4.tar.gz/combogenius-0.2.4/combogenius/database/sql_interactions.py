import sqlite3
import logging 
import pandas as pd
import numpy as np
import os
from ..logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class SqlHandler:
    """
    A class to handle SQLite database operations.

    Attributes:
        dbname (str): The name of the SQLite database.
        table_name (str): The name of the table within the database.
        cnxn (sqlite3.Connection): The SQLite database connection object.
        cursor (sqlite3.Cursor): The SQLite cursor object.
    """

    def __init__(self, dbname:str,table_name:str) -> None:
        """
        Initializes the SqlHandler class.

        Args:
            dbname (str): The name of the SQLite database.
            table_name (str): The name of the table within the database.
        """   
        
        self.cnxn=sqlite3.connect(f'{dbname}.db')
        self.cursor=self.cnxn.cursor()
        self.dbname=dbname
        self.table_name=table_name

    def close_cnxn(self)->None:
        """
        Closes the database connection.

        Returns:
            None
        """
        logger.info('commiting the changes')
        self.cursor.close()
        self.cnxn.close()
        logger.info('the connection has been closed')

    def get_table_columns(self)->list:
        """
        Retrieves the list of column names in the table.

        Returns:
            list: List of column names.
        """  

        self.cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = self.cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        logger.info(f'the list of columns: {column_names}')
        #self.cursor.close()

        return column_names
    
    def truncate_table(self)->None:
        """
        Truncates the table by dropping all rows.

        Returns:
            None
        """
        query=f"DROP TABLE IF EXISTS {self.table_name};"
        self.cursor.execute(query)
        logging.info(f'the {self.table_name} is truncated')
        #self.cursor.close()

    def drop_table(self):
        """
        Drops the entire table from the database.

        Returns:
            None
        """   
        query = f"DROP TABLE IF EXISTS {self.table_name};"
        logging.info(query)
        self.cursor.execute(query)
        self.cnxn.commit()
        logging.info(f"table '{self.table_name}' deleted.")
        logger.debug('using drop table function')

    def insert_many(self, df:pd.DataFrame) -> str:
        """
        Inserts multiple rows into the table from a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing the data to be inserted.

        Returns:
            str: Message indicating the status of the operation.
        """      
        try:
            chunksize = 1000  # Adjust as needed
            total_rows = df.shape[0]
            num_chunks = (total_rows + chunksize - 1) // chunksize  # Ceiling division to get the number of chunks

            for i in range(num_chunks):
                start_idx = i * chunksize
                end_idx = min((i + 1) * chunksize, total_rows)
                chunk_df = df.iloc[start_idx:end_idx]

                chunk_df = chunk_df.replace(np.nan, None) # for handling NULLS
                chunk_df.rename(columns=lambda x: x.lower(), inplace=True)
                columns = list(chunk_df.columns)
                logger.info(f'BEFORE the column intersection: {columns}')
                sql_column_names = [i.lower() for i in self.get_table_columns()]
                columns = list(set(columns) & set(sql_column_names))
                logger.info(f'AFTER the column intersection: {columns}')
                ncolumns = list(len(columns) * '?')
                data_to_insert = chunk_df.loc[:, columns]

                values = [tuple(i) for i in data_to_insert.values]
                logger.info(f'the shape of the table which is going to be imported {data_to_insert.shape}')
                if len(columns) > 1:
                    cols, params = ', '.join(columns), ', '.join(ncolumns)
                else:
                    cols, params = columns[0], ncolumns[0]

                logger.info(f'insert structure: colnames: {cols} params: {params}')
                logger.info(values[0])
                query = f"""INSERT INTO  {self.table_name} ({cols}) VALUES ({params});"""

                logger.info(f'QUERY: {query}')

                self.cursor.executemany(query, values)
                try:
                    for i in self.cursor.messages:
                        logger.info(i)
                except:
                    pass

            self.cnxn.commit()
            logger.warning('the data is loaded')
        except sqlite3.IntegrityError as e:
            logger.error(f"An IntegrityError occurred: {e}")
            self.cnxn.rollback()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.cnxn.rollback()

    def update_table(dbname, table_name, set_values, condition):
        """
        Update records in the specified table based on the provided condition.

        Args:
        dbname (str): The database name.
        table_name (str): The table to update.
        set_values (dict): A dictionary where keys are column names and values are the new data for these columns.
        condition (str): A SQL condition string for the WHERE clause.

        Returns:
        None
        """
        # Connect to the SQLite database
        connection = sqlite3.connect(f'{dbname}.db')
        cursor = connection.cursor()
        
        # Prepare the SET part of the SQL update statement
        set_clause = ', '.join([f"{key} = ?" for key in set_values.keys()])
        values = list(set_values.values())
        
        # Prepare the SQL update query
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        try:
            cursor.execute(query, values)
            connection.commit()
            logger.info(f"Rows updated: {cursor.rowcount}")
        except sqlite3.Error as e:
            logger.error(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
            logger.info("Database connection closed.")
