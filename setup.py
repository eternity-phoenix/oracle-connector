from setuptools import setup, find_packages

setup(
    name='oracle-connector',
    version='0.1.0',
    packages=find_packages(),
    description="Oracle Connector Without Client",
    author="Etern",
    author_email='769518953@qq.com',
    url="https://github.com/eternity-phoenix/oracle-connector",
    license="LGPL",
    keywords=('oracle', 'Connector', 'Without Client', 'CLR'),
    install_requires=['pythonnet'],
    #include_package_data=True,
    package_data={
        'oracle.connector': ['Oracle.ManagedDataAccess/*']
    }
)