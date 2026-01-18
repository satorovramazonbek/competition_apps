import tkinter as tk
from tkinter import messagebox

# ================= GUI =================
root = tk.Tk()
root.title("Futbol hisob")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# ================= EKRAN O'LCHAMI =================
SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()

def fs(size):  # font scale (1080p asosida)
    return int((SCREEN_H / 1080) * size)

def ws(size):
    return int((SCREEN_W / 1920) * size)

# ================= O'ZGARUVCHILAR =================
score1 = tk.StringVar(value="0")
score2 = tk.StringVar(value="0")

team1 = tk.StringVar(value="—")
team2 = tk.StringVar(value="—")

team1_var = tk.StringVar(value="Tuman tanlang")
team2_var = tk.StringVar(value="Tuman tanlang")

START_TIME = 180
time_left = START_TIME
time_var = tk.StringVar(value="3:00")
result_var = tk.StringVar(value="")

game_over = False
timer_after_id = None

# ================= CHIQISH =================
def exit_app(e=None):
    root.destroy()

root.bind_all("<F11>", exit_app)

# ================= RESET =================
def back_to_setup(e=None):
    global time_left, game_over, timer_after_id

    if timer_after_id:
        root.after_cancel(timer_after_id)

    score1.set("0")
    score2.set("0")
    team1.set("—")
    team2.set("—")
    team1_var.set("Tuman tanlang")
    team2_var.set("Tuman tanlang")

    time_left = START_TIME
    time_var.set("3:00")
    result_var.set("")

    score1_label.config(font=("Arial", fs(360), "bold"))
    score2_label.config(font=("Arial", fs(360), "bold"))
    result_label.config(font=("Arial", fs(80), "bold"))

    game_over = False
    main_frame.pack_forget()
    setup_frame.pack(expand=True)

root.bind_all("<F2>", back_to_setup)

# ================= TUMANLAR =================
buxoro_tumanlari = [
    "Buxoro shahar", "Buxoro tuman", "G‘ijduvon", "Kogon shahar",
    "Kogon tuman", "Olot", "Qorako‘l", "Qorovulbozor",
    "Peshku", "Romitan", "Shofirkon", "Vobkent", "Jondor"
]

# ================= SETUP =================
setup_frame = tk.Frame(root, bg="black")
setup_frame.pack(expand=True)

teams_frame = tk.Frame(setup_frame, bg="black")
teams_frame.pack(pady=fs(40))

tk.Label(teams_frame, text="1-jamoa", fg="white", bg="black",
         font=("Arial", fs(48))).grid(row=0, column=0, padx=ws(80))

team1_menu = tk.OptionMenu(teams_frame, team1_var, *buxoro_tumanlari)
team1_menu.config(font=("Arial", fs(36)), bg="white")
team1_menu.grid(row=1, column=0, padx=ws(80))

tk.Label(teams_frame, text="2-jamoa", fg="white", bg="black",
         font=("Arial", fs(48))).grid(row=0, column=1, padx=ws(80))

team2_menu = tk.OptionMenu(teams_frame, team2_var, *buxoro_tumanlari)
team2_menu.config(font=("Arial", fs(36)), bg="white")
team2_menu.grid(row=1, column=1, padx=ws(80))

def start_app():
    if team1_var.get() == "Tuman tanlang" or team2_var.get() == "Tuman tanlang":
        messagebox.showerror("Xato", "2 ta tuman tanlanishi shart!")
        return

    team1.set(team1_var.get())
    team2.set(team2_var.get())

    setup_frame.pack_forget()
    main_frame.pack(expand=True, fill="both")
    countdown()

tk.Button(setup_frame, text="START", font=("Arial", fs(50)),
          command=start_app).pack(pady=fs(40))

# ================= ASOSIY EKRAN =================
main_frame = tk.Frame(root, bg="black")

# ---- VAQT (KICHRAYTIRILDI) ----
time_frame = tk.Frame(main_frame, bg="black")
time_frame.pack(side="top", fill="x")

tk.Label(time_frame, textvariable=time_var,
         font=("Arial", fs(110), "bold"),
         fg="yellow", bg="black").pack()

result_label = tk.Label(time_frame, textvariable=result_var,
                        font=("Arial", fs(80), "bold"),
                        fg="yellow", bg="black")
result_label.pack()

# ---- SCORE ----
score_frame = tk.Frame(main_frame, bg="black")
score_frame.pack(expand=True, fill="both")

score_frame.columnconfigure(0, weight=1)
score_frame.columnconfigure(1, weight=0)
score_frame.columnconfigure(2, weight=1)

# CHAP TOMON
left = tk.Frame(score_frame, bg="black")
left.grid(row=0, column=0, sticky="nsew")

tk.Label(left, textvariable=team1,
         font=("Arial", fs(80), "bold"),
         fg="red", bg="black").pack(pady=fs(10))

score1_label = tk.Label(left, textvariable=score1,
                        font=("Arial", fs(360), "bold"),
                        fg="red", bg="black")
score1_label.pack(pady=(fs(10), 0))

# CHIZIQ
tk.Frame(score_frame, bg="white", width=ws(18)).grid(row=0, column=1, sticky="ns")

# O‘NG TOMON
right = tk.Frame(score_frame, bg="black")
right.grid(row=0, column=2, sticky="nsew")

tk.Label(right, textvariable=team2,
         font=("Arial", fs(80), "bold"),
         fg="blue", bg="black").pack(pady=fs(10))

score2_label = tk.Label(right, textvariable=score2,
                        font=("Arial", fs(360), "bold"),
                        fg="blue", bg="black")
score2_label.pack(pady=(fs(10), 0))

# ================= KLAVIATURA =================
def key_handler(e):
    if game_over:
        return
    if e.char == "1":
        score1.set(str(int(score1.get()) + 1))
    elif e.char == "2":
        score2.set(str(int(score2.get()) + 1))

root.bind("<Key>", key_handler)

# ================= TIMER =================
def countdown():
    global time_left, timer_after_id
    if time_left >= 0:
        time_var.set(f"{time_left//60}:{time_left%60:02d}")
        time_left -= 1
        timer_after_id = root.after(1000, countdown)
    else:
        end_game()

# ================= END GAME =================
def end_game():
    global game_over
    game_over = True

    score1_label.config(font=("Arial", fs(240), "bold"))
    score2_label.config(font=("Arial", fs(240), "bold"))
    result_label.config(font=("Arial", fs(120), "bold"))

    if int(score1.get()) > int(score2.get()):
        result_var.set(f"WINNER: {team1.get()}")
    elif int(score2.get()) > int(score1.get()):
        result_var.set(f"WINNER: {team2.get()}")
    else:
        result_var.set("DRAW")

# ================= START =================
root.mainloop()
