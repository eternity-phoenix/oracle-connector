from enum import Enum, unique
import warnings
from . import err
import logging

from Oracle.ManagedDataAccess.Client import OracleConnection, OracleCommand 

class Cursor(object):
    """
    This is the object you use to interact with the database.
    """

    _defer_warnings = True
    _logging_sql = True

    def __init__(self, connection):
        """
        Do not create an instance of a Cursor yourself. Call by
        connection.cursor().
        """
        self.connection = connection
        self._description = None
        self.rownumber = 0
        self._rowcount = -1
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows = None
        self._warnings_handled = False
    
    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()
    
    def _check_executed(self):
        if not self._executed:
            raise err.ProgrammingError("execute() first")
        
    def setinputsizes(self, *args):
        """Do nothing, required by DB API."""

    def setoutputsizes(self, *args):
        """Do nothing, required by DB API."""
    
    def close(self):
        """
        Closing a cursor just exhausts all remaining data.
        """
        self.connection = None
        
    def _get_connection(self):
        if not self.connection:
            raise err.ProgrammingError("Cursor closed")
        return self.connection

    
    @property
    def description(self):
        return self._description
    
    @property
    def rowcount(self):
        return self._rowcount

    def callproc(self):
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
    
    def execute(self, sql, *args):
        """Execute a query

        :param str query: Query to execute.

        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        query = self.mogrify(sql, args)

        result = self._query(query)
        self._executed = query
        return result
    
    def mogrify(self, query, args=None):
        """
        Returns the exact string
        """
        conn = self._get_connection()
        if args is not None:
            query = query % self._escape_args(args)

        return query
    
    def _escape_args(self, args):
        if isinstance(args, (tuple, list)):
            return tuple("'" + arg + "'" for arg in args)
        elif isinstance(args, dict):
            return dict((key, "'" + val + "'") for (key, val) in args.items())
        else:
            return "'" + args + "'"
    
    def _query(self, q):
        if self._logging_sql:
            logging.info(q)
        conn = self._get_connection()
        self._last_executed = q
        odr = conn.query(q)
        self._do_get_result(odr)
        return self.rowcount

    def _do_get_result(self, odr):

        self.rownumber = 0
        self._result = result = odr
        self._rowcount = result.FetchSize
        #self._description = result.description
        #self.lastrowid = result.insert_id
        #self._rows = result.rows

        self._warnings_handled = False

        if not self._defer_warnings:
            self._show_warnings()

    def _show_warnings(self):
        if self._warnings_handled:
            return
        self._warnings_handled = True
        if self._result and (self._result.has_next or not self._result.warning_count):
            return
        ws = self._get_connection().show_warnings()
        if ws is None:
            return
        for w in ws:
            msg = w[-1]
            warnings.warn(err.Warning(*w[1:3]), stacklevel=4)

    def __iter__(self):
        return iter(self.fetchone, None)