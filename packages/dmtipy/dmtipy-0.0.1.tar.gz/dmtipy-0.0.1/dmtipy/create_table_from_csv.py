import pandas as pd
import pymssql
import os
from io import StringIO
from datetime import datetime
from sqlalchemy import create_engine

class create_sql_table_from_csv:
    """
    Initiate to create table based on your dataframe especially for csv file and SQL Server Database System
    
    :param df: Your dataframe from pandas.
    :type df: dataframe

    :param table_name: Your table_name at your server destination.
    :type table_name: string

    :param server: Your sql server destination server.
    :type server: string

    :param database: Your database name at your destination server.
    :type database: string

    :param username: Your username at your database destination.
    :type username: string

    :param password: Your password at your database destination.
    :type password: string
    """
    @staticmethod

    def create_sql_table_from_csv(df, table_name, server, database, username, password):
        connection = pymssql.connect(server=server, database=database, user=username, password=password)
        cursor = connection.cursor()

        column_type = []
        for col in df.columns:
            if df[col].dtypes == "int64":
                column_type.append(f"{str(col)} NVARCHAR(MAX)")

            if df[col].dtypes == "object":
                column_type.append(f"{str(col)} NVARCHAR(MAX)")

            if df[col].dtypes == "float64":
                column_type.append(f"{str(col)} FLOAT")

            if df[col].dtypes == "datetime64[ns]":
                column_type.append(f"{str(col)} NVARCHAR(MAX)")
        # Define the CREATE TABLE statement based on the DataFrame columns and data types

        if len(column_type) == 1:
            create_table_sql = f"""CREATE TABLE {table_name} ({column_type[0]});"""
        else:
            create_table_sql = f"""CREATE TABLE {table_name}({",".join(column_type)})"""

        # create_table_sql = f"CREATE TABLE {table_name} ({', '.join([f'{col} NVARCHAR(MAX)' for col in df.columns])});"

        cursor.execute(create_table_sql)
        connection.commit()
        connection.close()

