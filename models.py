from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    date_received = Column(DateTime, nullable=True)
    sender = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    ticket_number = Column(String, nullable=True)
    bert_message = Column(Text, nullable=True)       # for sentiment analysis results
    llama_response = Column(Text, nullable=True)     # for generated reply
    category = Column(String, nullable=True)
    status = Column(String, nullable=True)
