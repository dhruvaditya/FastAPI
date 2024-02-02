from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    choices = relationship("Choices", back_populates="question")

class Choices(Base):
    __tablename__ = 'choices'
    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Questions", back_populates="choices")

class Quiz(Base):
    __tablename__='quizzes'
    id=Column(Integer, primary_key= True, index=True)
    title=Column(String , index=True)
    questions=Column(JSON)