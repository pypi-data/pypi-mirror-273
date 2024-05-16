import os
import math
import warnings
import numpy as np
import pandas as pd
from tqdm import tqdm
from impala.dbapi import connect
from impala.util import as_pandas

DEBUG = False
if DEBUG:
    print("DB tools are loaded!")


def prepare_connection(host: str):
    """Prepare connection to IDP (Hadoop) in CDSW

    Author:
        Colin Li @ 2023-05

    Args:
        host (str): "impala" or "hive"

    Returns:
        impala.dbapi.connect: connection to IDP
    """
    CONN = None
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            if host == "impala":
                CONN = connect(
                    host=os.getenv("IMPALA_HOST"),
                    port=os.getenv("IMPALA_PORT"),
                    database="default",
                    use_ssl=True,
                    ca_cert=None,
                    auth_mechanism="GSSAPI",
                    user="impala",
                    password="",
                    kerberos_service_name="impala",
                )
            elif host == "hive":
                CONN = connect(
                    host=os.getenv("HIVE_HOST"),
                    port=os.getenv("HIVE_PORT"),
                    database="default",
                    use_ssl=True,
                    ca_cert=None,
                    auth_mechanism="GSSAPI",
                    user="hive",
                    password="",
                    kerberos_service_name="hive",
                )
    except TypeError:
        warnings.warn("Update password for Hadoop Authentication in CDSW!")
        warnings.warn("Run this in CDSW ONLY!")
        return None
    return CONN


def execute_db_query(conn, query: str):
    """Execute databass query

    Author:
        Colin Li @ 2023-05

    Args:
        conn (impala.dbapi.connect): connection
        query (str): can be either a string (query) or file path of a sql file
    """
    if os.path.isfile(query) and query[-4:] == ".sql":
        query_path = query
        with open(query_path, "r") as f:
            query = f.read()
        print(f"Executing task {query_path}")
    tasks = query.split(";")
    for i, t in enumerate(tasks):
        if t.replace(" ", "").replace("\n", "") == "":
            continue
        else:
            print(f"Executing subtask {i+1}")
            cursor = conn.cursor()
            cursor.execute(t)
    print(f"Task is completed!")


def extract_db_data(conn, query: str):
    """Extract data from database as pandas dataframe

    Author:
        Colin Li @ 2023-05

    Args:
        conn (impala.dbapi.connect): connection
        query (str): can be either a string (query) or file path of a sql file

    Returns:
        pandas.DataFrame: Pandas dataframe containing database data
    """
    if os.path.isfile(query) and query[-4:] == ".sql":
        query_path = query
        with open(query_path, "r") as f:
            query = f.read()
        print(f"Executing task {query_path}")
    cursor = conn.cursor()
    cursor.execute(query)
    df = as_pandas(cursor)
    return df


def generate_sql_row(row):
    """Generate one sql row used in sql insert statement
    Author:
        Colin Li @ 2023-02
    Args:
        row (pd.Series): pandas data series
    Returns:
        str: one sql row used in sql insert statement
    """
    tb_row_s0 = row.tolist()
    for i, c in enumerate(tb_row_s0):
        if isinstance(c, str):
            tb_row_s0[i] = '"' + str(c) + '"'
        elif isinstance(c, (int, np.integer)):
            tb_row_s0[i] = str(c)
        elif isinstance(c, (float, np.float32)):
            if math.isnan(c):
                tb_row_s0[i] = "NULL"
            else:
                tb_row_s0[i] = str(c)[:10]
        elif pd.isnull(c) or c is None:
            tb_row_s0[i] = "NULL"
        else:
            tb_row_s0[i] = '"' + str(c) + '"'
    tb_row_s1 = "(" + ",".join(tb_row_s0) + ")"
    return tb_row_s1


def insert_one_row(row, conn, db_table_name):
    """Insert one row into hadoop table
    Author:
        Colin Li @ 2023-02
    Args:
        row (_type_): _description_
        conn (_type_): _description_
        db_table_name (_type_): _description_
    """
    with conn.cursor() as cursor:
        t = (
            f"""
        INSERT INTO {db_table_name}
        VALUES
        """
            + row
        )
        cursor.execute(t)


def insert_rows_to_table(tasks_insert: list, conn, db_table_name, nrow_per_insert=20):
    """Insert rows to hadoop table

    Author:
        Colin Li @ 2023-02

    Args:
        tasks_insert (list): list of strings which is the output from
            function generate_sql_row
        conn (impala.hiveserver2.HiveServer2Connection):
            connetion to hive/impala
        db_table_name (str): database and tablename joined by dot '.'
        nrow_per_insert (int, optional): Number of rows per insert.
            Defaults to 20.
    """
    tasks_size = len(tasks_insert)
    print(f"Rows to insert: {tasks_size}")
    n, rem = divmod(tasks_size, nrow_per_insert)
    st = 0
    tqdm._instances.clear()
    if n > 0:
        for i in tqdm(range(n)):
            rows = tasks_insert[st : st + nrow_per_insert]
            if len(rows) > 1:
                insert_one_row(",".join(rows), conn, db_table_name)
            else:
                insert_one_row(rows[0], conn, db_table_name)
            st += nrow_per_insert
    if rem != 0:
        rows = tasks_insert[st:tasks_size]
        if len(rows) > 1:
            insert_one_row(",".join(rows), conn, db_table_name)
        else:
            insert_one_row(rows[0], conn, db_table_name)


def insert_df_to_table(df, conn, db_table_name, nrow_per_insert=20):
    """Insert pandas dataframe rows into hadoop table
    Author:
        Colin Li @ 2024-05
    Args:
        df (pandas.DataFrame): pandas dataframe
        conn (impala.hiveserver2.HiveServer2Connection):
            connetion to hive/impala
        db_table_name (str): database and tablename joined by dot '.'
        nrow_per_insert (int, optional): Number of rows per insert.
            Defaults to 20.
    """
    tasks_insert = df.apply(generate_sql_row, axis=1).tolist()
    insert_rows_to_table(
        tasks_insert,
        conn=conn,
        db_table_name=db_table_name,
        nrow_per_insert=nrow_per_insert,
    )


if __name__ == "__main__":
    pass
