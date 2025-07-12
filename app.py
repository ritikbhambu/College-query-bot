from flask import Flask, render_template, request, redirect, session
from chatbot.dbhelper import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 🔐 Change before deploying

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']  # <-- Add this line

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s"
    cursor.execute(query, (username, password, role))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['user_id']
        session['role'] = user['role']
        session['username'] = user['username']
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



if __name__ == '__main__':
    app.run(debug=True)
