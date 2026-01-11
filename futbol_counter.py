import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports

# ================= GUI =================
root = tk.Tk()
root.title("Futbol hisob")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# ================= O'ZGARUVCHILAR =================
score1 = tk.StringVar(value="0")
score2 = tk.StringVar(value="0")

team1 = tk.StringVar(value="—")
team2 = tk.StringVar(value="—")

team1_var = tk.StringVar(value="Tuman tanlang")
team2_var = tk.StringVar(value="Tuman tanlang")

port_var = tk.StringVar()

START_TIME = 180
time_left = START_TIME
time_var = tk.StringVar(value="3:00")
result_var = tk.StringVar(value="")

game_over = False
ser = None
timer_after_id = None

# ================= CHIQISH =================
def exit_app(event=None):
    try:
        if ser:
            ser.close()
    except:
        pass
    root.destroy()

root.bind_all("<F11>", exit_app)

# ================= RESET (F2) =================
def back_to_setup(event=None):
    global ser, time_left, game_over, timer_after_id

    if timer_after_id:
        root.after_cancel(timer_after_id)
        timer_after_id = None

    try:
        if ser:
            ser.close()
    except:
        pass

    score1.set("0")
    score2.set("0")
    team1.set("—")
    team2.set("—")

    team1_var.set("Tuman tanlang")
    team2_var.set("Tuman tanlang")

    time_left = START_TIME
    time_var.set("3:00")
    result_var.set("")

    score1_label.config(font=("Arial", 400, "bold"))
    score2_label.config(font=("Arial", 400, "bold"))
    result_label.config(font=("Arial", 40, "bold"))
    result_label.pack_configure(pady=0)

    game_over = False

    main_frame.pack_forget()
    setup_frame.pack(expand=True)

root.bind_all("<F2>", back_to_setup)

# ================= TUMANLAR =================
buxoro_tumanlari = [
    "Buxoro shahar", "Buxoro tuman", "G‘ijduvon",
    "Kogon shahar", "Kogon tuman", "Olot",
    "Qorako‘l", "Qorovulbozor", "Peshku",
    "Romitan", "Shofirkon", "Vobkent", "Jondor"
]

def get_ports():
    return [p.device for p in serial.tools.list_ports.comports()]

# ================= SETUP OYNASI =================
setup_frame = tk.Frame(root, bg="black")
setup_frame.pack(expand=True)

teams_frame = tk.Frame(setup_frame, bg="black")
teams_frame.pack(pady=30)

# ---- 1-JAMOA ----
tk.Label(teams_frame, text="1-jamoa", fg="white", bg="black",
         font=("Arial", 32)).grid(row=0, column=0, padx=40, pady=10)

team1_menu = tk.OptionMenu(teams_frame, team1_var, *buxoro_tumanlari)
team1_menu.config(font=("Arial", 28), bg="white", width=18)
team1_menu["menu"].config(font=("Arial", 24))
team1_menu.grid(row=1, column=0, padx=40)

# ---- 2-JAMOA ----
tk.Label(teams_frame, text="2-jamoa", fg="white", bg="black",
         font=("Arial", 32)).grid(row=0, column=1, padx=40, pady=10)

team2_menu = tk.OptionMenu(teams_frame, team2_var, *buxoro_tumanlari)
team2_menu.config(font=("Arial", 28), bg="white", width=18)
team2_menu["menu"].config(font=("Arial", 24))
team2_menu.grid(row=1, column=1, padx=40)

# ---- PORT ----
tk.Label(setup_frame, text="COM port", fg="white",
         bg="black", font=("Arial", 28)).pack(pady=20)

ports = get_ports()
if not ports:
    ports = ["Port topilmadi"]

port_var.set(ports[0])

port_menu = tk.OptionMenu(setup_frame, port_var, *ports)
port_menu.config(font=("Arial", 24), bg="white", width=15)
port_menu["menu"].config(font=("Arial", 20))
port_menu.pack()

# ================= START =================
def start_app():
    global ser, game_over, timer_after_id

    if team1_var.get() == "Tuman tanlang" or team2_var.get() == "Tuman tanlang":
        messagebox.showerror("Xato", "2 ta tuman tanlanishi shart!")
        return

    if port_var.get() == "Port topilmadi":
        messagebox.showerror("Xato", "Arduino ulanmagan!")
        return

    try:
        ser = serial.Serial(port_var.get(), 9600, timeout=0.1)
    except:
        messagebox.showerror("Xato", "COM port ochilmadi!")
        return

    team1.set(team1_var.get())
    team2.set(team2_var.get())
    game_over = False

    setup_frame.pack_forget()
    main_frame.pack(expand=True, fill="both")

    read_serial()
    countdown()

tk.Button(setup_frame, text="START",
          font=("Arial", 28), command=start_app).pack(pady=40)

# ================= ASOSIY EKRAN =================
main_frame = tk.Frame(root, bg="black")

# ---- VAQT ----
time_frame = tk.Frame(main_frame, bg="black")
time_frame.pack(side="top", fill="x")

tk.Label(time_frame, textvariable=time_var,
         font=("Arial", 120, "bold"),
         fg="yellow", bg="black").pack()

result_label = tk.Label(time_frame, textvariable=result_var,
                        font=("Arial", 40, "bold"),
                        fg="yellow", bg="black")
result_label.pack()

# ---- SCORE ----
score_frame = tk.Frame(main_frame, bg="black")
score_frame.pack(expand=True, fill="both")

score_frame.columnconfigure(0, weight=1)
score_frame.columnconfigure(1, weight=0)
score_frame.columnconfigure(2, weight=1)

# CHAP
left = tk.Frame(score_frame, bg="black", width=600, height=800)
left.grid(row=0, column=0, sticky="nsew")
left.pack_propagate(False)

tk.Label(left, textvariable=team1,
         font=("Arial", 80, "bold"),
         fg="red", bg="black").place(relx=0.5, y=60, anchor="center")

score1_label = tk.Label(left, textvariable=score1,
                        font=("Arial", 400, "bold"),
                        fg="red", bg="black")
score1_label.place(relx=0.5, rely=0.55, anchor="center")

# CHIZIQ
tk.Frame(score_frame, bg="white", width=14).grid(row=0, column=1, sticky="ns")

# O‘NG
right = tk.Frame(score_frame, bg="black", width=600, height=800)
right.grid(row=0, column=2, sticky="nsew")
right.pack_propagate(False)

tk.Label(right, textvariable=team2,
         font=("Arial", 80, "bold"),
         fg="blue", bg="black").place(relx=0.5, y=60, anchor="center")

score2_label = tk.Label(right, textvariable=score2,
                        font=("Arial", 400, "bold"),
                        fg="blue", bg="black")
score2_label.place(relx=0.5, rely=0.55, anchor="center")

# ================= SERIAL =================
def read_serial():
    if game_over:
        return

    if ser and ser.in_waiting:
        line = ser.readline().decode(errors="ignore").strip()
        for p in line.split():
            if p.startswith("btn1_"):
                score1.set(p.split("_")[1])
            elif p.startswith("btn2_"):
                score2.set(p.split("_")[1])

    root.after(10, read_serial)

# ================= TIMER =================
def countdown():
    global time_left, game_over, timer_after_id

    if game_over:
        return

    if time_left >= 0:
        time_var.set(f"{time_left//60}:{time_left%60:02d}")
        time_left -= 1
        timer_after_id = root.after(1000, countdown)
    else:
        end_game()
        timer_after_id = root.after(3000, back_to_setup)

# ================= END GAME =================
def end_game():
    global game_over
    game_over = True

    score1_label.config(font=("Arial", 220, "bold"))
    score2_label.config(font=("Arial", 220, "bold"))
    result_label.config(font=("Arial", 90, "bold"))
    result_label.pack_configure(pady=40)

    s1 = int(score1.get())
    s2 = int(score2.get())

    if s1 > s2:
        result_var.set(f"WINNER: {team1.get()}")
    elif s2 > s1:
        result_var.set(f"WINNER: {team2.get()}")
    else:
        result_var.set("DRAW")

# ================= START =================
root.mainloop()
