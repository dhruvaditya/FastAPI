from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 
URL_DATABASE = 'postgresql://postgres:Post123@localhost/Quiz App'
engine=create_engine(URL_DATABASE)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
def initialize_db():
    db=SessionLocal()
    try:
        for quiz_data in quizzes_data:
            db_quiz=Quiz(**quiz_data)
            db.add(db_quiz)
        db.commit()
    finally:
        db.close()