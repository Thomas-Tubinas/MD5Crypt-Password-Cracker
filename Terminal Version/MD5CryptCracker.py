from passlib.hash import md5_crypt

words = []
hashes = []
salts = []

def Load():
    global words, hashes
    with open("hashes.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            hashes.append(line)
    with open("wordlist.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            words.append(line)

def salt(hash):
    parts = hash.split('$')
    if len(parts) >= 3:
        return parts[2]
    return None

def crack(word):
    for h in hashes[:]:
        hs = salt(h)
        genHash = md5_crypt.using(salt=hs).hash(word)
        if(genHash == h):
            print(h,word)
            hashes.remove(h)
Load()
cracked = len(hashes)
for w in words:
    crack(w)
print(cracked)
