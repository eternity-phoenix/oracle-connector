import re
import logging
import warnings
from collections import OrderedDict
from Oracle.ManagedDataAccess.Client import OracleConnection, OracleCommand 
from . import err
from . import convert
from . import formatter


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
        self.init()

    def init(self):
        self._description = None
        self.currownumber = 0
        self._rowcount = -1
        self._executed = None
        self._result = None
        self._comm = None
        self._rows = []
        self._warnings_handled = False

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def _check_closed(self):
        if self.connection is None:
            raise err.OperationalError('the connection has been closed')

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
        self.init()

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

    def __fetchnext(self):
        '''
        do not use this method, it's called by other's methods
        '''
        return self._result.Read()

    def __read_one_record(self):
        self.currownumber += 1
        d = OrderedDict()
        for i in range(self._result.VisibleFieldCount):
            name = self._result.GetName(i)
            while d.get(name, None) is not None:
                name += str(1)
            d[name] = convert.convert(self._result[i])# 格式转换
        self._rows.append(d)
        return d

    def fetchone(self, dict_=False):
        """Fetch the next row"""
        self._check_executed()
        if not self.__fetchnext():
            return None

        return self.__read_one_record() if dict_ else tuple(self.__read_one_record().values())

    def fetchmany(self, size=None, dict_=False):
        """Fetch the size row"""
        self._check_executed()
        if size is None:
            return self.fetchall(dict_)
        else:
            dl = []
            for i in range(size):
                if self.__fetchnext():
                    dl.append(self.__read_one_record())
            return dl if dict_ else [tuple(r.values()) for r in dl]

    def fetchall(self, dict_=False):
        """Fetch the all row"""
        self._check_executed()
        dl = []
        while self.__fetchnext():
            dl.append(self.__read_one_record())
        return dl if dict_ else [tuple(r.values()) for r in dl]

    def execute(self, sql, args=None):
        """Execute a query

        :param str query: Query to execute.

        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        self.init()
        self._check_closed()
        sqlformat = formatter.SQLFormat(sql, args)
        result = self._query(sqlformat)
        self._executed = sqlformat.sql
        return result

    def _query(self, sqlformat):
        if self._logging_sql:
            logging.info(sqlformat.sql)
        conn = self._get_connection()
        self._comm = conn._query(sqlformat)

        self._do_get_result(self._comm.ExecuteReader())
        return self.rowcount

    def _do_get_result(self, odr):

        self.rownumber = 0
        self._result = result = odr
        self._rowcount = result.RecordsAffected
        #self._description = result.description
        # self.lastrowid = result.insert_id
        # self._rows = self._init_rows(result)

        self._warnings_handled = False

        if not self._defer_warnings:
            pass
            # self._show_warnings()

    def _show_warnings(self):
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