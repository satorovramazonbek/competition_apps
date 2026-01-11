import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk

ser = None
last_time = "0.0"

root = tk.Tk()
root.title("Serial Time Reader")
root.attributes('-fullscreen', True)
root.configure(bg='black')

# ================== LABEL ==================
label = tk.Label(
    root,
    text=last_time + " s",
    fg="lime",
    bg="black"
)
label.pack(expand=True, fill="both")

# ================== FONT AUTO RESIZE ==================
def resize_font(event=None):
    w = root.winfo_width()
    h = root.winfo_height()
    font_size = int(min(w * 0.25, h * 0.6))
    label.config(font=("Arial", font_size, "bold"))

# ================== SERIAL PORTS ==================
def get_ports():
    ports = serial.tools.list_ports.comports()
    return [p.device for p in ports]

# ================== CONNECT ==================
def connect_port():
    global ser
    port = port_combo.get()

    if not port:
        return

    try:
        ser = serial.Serial(port, 9600, timeout=1)
        status.config(text=f"CONNECTED: {port}", fg="lime")
    except Exception as e:
        status.config(text="ERROR", fg="red")
        print(e)

# ================== READ SERIAL ==================
def read_serial():
    global last_time

    if ser and ser.in_waiting:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if line.startswith("TIME:"):
                last_time = line.split(":")[1]
                label.config(text=last_time + " s")
        except:
            pass

    root.after(10, read_serial)

# ================== EXIT ==================
def exit_app(event=None):
    try:
        if ser:
            ser.close()
    except:
        pass
    root.destroy()

# ================== TOP CONTROL PANEL ==================
top = tk.Frame(root, bg="black")
top.place(relx=0.5, rely=0.05, anchor="n")

port_combo = ttk.Combobox(
    top,
    values=get_ports(),
    font=("Arial", 14),
    width=10
)
port_combo.pack(side="left", padx=10)

connect_btn = tk.Button(
    top,
    text="CONNECT",
    command=connect_port,
    font=("Arial", 14)
)
connect_btn.pack(side="left")

status = tk.Label(
    top,
    text="DISCONNECTED",
    fg="red",
    bg="black",
    font=("Arial", 14)
)
status.pack(side="left", padx=10)

# ================== BINDS ==================
root.bind("<Configure>", resize_font)
root.bind("<F11>", exit_app)

resize_font()
read_serial()
root.mainloop()
