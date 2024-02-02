from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine, SessionLocal, initialize_db
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
#Here the quiz is created in the local database which will be reflected to the user when call the GET Method
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
#initialize function is called to initially show the questions on the UI
initialize_db()
#This is get method which has route /quizzes/id means it will show the specific quiz according to their id
@app.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id:int):
    db=SessionLocal()
    quiz=db.query(Quiz).filter(Quiz.id ==quiz_id).first()
    db.close()
    #This  will check for NULL if there is no any quiz  then it will be handled by this if else statement
    if quiz is None:
        raise HTTPException(status_code=404,detail="Quiz Not found")
    return quiz
#As we know submit is a post method because we are basically creating a new data. so method will be called
#we can submit the answer according to the quiz_id

@app.post("/submit/{quiz_id}")
async def submit_quiz(quiz_id: int, answers: dict):
    db = SessionLocal()
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    db.close()
    #Exception handling
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    #initially user_score is declared 0
    user_score = 0
    correct_answers = []
    #This for loop iterates through all the questions inside the quiz and also get the answer of the user, if the user have given correct answer then marks will be added
    for i, question in enumerate(quiz.questions):
        user_answer = answers.get(str(i + 1))
        if user_answer and user_answer.upper() == question["correct_answer"]:
            user_score += 1
            correct_answers.append(i + 1)
    result = {"user_score": user_score, "correct_answers": correct_answers}
    return result


#class for choices of the question there is two attributes one is string and other one is whether this one is true or not
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
#Question has two types of attributes one is string means question text and other one is list of options
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
# declares a function named get_db that will serve as a dependency for database access.

def get_db():
    #creates a new database session using a SessionLocal object. This object is typically configured to manage sessions for a specific database connection pool.
    db = SessionLocal()
    #initiates a try-finally block for exception handling.
    try:
        yield db
    finally:
        #closes the database session, releasing resources and preventing potential connection leaks.
        db.close()

db_dependency = Depends(get_db)
#get method to get question by question id but this method is for those questions which is created by the help of post method not for the one which is already initialized in initial database
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
#Here post method is used to create question as well, there can be two ways to create question one can be predefined other one can be created by the help of post method

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
