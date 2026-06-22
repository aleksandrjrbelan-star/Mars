from customtkinter import *
from tkinter import messagebox
from PIL import Image
import subprocess
import sys

window = CTk()
window.title("Mars")
window.geometry("700x600")
window.resizable(False, False)

bg_image = Image.open("data/images/background/launcher/launcher_bg.png")
bg = CTkImage(bg_image, size=(700, 600))
bg_label = CTkLabel(window, image=bg,text="")
bg_label.place(x=0, y=0)

combobox = CTkComboBox(
    window,
    values=["Одиночна гра", "Багатокористувацька гра"],
    
    # --- НАЛАШТУВАННЯ КОЛЬОРІВ ---
    bg_color="transparent",              # Фон самого віджета (прозорий)
    fg_color="#1a1a1a",          # Колір самого поля (темно-сірий)
    border_color="#FF4500",      # Колір рамки (марсіанський помаранчевий)
    button_color="#FF4500",      # Колір стрілочки вибору
    button_hover_color="#cc3700",# Колір стрілочки при наведенні
    text_color="white",          # Колір тексту в полі
    dropdown_text_color="white", # Колір тексту у випадаючому списку
    dropdown_fg_color="#2b2b2b", # Фон самого випадаючого списку
    dropdown_hover_color="#FF4500", # Колір рядка, на який навели мишку
    state="readonly",
    width=250
)
combobox.place(x=11,y=466)

def start_game():
    try:
        if combobox.get() == "Багатокористувацька гра":
            messagebox.showinfo("Інформація", "Багатокористувацька гра ще не реалізована.")
            return
        else:
            window.withdraw()
            subprocess.run([sys.executable, "singleplayer.py"])
            window.deiconify()
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка при запуску гри:\n{e}")
start_button = CTkButton(window, text="Start", font=CTkFont(size=30, weight="bold"), width=300, height=79, command=start_game)

start_button.place(x=11, y=508)


window.mainloop()