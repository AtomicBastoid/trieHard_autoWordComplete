import csv
from main import insert, delete, isWord, allWordsWithPrefix

FILE_NAME = "data.csv"

word_frequency = {}
word_status = {}
history = []


# ---------------- LOAD ---------------- #

def load_data(trie):
    try:
        f = open(FILE_NAME, "r")
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            word = row[0]
            freq = int(row[1])
            status = row[2]

            word_frequency[word] = freq
            word_status[word] = status

            if status == "active":
                insert(trie, word)

        f.close()
    except:
        pass


# ---------------- SAVE ---------------- #

def save_data():
    f = open(FILE_NAME, "w", newline="")
    writer = csv.writer(f)

    writer.writerow(["word", "frequency", "status"])

    for w in word_status:
        writer.writerow([w, word_frequency.get(w, 0), word_status[w]])

    f.close()


# ---------------- HISTORY ---------------- #

def add_to_history(word):
    word = word.lower()
    if word and word not in history:
        history.append(word)


def get_history():
    return history[-10:]


# ---------------- UPDATE ---------------- #

def update_frequency(word):
    word = word.lower()
    word_frequency[word] = word_frequency.get(word, 0) + 1
    word_status[word] = "active"

    add_to_history(word)
    save_data()


# ---------------- SUGGESTIONS ---------------- #

def get_top_suggestions(trie, prefix):
    words = allWordsWithPrefix(trie, prefix)
    words.sort(key=lambda w: word_frequency.get(w, 0), reverse=True)
    return words[:15]


# ---------------- ADD / DELETE ---------------- #

def add_word_persistent(trie, word):
    word = word.lower()

    if not isWord(trie, word):
        insert(trie, word)
        word_status[word] = "active"
        word_frequency[word] = word_frequency.get(word, 1)
        save_data()
        return True

    return False


def delete_word_persistent(trie, word):
    word = word.lower()

    if isWord(trie, word):
        delete(trie, word)
        word_status[word] = "deleted"
        word_frequency[word] = 0
        save_data()
        return True

    return False


# ---------------- CURRENT WORD ---------------- #

def get_current_word(text):
    parts = text.split()
    return parts[-1].lower() if parts else ""