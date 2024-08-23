from tkinter import *
from tkinter import messagebox
from random import shuffle, choice, randint
import pyperclip
import sqlite3
from cryptography.fernet import Fernet
import os

# ---------------------------- CONSTANTS ------------------------------- #
# Key generation/loading
KEY_FILE = "key.key"

if not os.path.exists(KEY_FILE):
    # Generate the key and save it to a file if it doesn't exist
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    # Load the key from the file
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

# SQLite Database Setup
conn = sqlite3.connect('password_manager.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS passwords
             (website TEXT, email TEXT, password TEXT)''')

# cur.execute("SELECT * FROM passwords")
# rows = cur.fetchall()
# for row in rows:
#     print(row)

conn.commit()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    encrypted_password = cipher_suite.encrypt(password.encode())

    with conn:
        cur.execute("INSERT INTO passwords VALUES (:website, :email, :password)",
                  {'website': website, 'email': email, 'password': encrypted_password})

    website_entry.delete(0, END)
    password_entry.delete(0, END)

    messagebox.showinfo(title="Success", message="Password saved successfully.")


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website to search.")
        return

    cur.execute("SELECT * FROM passwords WHERE website=:website", {'website': website})
    record = cur.fetchone()

    if record:
        decrypted_password = cipher_suite.decrypt(record[2]).decode()
        messagebox.showinfo(title=website, message=f"Email: {record[1]}\nPassword: {decrypted_password}")
    else:
        messagebox.showinfo(title="Not Found", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="w")
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="w")
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky="w")

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
email_entry.insert(0, "nickwallace@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="ew")

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="ew")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="ew")
search_button = Button(text="Search", width=36, command=find_password)
search_button.grid(row=5, column=1, columnspan=2, sticky="ew")

window.mainloop()


# from tkinter import *
# from tkinter import messagebox
# from random import shuffle, choice, randint
# import pyperclip
#
#
# # ---------------------------- PASSWORD GENERATOR ------------------------------- #
# def generate_password():
#     letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
#                'v',
#                'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
#                'R',
#                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#     numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#     symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
#
#     password_letters = [choice(letters) for _ in range(randint(8, 10))]
#     password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
#     password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
#
#     password_list = password_numbers + password_symbols + password_letters
#     shuffle(password_list)
#
#     password = "".join(password_list)
#     password_entry.insert(0, password)
#     pyperclip.copy(password)
#
#
# # ---------------------------- SAVE PASSWORD ------------------------------- #
# def save():
#     website = website_entry.get()
#     email = email_entry.get()
#     password = password_entry.get()
#
#     if len(website) == 0 or len(password) == 0:
#         messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty. ")
#     else:
#         is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
#                                                               f"\nPassword: {password} \nIs it ok to save?")
#
#         if is_ok:
#             with open("data.txt", "a") as file:
#                 file.write(f"{website} | {email} | {password}\n")
#                 website_entry.delete(0, END)
#                 password_entry.delete(0, END)
#
#
# # ---------------------------- UI SETUP ------------------------------- #
# window = Tk()
# window.title("Password Manager")
# window.config(padx=50, pady=50)
#
# canvas = Canvas(width=200, height=200)
# logo_image = PhotoImage(file="logo.png")
# canvas.create_image(100, 100, image=logo_image)
# canvas.grid(row=0, column=1)
#
# # Labels
# website_label = Label(text="Website:")
# website_label.grid(row=1, column=0, sticky="w")
# email_label = Label(text="Email/Username:")
# email_label.grid(row=2, column=0, sticky="w")
# password_label = Label(text="Password:")
# password_label.grid(row=3, column=0, sticky="w")
#
# # Entries
# website_entry = Entry(width=35)
# website_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
# website_entry.focus()
# email_entry = Entry(width=35)
# email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
# email_entry.insert(0, "nickwallace@gmail.com")
# password_entry = Entry(width=21)
# password_entry.grid(row=3, column=1, sticky="ew")
#
# # Buttons
# generate_button = Button(text="Generate Password", command=generate_password)
# generate_button.grid(row=3, column=2, sticky="ew")
# add_button = Button(text="Add", width=36, command=save)
# add_button.grid(row=4, column=1, columnspan=2, sticky="ew")
#
# window.mainloop()
