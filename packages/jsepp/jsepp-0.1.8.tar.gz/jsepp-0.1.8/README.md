## JSEPP
### dbutils
#### MySQLConn
1. __init__(host: str, user: str, password: str, db: str, port: int)
2. excute_one(comm)
3. excute_all(comm)
4. insert_confirm(comm)
5. insert(comm)
6. confirm()
7. rollback()
#### MongoConn
1. __init__(user:str, password:str, host:str, port:int, db:str)
2. fetch_one(tablename:str, filter: dict)
3. update_one(tablename:str, filter:dict, data:dict)
4. insert_one(tablename:str, data:dict)