import os
import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import face_recognition

def get_button(window, text, color, command, fg='white'):
    style = ttk.Style()
    style.configure(f"{color}.TButton", font=('Helvetica', 16, 'bold'), padding=10, background=color, foreground=fg)
    style.map(f"{color}.TButton", background=[('active', '#0059b3')])

    button = ttk.Button(
        window,
        text=text,
        command=command,
        style=f"{color}.TButton"
    )
    return button

def get_img_label(window):
    label = ttk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = ttk.Label(window, text=text)
    return label

def get_entry_text(window):
    inputtxt = ttk.Entry(window)
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)

def recognize(img, db_path):
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        with open(path_, 'rb') as file:
            embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'
