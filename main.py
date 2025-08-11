from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, engine
from bert_module import analyze_email_body  # your local BERT analyzer
from llama_module import get_llama_response  # your local LLaMA integration

app = FastAPI()

# Create tables (if not already created)
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/process-emails")
def process_emails(db: Session = Depends(get_db)):
    emails = crud.get_emails_by_status(db, status="new")
    if not emails:
        return {"message": "No unprocessed emails found"}

    for email in emails:
        # Analyze email body with your BERT module
        bert_message = analyze_email_body(email.body)

        # Generate response with your local LLaMA model
        llama_response = get_llama_response(email.body, bert_message)

        # Update email record with bert message, llama response and status
        email.bert_message = bert_message
        email.llama_response = llama_response
        email.status = "processed"
        db.add(email)

    db.commit()
    return {"message": f"Processed {len(emails)} emails"}
