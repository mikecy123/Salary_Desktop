import tkinter as tk
import time
import datetime
import os
import sys
import winreg

# ============ 配置 ============
MONTH_SALARY = 15000        # 月薪
SECONDS_PER_MONTH = 30 * 24 * 60 * 60
AUTO_START = True
# ==============================

salary_per_second = MONTH_SALARY / SECONDS_PER_MONTH

show_money = True
start_time = time.time()


# ============ 时间锚点 ============
def today_start():
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day)


def week_start():
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(days=now.weekday())
    return datetime.datetime(monday.year, monday.month, monday.day)


def month_start():
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, 1)


# ============ 核心 ============
def tick():
    now = datetime.datetime.now()

    today_money = (now - today_start()).total_seconds() * salary_per_second
    week_money = (now - week_start()).total_seconds() * salary_per_second
    month_money = (now - month_start()).total_seconds() * salary_per_second

    if show_money:
        label.config(
            text=f"{month_money:,.2f}:{week_money:,.2f}:{today_money:,.2f}"
        )
    else:
        elapsed = int(time.time() - start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    root.after(1000, tick)


# ============ 交互 ============
def toggle_mode(event=None):
    global show_money
    show_money = not show_money


def reset():
    global start_time
    start_time = time.time()


def exit_app():
    root.destroy()


# ============ 拖动 ============
def start_move(event):
    root.x = event.x
    root.y = event.y


def on_move(event):
    root.geometry(f"+{event.x_root - root.x}+{event.y_root - root.y}")


# ============ 右键菜单 ============
def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)


# ============ 开机自启 ============
def enable_autostart():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(
            key,
            "SalaryFloating",
            0,
            winreg.REG_SZ,
            sys.executable + " " + os.path.abspath(__file__)
        )
        winreg.CloseKey(key)
    except Exception:
        pass


# ============ GUI ============
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="#111111")
root.geometry("420x70+300+200")

label = tk.Label(
    root,
    text="0.00:0.00:0.00",
    font=("Consolas", 20, "bold"),
    fg="#00ff99",
    bg="#111111"
)
label.pack(fill="both", expand=True)

label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", on_move)
label.bind("<Double-Button-1>", toggle_mode)
label.bind("<Button-3>", show_menu)

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="重置计时", command=reset)
menu.add_separator()
menu.add_command(label="退出", command=exit_app)

if AUTO_START:
    enable_autostart()

tick()
root.mainloop()
