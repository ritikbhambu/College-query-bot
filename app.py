from flask import Flask, render_template, request, redirect, session
from chatbot.dbhelper import get_db_connection
from flask import jsonify
from chatbot.query_engine import extract_query_info


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 🔐 Change before deploying

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']  

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


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('dashboard.html', role=session['role'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Call your NLP/spaCy function here
    response = f"You asked: {user_message}"  # Placeholder
    return jsonify({'response': response})

@app.route('/chatbot')
def chatbot_page():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)
