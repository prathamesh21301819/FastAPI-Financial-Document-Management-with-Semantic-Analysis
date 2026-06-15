from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL = "postgresql://postgres:patil123@localhost:2130/financedb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker (bind=engine)
Base = declarative_base()
try:
    connection = engine.connect()
    print("✅ Database Connected Successfully!")
    connection.close()
except Exception as e:
    print("❌ Connection Failed")
    print(e)