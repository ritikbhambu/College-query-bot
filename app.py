from flask import Flask, render_template, request, redirect, session, jsonify
from chatbot.dbhelper import get_db_connection
from chatbot.query_engine import extract_query_info

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this before deployment

# ======================== LOGIN PAGE ========================
@app.route('/')
def login():
    return render_template('login.html')


# ======================== AUTHENTICATION ========================
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']  # 'student' or 'faculty'

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE emp_or_stud_id=%s AND password=%s AND role=%s"
    cursor.execute(query, (username, password, role))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        session['username'] = user['emp_or_stud_id']
        return redirect('/dashboard')
    else:
        return render_template('login.html', error="Invalid username, password, or role")


# ======================== DASHBOARD ========================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('dashboard.html', role=session['role'])


# ======================== LOGOUT ========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ======================== CHAT API ========================
@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'response': 'Session expired. Please log in again.'})

    user_message = request.json.get('message', '')
    intent, subject = extract_query_info(user_message)

    if intent == 'attendance':
        response = f"Your attendance in {subject or 'all subjects'} is 85%."
    elif intent == 'marks':
        response = f"Your marks in {subject or 'all subjects'} will be updated soon."
    elif intent == 'faculty':
        response = f"The faculty for {subject or 'CSE'} is Dr. Sharma."
    elif intent == 'unsupported':
        response = "Sorry, I can only provide your information, not others'."
    else:
        response = "Sorry, I couldn't understand your query."

    return jsonify({'response': response})


# ======================== CHATBOT PAGE ========================
@app.route('/chatbot')
def chatbot_page():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('chatbot.html')


# ======================== MAIN ========================
if __name__ == '__main__':
    app.run(debug=True)
