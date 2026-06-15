from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base

class User (Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique= True)
    password = Column(String)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer,primary_key=True,index = True)
    role_name = Column(String,unique=True)

class Userrole(Base):
    __tablename__ = "user_role"
    id = Column(Integer,primary_key = True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    role_id = Column(
        Integer,
        ForeignKey("roles.id")
    )
class Document(Base):
    __tablename__ = "documents"
    document_id = Column(Integer,primary_key= True,index = True )
    title = Column(String)
    company_name = Column(String)
    document_type = Column(String)
    uploaded_by = Column(Integer)
    file_path = Column(String)
    created_at = Column(String)