from utils.random_string import id_generator

def update_answer():
    return

def create_session(info, questions):
    session = {
        "id" : id_generator(),
        "name" : info['name'],
        "job" : info['job'],
        "experience" : info['experience'],
        "questions" : []
    }

    for i, question in enumerate(questions):
        session["questions"].append({
            "id": i,
            "question": question,
            "user_answer" : "",
            "chat_response" : ""
        })

def get_question_by_id(session, question_id):
    for question in session['questions']:
        if str(question['id']) != str(question_id):
            continue
        
        return question
    
def get_keyword_question_by_id(session, question_id, keyword_question_id):
    for question in session['questions']:
        if str(question['id']) != str(question_id):
            continue

        for keyword_questions in question['keyword_questions']:
            if str(keyword_questions['id']) != str(keyword_question_id):
                continue

            return keyword_questions

def get_question_index(session, question_id):
    for i, question in enumerate(session['questions']):
        if str(question['id']) != str(question_id):
            continue

        return i
    
def get_keyword_question_index(session, question_id, keyword_question_id):
    for i, question in enumerate(session['questions']):
        if str(question['id']) != str(question_id):
            continue

        for j, keyword_questions in enumerate(question['keyword_questions']):
            if str(keyword_questions['id']) != str(keyword_question_id):
                continue

            return i, j