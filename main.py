from words_dataset import words

def trie() -> dict:
    return {}

def node(eow=False) -> dict:
    return {
        "eow" : eow
    }

# ---------------- INSERT ---------------- #

def insert(trie:dict, word:str, addWord=True) -> None:
    word = word.lower()
    iter = len(word)
    def eow():
        return idx == (iter-1)
    
    for idx in range(iter):
        ch = word[idx]

        if not (ch.isalnum()):
            continue

        if ch not in trie:
            trie[ch] = node()
        
        if eow():
            trie[ch]["eow"] = addWord
            
        trie = trie[ch]

# ---------------- DELETE ---------------- #

def delete(trie: dict, word: str) -> bool:
    word = word.lower()

    def delete_helper(node, word, depth):
        # Base case: reached end of word
        if depth == len(word):
            if not node.get("eow", False):
                return False  # word not found

            node["eow"] = False

            # If node has no children, delete it
            return len(node) == 1  # only "eow" exists

        ch = word[depth]

        if ch not in node:
            return False  # word not found

        should_delete_child = delete_helper(node[ch], word, depth + 1)

        # If child should be deleted → remove it
        if should_delete_child:
            del node[ch]

            # Return True if current node also becomes useless
            return len(node) == 1 and not node["eow"]

        return False

    return delete_helper(trie, word, 0)

# ---------------- UPDATE ---------------- #

def update(trie:dict, word:str) -> None:
    insert(trie, word)

# ---------------- SEARCH ---------------- #

def isWord(trie:dict, word:str) -> bool:
    word = word.lower()
    iter = len(word)
    def eow():
        return idx == (iter-1)
    
    for idx in range(iter):
        ch = word[idx]

        if ch not in trie:
            return False

        if eow():
            return trie[ch]["eow"]

        trie = trie[ch]
        
    return False

# ---------------- PREFIX ---------------- #

def allWordsWithPrefix(trie:dict, prefix:str) -> list:
    prefix = prefix.lower()
    if not prefix:
        return []

    for ch in prefix:
        
        if ch not in trie:
            return []             
        trie = trie[ch]

    posWords = []
    def getWordsHelper(node: dict, postfix: str): #Recursive Function to get all words
        if node["eow"]: # Base Case
            posWords.append(prefix[:-1] + postfix)  
        for ch, child in node.items(): 
            if ch != "eow" and isinstance(child, dict): # Recursive Case
                getWordsHelper(child, postfix + ch)

    getWordsHelper(trie, prefix[-1] if prefix else "")
    return posWords


