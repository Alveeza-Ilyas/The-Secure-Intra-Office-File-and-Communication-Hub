from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Login Credentials
USERNAME = "admin"
PASSWORD = "12345"

# Upload Folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder automatically
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home Page
@app.route('/')
def home():
    return render_template('login.html')

# Login
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        return redirect(url_for('dashboard'))

    return "Invalid Username or Password"

# Dashboard
@app.route('/dashboard')
def dashboard():

    files = os.listdir(UPLOAD_FOLDER)

    return render_template(
        'dashboard.html',
        files=files
    )

# Upload File
@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']

    if file:
        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )
        )

    return redirect('/dashboard')

# Download File
@app.route('/download/<filename>')
def download_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

# Chat Page
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Run App
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)