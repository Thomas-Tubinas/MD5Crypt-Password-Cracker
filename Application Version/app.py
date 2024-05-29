from flask import Flask, render_template, request
from passlib.hash import md5_crypt
import concurrent.futures
app = Flask(__name__)

words = set()

def load_data():
    global words
    with open("wordlist.txt", "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        words = {line.strip() for line in lines}
load_data()
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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(crack, word, target_hash): word for word in words}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return render_template('index.html', cracked=True, hash=target_hash, word=result)
    return render_template('index.html', cracked=False, hash=target_hash)
if __name__ == '__main__':
    app.run(debug=True)
