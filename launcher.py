from customtkinter import *
from tkinter import messagebox
import subprocess
import sys

window = CTk()
window.title("Mars")
window.geometry("500x500")
window.resizable(False, False)

title = CTkLabel(window, text="Mars doesn`t give you a second chance", font=CTkFont(size=24, weight="bold"))

def start_game():
    try:
        window.withdraw()
        subprocess.run([sys.executable, "main.py"])
        window.deiconify()
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка при запуску гри:\n{e}")
start_button = CTkButton(window, text="Start", font=CTkFont(size=30, weight="bold"), width=200, height=50, command=start_game)

title.pack(pady=10)

start_button.pack(pady=200)


window.mainloop()