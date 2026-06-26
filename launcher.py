from customtkinter import *
from tkinter import messagebox
from PIL import Image
import subprocess
import sys

window = CTk()
window.title("Mars")
window.iconbitmap("data/images/gui/icons/icon.ico")
window.geometry("700x600")
window.resizable(False, False)

bg_image = Image.open("data/images/background/launcher/launcher_bg.png")
bg = CTkImage(bg_image, size=(700, 600))
bg_label = CTkLabel(window, image=bg,text="")
bg_label.place(x=0, y=0)

gui_frame = CTkFrame(window, width=594, height=102,bg_color='blue', fg_color='blue')
gui_frame.place(x=0, y=498)

close_image = Image.open("data/images/gui/buttons/close 1.png")
close = CTkImage(close_image, size=(90, 90))
close_button = CTkButton(window, image=close, text="", width=90, height=90, command=window.destroy,bg_color='blue', fg_color='blue')
close_button.place(x=497, y=501)



combobox = CTkComboBox(
    window,
    values=["Одиночна гра", "Багатокористувацька гра"],
    
    # --- НАЛАШТУВАННЯ КОЛЬОРІВ ---
    bg_color="blue",              # Фон самого віджета (прозорий)
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
combobox.place(x=6,y=501)

def start_game():
    try:
        if combobox.get() == "Багатокористувацька гра":
            messagebox.showinfo("Інформація", "Багатокористувацька гра ще не реалізована.")
            return
        elif combobox.get() == "Одиночна гра":
            window.withdraw()
            subprocess.run([sys.executable, "singleplayer.py"])
            window.deiconify()
        else:
            messagebox.showwarning("Попередження", "Будь ласка, оберіть режим гри.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка при запуску гри:\n{e}")
start_button = CTkButton(window,bg_color="blue", text="Start", font=CTkFont(size=30, weight="bold"), width=250, height=63, command=start_game)

start_button.place(x=6, y=533)


window.mainloop()