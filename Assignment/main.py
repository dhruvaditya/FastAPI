from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine, SessionLocal, initialize_db
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
quizzes_data=[
    {
        "title":"AI Quiz",
        "questions":[
            {
                "statement":"What is full form of AI?" ,
                "options":["A. Artificial Intelligence", "B. Arduino Intelligence"],
                "correct_answer":"A",
            },
            {
                "statement":"What is the most interesting thing to learn in this decade?" ,
                "options":["A. Artificial Intelligence", "B. Fashion design"],
                "correct_answer":"A",
            },
            {
                "statement":"Where is statue of unity situated?" ,
                "options":["A. Bihar", "B. Gujarat"],
                "correct_answer":"B",
            }

        ]
    }
]
initialize_db()
@app.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id:int):
    db=SessionLocal()
    quiz=db.query(Quiz).filter(Quiz.id ==quiz_id).first()
    db.close()
    if quiz is None:
        raise HTTPException(status_code=404,detail="Quiz Not found")
    return quiz

@app.post("/submit/{quiz_id}")
async def submit_quiz(quiz_id: int, answers: dict):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.close()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user_score = 0
    correct_answers = []

    for i, question in enumerate(quiz.questions):
        user_answer = answers.get(str(i + 1))
        if user_answer and user_answer.upper() == question["correct_answer"]:
            user_score += 1
            correct_answers.append(i + 1)

    result = {"user_score": user_score, "correct_answers": correct_answers}
    return result



class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)
@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id==question_id).first()
    if not result:
        raise HTTPException (status_code=404, detail='Questions is not found')
    return result
@app.get("/choices/{question_id}")
async def read_choices(question_id:int, db:db_dependency):
          result=db.query(models.Choices).filter(models.Choices.question_id==question_id).all()
          if not result:
             raise HTTPException (status_code=404,detail='Question is not found')
          return result

@app.post("/questions")
async def create_questions(question: QuestionBase, db: Session = db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    
    db.commit()
    db.refresh(db_question)

    return {"message": "Question created successfully"}
