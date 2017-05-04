'''
the sql formatters
'''
from collections import OrderedDict
import re

class SQLFormat(object):
    
    def __init__(self, sql, args):
        self.__sql, self.__args = sql, args
        self._format()

    @property
    def sql(self):
        return self._sql
    
    @property
    def args(self):
        return self._args

    def _format(self):
        if self.__args is None:
            self._sql, self._args = self.__sql, OrderedDict()
            return
        try:
            rsql = ""
            rargs = OrderedDict()
            if isinstance(self.__args, (list, tuple)):
                l = self.__sql.split('%s')
                pars = [':par' + str(i) for i in range(len(l)-1)]
                for i in range(len(pars)):
                    rsql += l[i] + pars[i]
                    rargs[':par' + str(i)] = self.__args[i]
                rsql += l[-1]
            elif isinstance(self.__args, dict):
                rsql = self.__sql
                iters = re.finditer(r'%\(.*?\)s', self.__sql)
                for i in iters:
                    par = self.__sql[slice(*i.span())]
                    rsql = rsql.replace(par, ':' + par[2:-2])
                    rargs[':' + par[2:-2]] = self.__args[par[2:-2]]

            self._sql, self._args = rsql, rargs
        except KeyError as e:
            raise KeyError('missing kwargs: ' + str(e.args)) from e
