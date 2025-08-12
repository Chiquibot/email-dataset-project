from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, engine
from bert_module import analyze_email_body
from llama_module import get_llama_response
from models import Email
import psycopg2
from psycopg2.extras import RealDictCursor
from knowledge_base import knowledge_base

# Import your knowledge base here (adjust path as needed)
from knowledge_base import knowledge_base

# Create tables at startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database connection for raw psycopg2 queries
conn = psycopg2.connect("postgresql://postgres:admin@localhost:5432/fastapi_react_db")

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/processed-emails-raw")
def get_processed_emails_raw():
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT * FROM emails
            WHERE status = 'processed'
            ORDER BY id DESC
            LIMIT 20;
        """)
        rows = cur.fetchall()
    return {"emails": rows}

@app.get("/processed-emails")
def get_processed_emails(db: Session = Depends(get_db)):
    emails = db.query(Email).filter(Email.status == "processed").all()
    result = [
        {
            "id": e.id,
            "subject": e.subject,
            "body": e.body,
            "bert_message": e.bert_message,
            "llama_response": e.llama_response,
            "status": e.status,
            # add other fields if needed
        }
        for e in emails
    ]
    return {"emails": result}

@app.post("/process-emails")
def process_emails(db: Session = Depends(get_db)):
    emails = crud.get_emails_by_status(db, status="new")
    if not emails:
        return {"message": "No unprocessed emails found"}

    processed_count = 0
    for email in emails:
        try:
            bert_message = analyze_email_body(email.body)

            # You can implement filtering logic here to pick relevant Q&A pairs
            # For now, we pass the full knowledge base
            relevant_qa_pairs = knowledge_base

            llama_response = get_llama_response(
                email.subject,
                email.body,
                bert_message,
                relevant_qa_pairs
            )

            email.bert_message = bert_message
            email.llama_response = llama_response
            email.status = "processed"
            db.add(email)
            processed_count += 1
        except Exception as e:
            print(f"Error processing email {email.id}: {e}")

    db.commit()
    return {"message": f"Processed {processed_count} emails"}
