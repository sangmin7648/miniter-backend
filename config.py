db = {
    'user': 'admin',
    'password': 'iamthemaster!',
    'host': 'database-1.cydpwjfwzhkw.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"

JWT_SECRET_KEY = 'jwtsecret'

test_db = {
    'user': 'root',
    'password': '691103',
    'host': 'localhost',
    'port': 3306,
    'database': 'test_miniter'
}

test_config = {
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@"
              f"{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8"
}
