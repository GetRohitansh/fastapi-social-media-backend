from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings

# SQL_ALCHEMY_URL = 'postgresql://<username>:<password>@(<ip-address>/hostname):port_number/<database_name'
# SQL_ALCHEMY_URL = 'postgresql://postgres:password123@localhost:5432/fastapi'
SQL_ALCHEMY_URL = f'postgresql://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DATABASE_HOSTNAME}:{Settings.DATABASE_PORT}/{Settings.DATABASE_NAME}'

engine = create_engine(SQL_ALCHEMY_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
# Whenever we get request through API we get connection/session to database which is close after request is compeleted
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()





# SQL driver which is used to setup connection
# but this is now done using sqlalchemy
'''
import psycopg2 # for database
from psycopg2.extras import RealDictCursor # to get column name along with data (like dictionary)
import time

while True: # To reconnect database after connection is failed
    try:
        # connecting to database
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor() # used to execute SQL queries
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
'''