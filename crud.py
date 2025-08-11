# crud.py
from models import Email

def get_emails_by_status(db, status):
    return db.query(Email).filter(Email.status == status).all()

def update_email(db, email, bert_message, llama_response):
    email.bert_message = bert_message
    email.llama_response = llama_response
    email.status = "processed"
    # Do NOT commit here; commit after processing all emails