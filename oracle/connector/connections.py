from enum import Enum, unique
import warnings
from . import err
from .cursors import Cursor
import logging

from Oracle.ManagedDataAccess.Client import OracleConnection, OracleCommand 
import System


@unique
class ConnectionState(Enum):
    '''
    connection states enum
    '''
    closed = 0
    open = 1
    connecting = 2
    executing = 4
    fetching = 8
    broken = 16

class Connection(object):
    '''
    the connection class, with no trans
    '''
    def __init__(self, conn):
        self.__conn = conn
        self.trans = None
    
    @property
    def state(self):
        return ConnectionState(self.__conn.State)
    
    def close(self):
        '''
        close the connection
        '''
        if not self.state is ConnectionState.closed:
            self.__conn.Close()
    
    @property
    def connectString(self):
        return self.__conn.ConnectionString
    
    def cursor(self):
        '''
        get the cursor
        '''
        return Cursor(self)
    
    def query(self, q):
        comm = OracleCommand(q, self.__conn)
        return comm.ExecuteReader()
    
    def create_transaction(self, isolation_level=System.Data.IsolationLevel.ReadCommitted):
        '''
        get a OracleTransactionConnection instance
        '''
        self.trans = self.__conn.BeginTransaction(isolation_level)
    
    def commit(self):
        if not self.in_transaction:
            raise err.OperationalError('the trans is not opened')
        self.trans.Commit()
        self.trans = None

    def rollback(self):
        if not self.in_transaction:
            raise err.OperationalError('the trans is not opened')
        self.trans.Rollback()
        self.trans = None
    
    @property
    def isolation_level(self):
        if not self.in_transaction:
            return None
        return self.trans._isolation_level
    
    @property
    def in_transaction(self):
        return bool(self.trans)

