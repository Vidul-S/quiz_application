from flask import Flask, render_template, request, redirect, url_for, session, g
app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Quiz questions related to web frameworks
questions = {
    1: {"question": "Which animal is known as the king of the jungle?", "options": ["Elephant", "Tiger", "Lion", "Bear"], "answer": "Lion"},
    2: {"question": "Which country is known as the Land of the Rising Sun?", "options": ["China", "India", "Japan", "Thailand"], "answer": "Japan"},
    3: {"question": "Which language is the most spoken worldwide?", "options": ["English", "Spanish", "Mandarin", "Hindi"], "answer": "Mandarin"},
    4: {"question": "Which country is known for the Great Wall?", "options": ["India", "China", "Japan", "Korea"], "answer": "China"},
    5: {"question": "Who painted the Mona Lisa?", "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"], "answer": "Leonardo da Vinci"},
    6: {"question": "Who was the first president of the United States?", "options": ["George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"], "answer": "George Washington"},
    7: {"question": "What is the capital of France?", "options": ["Paris", "Berlin", "Madrid", "Rome"], "answer": "Paris"},
    8: {"question": "Who wrote 'Romeo and Juliet'?", "options": ["William Shakespeare", "Charles Dickens", "Mark Twain", "J.K. Rowling"], "answer": "William Shakespeare"},
    9: {"question": "Who is the author of the Harry Potter series?", "options": ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "Stephen King"], "answer": "J.K. Rowling"},
    10: {"question": "What is the smallest country in the world?", "options": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"], "answer": "Vatican City"},
    11: {"question": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Mississippi", "Yangtze"], "answer": "Nile"},
    12: {"question": "How many dots appear in a pair of dice?", "options": ["36", "42", "30", "24"], "answer": "42"},
    13: {"question": "Which country has the most islands?", "options": ["Sweden", "Canada", "Norway", "Finland"], "answer": "Sweden"},
    14: {"question": "Which is the tallest mountain in the world?", "options": ["Mount Everest", "K2", "Kilimanjaro", "Mount Fuji"], "answer": "Mount Everest"},
    15: {"question": "Which sport is known as 'the beautiful game'?", "options": ["Basketball", "Cricket", "Football (Soccer)", "Tennis"], "answer": "Football (Soccer)"},
    16: {"question": "Which city is known as the Big Apple?", "options": ["Los Angeles", "Chicago", "New York City", "Miami"], "answer": "New York City"},
    17: {"question": "Which country is home to the kangaroo?", "options": ["Australia", "South Africa", "India", "Brazil"], "answer": "Australia"},
    18: {"question": "What is the hardest natural substance on Earth?", "options": ["Gold", "Iron", "Diamond", "Silver"], "answer": "Diamond"},
    19: {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"], "answer": "Blue Whale"},
    20: {"question": "Which country is famous for sushi?", "options": ["China", "Japan", "South Korea", "Thailand"], "answer": "Japan"}
}
@app.before_request
def before_request():
    g.questions = questions
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    if request.method == 'POST':
        session['score'] = 0
        session['current_question'] = 1
        session['answers'] = []  # Initialize the answers list
        return redirect(url_for('question'))
    return render_template('quiz.html')
@app.route('/question', methods=['POST', 'GET'])
def question():
    question_id = session.get('current_question')
    # Check if question_id is valid
    if question_id is None or question_id > len(questions):
        return redirect(url_for('result'))
    question_data = questions[question_id]
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == question_data['answer']:
            session['score'] += 1
        
        # Store the selected answer
        if 'answers' not in session:
            session['answers'] = []
        session['answers'].append(selected_option)
        # Move to the next question
        session['current_question'] += 1
        return redirect(url_for('question'))
    return render_template('question.html', question=question_data['question'], options=question_data['options'], qid=question_id)
@app.route('/review_answers')
def review_answers():
    questions_list = g.questions  # Retrieve questions from g
    answers = session.get('answers', [])  # Retrieve selected answers from the session
    correct_answers = [q['answer'] for q in questions_list.values()]  # Get correct answers
    total = len(questions_list)  # Total number of questions
    # Prepare a list of results to display in the review
    review_data = []
    for i in range(1, total + 1):
        review_data.append({
            'question': questions_list[i]['question'],
            'selected_answer': answers[i - 1] if i - 1 < len(answers) else None,
            'correct_answer': questions_list[i]['answer']
        })
    return render_template('review_answers.html', total=total, review_data=review_data)
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    # Example data (replace with your actual logic to get these values)
    answers = request.form.getlist('answers')  # Get the submitted answers
    correct_answers = [questions[i]['answer'] for i in range(1, len(questions) + 1)]  # Replace with your actual correct answers
    # Store the answers in the session
    session['answers'] = answers
    session['correct_answers'] = correct_answers  # Ensure you have correct answers stored as well
    score = sum(1 for i in range(len(answers)) if answers[i] == correct_answers[i])  # Example scoring logic
    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    return render_template('result.html', score=score, total=total, percentage=percentage)
@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(questions)
    percentage = (score / total) * 100
    answers = session.get('answers', [])
    correct_answers = [questions[i]['answer'] for i in range(1, total + 1)]
    
    return render_template('result.html', score=score, total=total, percentage=percentage, answers=answers, correct_answers=correct_answers)
if __name__ == '__main__':
    app.run(debug=True)