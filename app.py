from flask import Flask, render_template, request
import secrets
import infobox_generation

app = Flask(__name__)

# Generate a random string of 32 bytes
app.secret_key = secrets.token_hex(32)

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/infobox', methods=['POST'])
def generate_infobox():
    url = request.form['userInput']
    ib, similarity_score = infobox_generation.generate_infobox(url)
    return ib
