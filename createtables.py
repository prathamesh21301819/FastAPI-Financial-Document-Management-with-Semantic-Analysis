from database import engine,Base
from models  import User,Role,Userrole,Document
Base.metadata.create_all(bind = engine)
print("Tables Created")