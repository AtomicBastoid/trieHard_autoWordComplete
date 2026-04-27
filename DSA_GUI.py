"""
Auto Word Complete Project using Trie data structure

DSA PROJECT
By: Muhammad Hadi, Syed Ebad, Eishal Keshwani
"""
import customtkinter as ctk
from main import trie, insert, words
from DSA_FEATURES import (
    load_data, update_frequency, get_top_suggestions,
    add_word_persistent, delete_word_persistent, get_history
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- SETUP ---------------- #

T = trie()
for w in words:
    insert(T, w)

load_data(T)

app = ctk.CTk()
app.title("TrieHard")
app.geometry("650x550")

buttons = []
current_suggestions = []
selected_index = 0
ignore_render = False


# ---------------- TEXT BOX ---------------- #

textbox = ctk.CTkTextbox(app, height=120)
textbox.pack(padx=20, pady=10, fill="x")


# ---------------- STATUS MESSAGE ---------------- #

status = ctk.CTkLabel(app, text="")
status.pack(pady=5)


def show_message(text):
    status.configure(text=text)
    app.after(2000, lambda: status.configure(text=""))


# ---------------- CLEAR BUTTON ---------------- #

def clear_text():
    textbox.delete("1.0", "end")
    clear_buttons()
    clear_btn.pack_forget()


clear_btn = ctk.CTkButton(app, text="Clear", command=clear_text)
clear_btn.pack(pady=5)
clear_btn.pack_forget()


# ---------------- TOP BUTTONS ---------------- #

btn_frame = ctk.CTkFrame(app)
btn_frame.pack(padx=20, pady=5, fill="x")

ctk.CTkButton(btn_frame, text="Add",     command=lambda: add_word()).pack(side="left", expand=True, padx=5)
ctk.CTkButton(btn_frame, text="Delete",  command=lambda: delete_word()).pack(side="left", expand=True, padx=5)
ctk.CTkButton(btn_frame, text="History", command=lambda: show_history()).pack(side="left", expand=True, padx=5)


# ---------------- SUGGESTIONS FRAME ---------------- #

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=10, fill="both", expand=True)


def clear_buttons():
    global selected_index
    for b in buttons:
        b.destroy()
    buttons.clear()
    selected_index = 0


def select_word(word):
    update_frequency(word)

    text = textbox.get("1.0", "end").strip()
    parts = text.split()

    if parts:
        parts[-1] = word

    textbox.delete("1.0", "end")
    textbox.insert("1.0", " ".join(parts) + " ")
    clear_buttons()


def render(lst):
    global current_suggestions
    current_suggestions = lst
    clear_buttons()

    for w in lst:
        btn = ctk.CTkButton(frame, text=w, command=lambda x=w: select_word(x))
        btn.pack(pady=2, fill="x")
        buttons.append(btn)

    highlight()


# ---------------- HIGHLIGHT ---------------- #

def highlight():
    for i, btn in enumerate(buttons):
        btn.configure(fg_color="#2ecc71" if i == selected_index else "gray20")


# ---------------- CURRENT WORD ---------------- #

def get_current_word_from_box():
    """Walk backwards from the cursor to extract the last alphanumeric token."""
    text = textbox.get("1.0", "end").strip()
    if not text:
        return ""

    token = []
    for ch in reversed(text):
        if ch.isalnum():
            token.append(ch)
        else:
            break

    return "".join(reversed(token)).lower()


# ---------------- KEY EVENTS ---------------- #

def on_key(event):
    global ignore_render

    if ignore_render:
        ignore_render = False
        return

    text = textbox.get("1.0", "end").strip()
    current = get_current_word_from_box()

    if text:
        clear_btn.pack(pady=5)
    else:
        clear_btn.pack_forget()

    if not current:
        clear_buttons()
        return

    render(get_top_suggestions(T, current))


def on_nav(event):
    global selected_index, ignore_render

    if not buttons:
        return

    ignore_render = True

    if event.keysym == "Down":
        selected_index = (selected_index + 1) % len(buttons)
    elif event.keysym == "Up":
        selected_index = (selected_index - 1) % len(buttons)
    elif event.keysym == "Return":
        select_word(current_suggestions[selected_index])
        return

    highlight()


textbox.bind("<KeyRelease>", on_key)
app.bind("<Up>",     on_nav)
app.bind("<Down>",   on_nav)
app.bind("<Return>", on_nav)


# ---------------- ACTIONS ---------------- #

def add_word():
    word = get_current_word_from_box()
    if word:
        if add_word_persistent(T, word):
            show_message(f"'{word}' added successfully")
        else:
            show_message(f"'{word}' already exists")


def delete_word():
    word = get_current_word_from_box()
    if word:
        if delete_word_persistent(T, word):
            show_message(f"'{word}' deleted successfully")
        else:
            show_message(f"'{word}' not found")


def show_history():
    render(get_history())


# ---------------- RUN ---------------- #

app.mainloop()
