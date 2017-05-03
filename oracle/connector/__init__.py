from . import loadDLL
from .connections import Connection
from Oracle.ManagedDataAccess.Client import OracleConnection 
import logging

logging.basicConfig(level=logging.DEBUG)

def connect(host, user, password, servername, port=1521):
    '''
    get the oracle connection, return a connection without trans
    '''
    conn = OracleConnection()
    conn.ConnectionString = '''Data Source=(
        DESCRIPTION=(
            ADDRESS=(
                PROTOCOL=TCP
            )
            (HOST={host})
            (PORT={port})
        )
        (CONNECT_DATA=(
            SERVICE_NAME={servername}
        ))
    );Persist Security Info=True;User ID={user};Password={password};'''.format(
        host=host,
        user=user,
        password=password,
        port=port,
        servername=servername
    )
    conn.Open()
    return Connection(conn)