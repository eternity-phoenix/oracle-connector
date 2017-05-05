# python -m oracle.test
import unittest
from ..connector import connect

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = connect('192.168.1.101', 'cacdms', 'cdms', 'cdms')
    
    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    ##初始化工作  
    def setUp(self):  
        self.cursor = self.conn.cursor()
      
    #退出清理工作  
    def tearDown(self):  
        self.cursor.close()
    
    def test_fetchone(self):
        self.cursor.execute('select 1 from dual')
        print(self.cursor.fetchone())
        print(self.cursor.rowcount)
    
    def test_fetchall(self):
        self.cursor.execute('select %s from dual union all select 123 from dual', (1,))
        print(self.cursor.fetchall(dict_=True))
        print(self.cursor.rowcount)
    
    def test_fetchmany(self):
        self.cursor.execute("select %(num)s, %(num)s, 'TEST' XX from dual", {'num': 1})
        print(self.cursor.fetchmany(dict_=True))
        print(self.cursor.rowcount)
    
    def test_insert(self):
        self.cursor.execute("insert into T (barcode, ver) values (%s, %s)", ('1234', '45678')) # do not mistake the column's type
        print(self.cursor.fetchmany(dict_=True))
        print(self.cursor.rowcount)
    
    def test_fetch_with_star(self):
        self.cursor.execute("select T.*, '中文' CN from T")
        print(self.cursor.fetchall(dict_=True))
        print(self.cursor.rowcount)
    
    def test_delete(self):
        self.cursor.execute('delete from T where barcode=%s', ('1234',))
        print(self.cursor.fetchall(dict_=True))
        print(self.cursor.rowcount)
    
    def test_create_table(self):
        self.cursor.execute('create table TT ( T VARCHAR2(50) NULL)')
        print(self.cursor.fetchall(dict_=True))
        print(self.cursor.rowcount)
    
    def test_drop_table(self):
        self.cursor.execute('drop table TT')
        print(self.cursor.fetchall(dict_=True))
        print(self.cursor.rowcount)
    
    def test_transaction_rollback(self):
        self.conn.create_transaction()
        self.cursor.execute("insert into T (barcode, ver) values('trans', 'trans')")
        self.conn.rollback()
        
        self.cursor.execute("select * from T where barcode='trans'")
        print(self.cursor.fetchall())

    def test_transaction_commit(self):
        self.conn.create_transaction()
        self.cursor.execute("insert into T (barcode, ver) values('trans', 'trans')")
        self.conn.commit()
        
        self.cursor.execute("select * from T where barcode='trans'")
        print(self.cursor.fetchall())

        self.cursor.execute("delete from T where barcode='trans'")

if __name__ == '__main__':
    unittest.main()