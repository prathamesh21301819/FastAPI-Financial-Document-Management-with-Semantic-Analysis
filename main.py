from fastapi import FastAPI
from database import SessionLocal
from models  import User, Role,UserRole
from auth  import hashing_password
from auth import(
    verifying_password,
    create_access_tokens
)
app =FastAPI()
from fastapi import UploadFile,File
import shutil
from datetime import datetime
from models import Document
from rag.pdfparser import extract_text
from rag.chunk import create_chunks
from rag.embeddings import create_embeddings
from rag.qdrant import store_vectors
from rag.embeddings import model
from rag.qdrant import client
from rag.qdrant import search_vectors
from rag.reranker import rerank
@app.post("/auth/register")
def register(name:str,email:str,password:str):
    db = SessionLocal()
    user = User(
        name = name,
        email =email,
        password = hashing_password(password)
    )

    db.add(user)
    db.commit()


    return{"message":"User Registered Successfully"}
@app.post("/auth/login")
def login (email:str,password:str):
    db = SessionLocal()
    user = db.query(User).filter(
        User.email == email
    ).first() 

    if not user:
        return {"error":"User not available"}  
    if not verifying_password(
        password,
        user.password
    ):
        return{"error":"Incorrect password"}
    token = create_access_tokens(
        {"sub":user.email}
    )
    return{
        "access_token":token
    }
@app.post("/roles/create")
def create_role(role_name:str):
    db = SessionLocal()
    role= Role(
        role_name = role_name
    )
    db.add(role)
    db.commit()
    return {
    "message":"Role created successfully"
}
@app.post("/users/assign-role")
def assign_role(
    user_id : int,
    role_id : int
):
    db = SessionLocal()
    assignment = UserRole(
        user_id = user_id,
        role_id = role_id
    )
    db.add(assignment)
    db.commit()
    return{
        "message ":"Role Assigned Successfully"
    }
@app.get("/users/{user_id}/roles")
def get_role(user_id: int):
    db = SessionLocal()
    roles=(
        db.query(Role.role_name)
        .join(
            UserRole,
            Role.id == UserRole.role_id
        )
        .filter(
            UserRole.user_id == user_id
        )
        .all()
    )
    return roles
permission ={
    "Admin":[
        "CREATE",
        "VIEW",
        "UPDATE",
        "DELETE"
    ],
    "Financial Analyst":[
        "UPLOAD",
        "EDIT"
    ],
    "Auditor":[
        "REVIEW"
    ],
    "Client":[
        "VIEW"
    ]
}
@app.get("/users/{user_id}/permissions")
def get_permission(user_id:int):
    db= SessionLocal()
    role=(
        db.query(Role.role_name)
        .join(
            UserRole,
            Role.id ==UserRole.role_id
        )
        .filter(
            UserRole.user_id  == user_id
        )
        .first()
    )
    if not  role:
        return{
            "error" :"No role"
        }
    return permissions.get(
        role.role_name,
        []
    )

@app.post("/documents/upload")
def upload_document(
    title:str,
    company_name:str,
    document_type:str,
    uploaded_by:int,
    file:UploadFile = File(...)

):
    db = SessionLocal()
    file_path = f"upload/{file.filename}"

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document = Document(
        title = title,
        company_name=company_name,
        document_type=document_type,
        uploaded_by = uploaded_by,
        file_path = file_path,
        created_at = str(datetime.now())
    )

    db.add(document)
    db.commit()

    return{
        "message":"Document Uploaded Succesfully"
    }
@app.get("/documents")
def get_documents():
    db = SessionLocal()
    documents = db.query(Document).all()
    return documents

@app.get("/documents/{document_id}")
def get_document(document_id:int):
    db = SessionLocal()
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        return{"error":"Document not available"}
    return document

@app.delete("/documents/{document_id}")
def delete_document(document_id:int):
    db = SessionLocal()
    document = db.query(Document).filter(
        Document.document_id == document_id
    ).first()

    if not document:
        return{"error":"Document not available"}
    
    db.delete(document)
    db.commit()
    return {
        "message":"Document deleted Successfully"
    }

@app.get("/documents/search")
def search_documents(
    company_name:str = None,
    document_type = None
):
    db = SessionLocal()
    query = db.query(Document)
    if company_name:
        query=query.filter(
            Document.company_name == company_name
        )
    if document_type:
        query = query.filter(
            Document.document_type == document_type
        )
    return query.all()

@app.post("/rag/index-document")
def indeex_document(file: UploadFile = File(...)):
    file_path = f"upload/{file.filename}"
    with open (file_path,"wb") as f:
        f.write(file.file.read())

    text = extract_text(file_path)
    chunks = create_chunks(text)
    embeddings = create_embeddings(chunks)
    store_vectors(chunks,embeddings)

    return{
        "message":"Document Uploaded Successfully",
        "chunks":len(chunks)
    }

@app.get("/rag/search")
def search(query: str):

    query_vector = model.encode(query)

    results = client.search(
        collection_name="Financial_Documents",
        query_vector=query_vector.tolist(),
        limit=3
    )

    return [
        result.payload["text"]
        for result in results
    ]
@app.get("/rag/search")
def search(query: str):

    query_vector = model.encode(query)

    results = client.search(
        collection_name="Financial_Documents",
        query_vector=query_vector.tolist(),
        limit=5
    )

    chunks = [
        result.payload["text"]
        for result in results
    ]

    ranked = rerank(
        query,
        chunks
    )

    return ranked[:3]
@app.get("/rag/context")
def get_context(query: str):

    results = search_vectors(query)

    chunks = [
        result.payload["text"]
        for result in results
    ]

    ranked = rerank(
        query,
        chunks
    )

    context = "\n\n".join(
        chunk
        for chunk, score in ranked[:3]
    )

    return {
        "query": query,
        "context": context
    }