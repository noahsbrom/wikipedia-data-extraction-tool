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

    while True:
        try:
            ib, _ = infobox_generation.generate_infobox(url)
            if ib != '':
                ib_dict = {}
                ib_arr = ib.split('\n')
                for pair in ib_arr:
                    pair_arr = pair.split(':')
                    key = pair_arr[0]
                    val = pair_arr[1]
                    ib_dict[key] = val
                break
        except:
            continue


    return render_template('infobox.html', infobox=ib_dict)
