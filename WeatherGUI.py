#Simple GUI App That Asks The User for a City and Will List Out The Temperature (in F)!

import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageOps

import requests
from bs4 import BeautifulSoup

class CustomTitleBar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, bg="#E8F1FA", height=30, *args, **kwargs)
        self.master = master
        self.is_maximized = False
        self.normal_geometry = master.geometry()

        logo_img = Image.open("Logo.png").resize((24, 24)) 
        self.logo_photo = ImageTk.PhotoImage(logo_img)
        self.logo_label = tk.Label(self, image=self.logo_photo, bg="#E8F1FA")
        self.logo_label.pack(side=tk.LEFT, padx=5, pady=2)

        self.title_label = tk.Label(self, text="WeatherApp GUI (V-1.0)", bg="#E8F1FA",
                                    fg="black", font=("Segoe UI", 10, "bold"))
        self.title_label.pack(side=tk.LEFT)

        btn_style = {"bg": "#E8F1FA","fg": "black","borderwidth": 0,"highlightthickness": 0,             
        "highlightbackground": "#E8F1FA", "activebackground": "#3a3a3a", "font": ("Segoe UI", 10, "bold"),
        "width": 4, "height": 1, "activebackground": "#C0C0C0"}

        self.close_btn = tk.Button(self, text="X", command=self.master.destroy, **btn_style)
        self.close_btn.pack(side=tk.RIGHT)

        self.max_btn = tk.Button(self, text="❐", command=self.maximize_restore, **btn_style)
        self.max_btn.pack(side=tk.RIGHT)

        self.min_btn = tk.Button(self, text="—", command=self.minimize, **btn_style)
        self.min_btn.pack(side=tk.RIGHT)

        for widget in (self, self.logo_label, self.title_label):
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.master.x = event.x
        self.master.y = event.y

    def do_move(self, event):
        x = event.x_root - self.master.x
        y = event.y_root - self.master.y
        self.master.geometry(f"+{x}+{y}")

    def minimize(self):
        self.master.update_idletasks()
        self.master.overrideredirect(False)
        self.master.iconify()

    def maximize_restore(self):
        if not self.is_maximized:
            self.normal_geometry = self.master.geometry()
            self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0")
            self.is_maximized = True
            self.max_btn.config(text="🗗" if not self.is_maximized else "❐")
        else:
            self.master.geometry(self.normal_geometry)
            self.is_maximized = False
            self.max_btn.config()
        self.master.update_idletasks()

def resize_icon(img_path, max_size=(36, 36)):
    img = Image.open(img_path)
    img = ImageOps.contain(img, max_size)
    return ImageTk.PhotoImage(img)

def WeatherAppGUI():
    def WeatherSearch():
        city = user_text.get().strip().replace(" ", "-").lower()
        if not city:
            print("Please enter a city name.")
            return
        
        url = f"https://www.wunderground.com/weather/us/ca/{city}"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            userTemp = soup.find('span', class_='wu-value wu-value-to')

            if userTemp:
                valueF = userTemp.text
                print(f"It is {valueF}°F in {city}!")
            else:
                print("Sorry, temperature info not found. Check the city name.")
        except Exception as e:
            print("Error fetching weather:", e)

    homepage_icon = resize_icon("Logo.png", max_size=(75, 75))
    icon_label = tk.Label(content, image=homepage_icon, bg="#2F3E51")
    icon_label.image = homepage_icon
    icon_label.pack(pady=20)
    icon_label.place(x=175, y=25)

    greetings_label = tk.Label(content, text="Greetings, User!", fg="#E8F1FA", bg="#2F3E51", font=("Segoe UI", 16, "bold"))
    greetings_label.place(x=135, y=100)

    city_label = tk.Label(content, text="City: ", fg="#E8F1FA", bg="#2F3E51", font=("Segoe UI", 10, "bold"))
    city_label.place(x=67, y=148)

    user_text = tk.StringVar()
    user_input = tk.Entry(content, textvariable=user_text, font=("Segoe UI", 10, "bold"), width=30, bg="#2F3E51", fg="white")
    user_input.place(x=105, y=150)
    user_value = user_text.get()

    execute_button = tk.Button(content, text="Search Me!", font=("Segoe UI", 8, "bold"), fg="#E8F1FA", width=30, bg="#2F3E51", command=WeatherSearch)
    execute_button.pack(pady=10, fill="x", padx=10)
    execute_button.place(x=103, y=180)

root = tk.Tk()
root.overrideredirect(True)
root.geometry("420x400")
root.configure(bg="#2F3E51")

title_bar = CustomTitleBar(root)
title_bar.pack(fill=tk.X)

main_frame = tk.Frame(root, bg="#2F3E51")
main_frame.pack(expand=True, fill=tk.BOTH)

content = tk.Frame(main_frame, bg="#2F3E51")
content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

WeatherAppGUI()
root.bind("<Map>")
root.mainloop()