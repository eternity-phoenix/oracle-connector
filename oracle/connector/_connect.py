from enum import Enum, unique

class Curser(object):
    def __init__(self, conn):
        self.__conn = conn
    
    @property
    def description(self):
        '''
        '''
    
    @property
    def rowcount(self):
        '''
        '''

    def callproc(self):
        '''
        '''

    def close(self):
        '''
        '''

    def fetchone(self):
        '''
        '''

    def fetchmany(self):
        '''
        '''

    def fetchall(self):
        '''
        '''


@unique
class ConnectionState(Enum):
    closed = 0
    open = 1
    connecting = 2
    executing = 4
    fetching = 8
    broken = 16

class Connection(object):
    
    def __init__(self, conn):
        self.__conn = conn
        self.state = conn.State
    
    def close(self):
        self.__conn.close()
    
    def commit(self):
        self.__conn.commit()
    
    def rollback(self):
        self.__conn.rollback()
    
    def cursor(self):
        return Curser(self)