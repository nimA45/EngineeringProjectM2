import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pysondb import db
from infrastructures.openai import get_questions, get_correction, create_keyword_questions
from utils.jwt_handler import encode_jwt, decode_jwt
from utils.db_utils import update_answer, create_session, get_question_by_id, get_question_index, get_keyword_question_by_id, get_keyword_question_index
from utils.random_string import id_generator
import os



class Answer(BaseModel):
    content: str

class AdminAuth(BaseModel):
    password: str

class Session(BaseModel):
    id: str
    name: str

class QuizzInformations(BaseModel):
    name: str
    job: str
    experience: int

json_db = db.getDb("db.json")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
def auth(request : Request, call_next):
    if 'authorization' in request.headers.keys():
        request.state.user = decode_jwt(request.headers["authorization"])
    return call_next(request)

# API health
@app.get("/")
def read_root():
    return True

@app.get("/api")
def read_api_root():
    return {"message": "Hello World !"}


# Get session
@app.post("/api/session")
def retrieve_session(session_details: Session):
    try:
        session = json_db.getByQuery({"id" : session_details.id})[0]

        if (session['name'] == session_details.name):
            token = encode_jwt({
                "session_id": session['id'],
                "session_name": session['name']
            })

            return {
                "session_id" : session['id'],
                "session_name": session['name'],
                "token": token
            }
        else:
            return {"error" : "Session doesn't exists"}
    except:
        return {"error" : "Internal errors or session doesn't exists"}
  
# Get quizz by session
@app.get('/api/quizz')
def quiz(request: Request):
    if request.state.user:
        try:
            return json_db.getByQuery({"id" : request.state.user['session_id']})[0]
        except:
            return {"error" : "Internal Error"}
    else:
        return {"error" : "Auth required"}

# Post user answer
@app.post("/api/quizz/{quizz_id}/{question_id}")
def quizz_post(request: Request, answer: Answer, quizz_id, question_id):
    if request.state.user:
        user_answer = answer.content

        try:
            session = json_db.getByQuery({"id" : quizz_id})[0]

            question = get_question_by_id(session, question_id)
            q_index = get_question_index(session, question_id)
                
            chat_response = get_correction(question, user_answer)
            chat_response = chat_response.strip()

            keyword_questions = create_keyword_questions(user_answer)

            session['questions'][q_index]['user_answer'] = user_answer
            session['questions'][q_index]['chat_response'] = chat_response

            session['questions'][q_index]['keyword_questions'] = []

            for i, keyword_question in enumerate(keyword_questions):
                session['questions'][q_index]['keyword_questions'].append({
                    "id": i,
                    "question": keyword_question,
                    "user_answer": "",
                    "chat_response": ""
                })

            json_db.update({"id" : quizz_id}, {"questions": session['questions']})

            return session['questions'][q_index]

        except ValueError:
            return {"error" : "Internal Error"}
    else:
        return {"error" : "Auth required"}

# Post user answer (keyword questions)
@app.post("/api/quizz/{quizz_id}/{question_id}/{keyword_question_id}")
def quizz_keyword_post(request: Request, answer: Answer, quizz_id, question_id, keyword_question_id):
    if request.state.user:
        user_answer = answer.content

        try:
            session = json_db.getByQuery({"id" : quizz_id})[0]

            keyword_question = get_keyword_question_by_id(session, question_id, keyword_question_id)
                
            chat_response = get_correction(keyword_question, user_answer)
            chat_response = chat_response.strip()
    
            q_index, kq_index = get_keyword_question_index(session, question_id, keyword_question_id)

            session['questions'][q_index]['keyword_questions'][kq_index]['user_answer'] = user_answer
            session['questions'][q_index]['keyword_questions'][kq_index]['chat_response'] = chat_response

            json_db.update({"id" : quizz_id}, {"questions": session['questions']})

            return session['questions'][q_index]
        
        except ValueError:
            return {"error" : "Internal Error"}
    else:
        return {"error" : "Auth required"}

# Auth admin
@app.post("/api/admin")
def connect_admin(admin_auth: AdminAuth):
    if admin_auth.password == os.environ['ADMIN_PASSWORD']:
        payload = {"is_admin": True}
        return encode_jwt(payload)
    else:
        return {"error" : "Wrong password"}
    
# Get all quizzes
@app.get('/api/admin/quizz')
def get_quiz():
    quizzes = json_db.getAll()
    return quizzes[::-1]

@app.post('/api/admin/quizz')
def generate_quizz(quizz_informations: QuizzInformations):
    job = quizz_informations.job 
    experience = quizz_informations.experience
    questions = []

    if job and experience:
        questions = get_questions(job, experience)
    else:
        raise HTTPException(status_code=422, detail="Field missing")
    
    session = {
        "name" : quizz_informations.name,
        "job" : quizz_informations.job,
        "experience": quizz_informations.experience,
        "questions" : [],
    }

    for i, question in enumerate(questions):
        session["questions"].append({
            "id": i,
            "question": question.strip(),
            "user_answer" : "",
            "chat_response" : "",
            "keyword_questions" : []
        })

    idToUpdate = json_db.add(session)
    json_db.update({"id" : idToUpdate}, {"id": id_generator()})
    
    return session['id']

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
