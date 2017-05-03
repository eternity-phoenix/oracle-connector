'''
load the Oracle.ManagedDataAccess assembly
'''
import os
import clr
cwd = os.path.abspath(os.path.dirname(__file__))
clr.AddReference(
    os.path.join(
        os.path.join(cwd, 'Oracle.ManagedDataAccess'), 'Oracle.ManagedDataAccess.dll'))
