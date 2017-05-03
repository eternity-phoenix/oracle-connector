from . import loadDLL
from Oracle.ManagedDataAccess.Client import OracleConnection

def connect(host, user, password, servername, charset='utf-8', port=1521):
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
        charset=charset,
        port=port,
        servername=servername
    )
    conn.Open()
    return conn