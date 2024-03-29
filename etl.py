import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Run queries that load staging tables into database
    ----------
    cur: cursor to database\n
    conn: connection to database
    Returns
    -------
    None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Run queries that take data from staging tables and inserts them into
    tables in star schema
    Parameters
    ----------
    cur: cursor to database\n
    conn: connection to database
    Returns
    -------
    None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function that executes process of loading data into staging tables
    and then into tables in star schema
    Parameters
    ----------
    cur: cursor to database\n
    conn: connection to database
    Returns
    -------
    None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}"
        .format(*config['CLUSTER'].values())
    )
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
