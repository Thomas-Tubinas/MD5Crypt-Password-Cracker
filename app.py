from flask import Flask, render_template, request
from passlib.hash import md5_crypt

app = Flask(__name__)

words = []

def load_data():
    global words
    with open("wordlists.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            words.append(line)

def get_salt(hash):
    parts = hash.split('$')
    if len(parts) >= 3:
        return parts[2]
    return None

def crack(word, target_hash):
    hs = get_salt(target_hash)
    if hs:
        gen_hash = md5_crypt.using(salt=hs).hash(word)
        if gen_hash == target_hash:
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack_hash():
    target_hash = request.form['hash']
    load_data()
    for word in words:
        if crack(word, target_hash):
            return render_template('index.html', cracked=True, hash=target_hash, word=word)
    return render_template('index.html', cracked=False, hash=target_hash)

if __name__ == '__main__':
    app.run(debug=True)
