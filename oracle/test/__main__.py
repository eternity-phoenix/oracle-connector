# python -m oracle.test
from ..connector import connect

conn = connect('192.168.184.134', 'cdms', 'cdms', 'ORCL')

cur = conn.cursor()

rowcount = cur.execute('select 1 from dual')
print(rowcount)

print(cur._result.FieldCount)