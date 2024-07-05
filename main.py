import os
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import pandas as pd
import datetime
import pickle

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition System")
        self.main_window.geometry("1200x600+350+100")
        self.main_window.configure(bg='#1a1a1a')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=('Helvetica', 16, 'bold'), padding=10, background='#3a3a3a', foreground='white')
        style.map("TButton", background=[('active', '#0059b3')])
        style.configure("TLabel", font=('Helvetica', 14), background='#1a1a1a', foreground='white')
        style.configure("TEntry", font=('Helvetica', 14))

        self.title_label = ttk.Label(self.main_window, text="Face Recognition System", font=('Helvetica', 28, 'bold'), background='#1a1a1a', foreground='cyan')
        self.title_label.place(x=300, y=10)

        self.login_button_main_window = util.get_button(self.main_window, 'Login', '#4caf50', self.login)
        self.login_button_main_window.place(x=850, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'Logout', '#f44336', self.logout)
        self.logout_button_main_window.place(x=850, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', '#9e9e9e', self.register_new_user, fg='White')
        self.register_new_user_button_main_window.place(x=850, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=50, y=100, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.attendance_data = []  # List to store attendance data

        self.logged_in_users = {}  # Dictionary to track currently logged-in users

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)  

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register a new user or try again.')
        elif name in self.logged_in_users:
            util.msg_box('Already Logged In', f'User {name} is already logged in.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}.')
            self.attendance_data.append({
                'Name': name,
                'Date': datetime.datetime.now().date().strftime('%Y-%m-%d'),
                'Time': datetime.datetime.now().time().strftime('%H:%M:%S'),
                'Action': 'in'
            })
            self.logged_in_users[name] = True
            self.export_to_excel()

    def logout(self):
        name = util.recognize(self.most_recent_capture_arr, self.db_dir)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register a new user or try again.')
        elif name not in self.logged_in_users:
            util.msg_box('Already Logged Out', f'User {name} is not currently logged in.')
        else:
            util.msg_box('Goodbye!', f'Goodbye, {name}.')
            self.attendance_data.append({
                'Name': name,
                'Date': datetime.datetime.now().date().strftime('%Y-%m-%d'),
                'Time': datetime.datetime.now().time().strftime('%H:%M:%S'),
                'Action': 'out'
            })
            del self.logged_in_users[name]
            self.export_to_excel()

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get()

        # Check if a face is detected before processing
        face_locations = face_recognition.face_locations(self.register_new_user_capture)
        if not face_locations:
            util.msg_box('Error', 'No face detected. Please try again.')
            return

        face_encodings = face_recognition.face_encodings(self.register_new_user_capture, face_locations)
        embeddings = face_encodings[0]  # Assuming only one face is detected

        file_path = os.path.join(self.db_dir, '{}.pickle'.format(name))
        with open(file_path, 'wb') as file:
            pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()

    def export_to_excel(self, excel_filename='attendance_log.xlsx'):
        try:
            new_data = pd.DataFrame(self.attendance_data)

            if os.path.exists(excel_filename):
                # Load existing data
                existing_data = pd.read_excel(excel_filename)

                # Append new data to existing data if it's not already present
                combined_data = pd.concat([existing_data, new_data], ignore_index=True).drop_duplicates(subset=['Name', 'Date', 'Time', 'Action'])
            else:
                # If file doesn't exist, just use the new data
                combined_data = new_data

            # Write combined data to Excel
            combined_data.to_excel(excel_filename, index=False)

            util.msg_box('Export Successful', f'Data successfully exported to {excel_filename}')
        except Exception as e:
            util.msg_box('Export Error', f'Error occurred while exporting to Excel: {str(e)}')

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
