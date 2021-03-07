from tkinter import *
import multiprocessing
from rlbot.setup_manager import SetupManager
import psutil
import configparser

config = configparser.ConfigParser()
config.read("src/config.ini")


def start_match():
    try:
        manager = SetupManager()
        manager.early_start_seconds = 5
        manager.connect_to_game()
        manager.game_interface.load_interface(
            wants_quick_chat=False, wants_game_messages=False, wants_ball_predictions=False)
        manager.load_config(config_location="src/match.cfg")
        manager.launch_early_start_bot_processes()
        manager.start_match()
        manager.launch_bot_processes()
    except Exception as e:
        print(e)


def start():
    global proc_starter
    proc_starter = multiprocessing.Process(target=start_match)
    proc_starter.start()


def stop():
    try:
        id = proc_starter.pid
        proc = psutil.Process(id)
        proc.kill()
    except Exception as e:
        print(e)


def setbutton():
    playback_time = time_entry.get()
    config["SETTINGS"]["playback_time"] = playback_time
    with open("src/config.ini", "w") as pp:
        config.write(pp)


def setsnap():
    snap_set = snap_entry.get()
    config["SETTINGS"]["set_custom_snap"] = snap_set
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def setmode():
    mode_set = str(mode_var.get())
    config["SETTINGS"]["mode"] = mode_set
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


if __name__ == "__main__":
    root = Tk()
    mode_var = IntVar()
    mode_var.set(0)
    root.geometry("300x310")
    root.title("RIP core")
    Label(root, text="RIP CORE", font=("Courier", 18)).pack()
    time_label = Label(root, text="Set Playback Time", font=("Courier"))
    time_label.pack()
    time_entry = Entry(root, width=30)
    time_entry.pack()
    set_button = Button(root, text="SET TIME",
                        command=setbutton).pack()
    count_label = Label(root, text="Set Snap", font=("Courier"))
    count_label.pack()
    time_label.pack()
    snap_entry = Entry(root, width=30)
    snap_entry.pack()
    set_snap = Button(root, text="SET SNAP",
                      command=setsnap).pack()
    mode_label = Label(root, text="Select Mode", font=("Courier"))
    mode_label.pack()
    Radiobutton(root, text="BOTH", variable=mode_var,
                value=0, command=setmode).pack()
    Radiobutton(root, text="BALL", variable=mode_var,
                value=1, command=setmode).pack()
    start_button = Button(root, text="START", bg="green",
                          fg="white", width=20, command=start).pack(side=BOTTOM)
    stop_button = Button(root, text="STOP", bg="red",
                         fg="white", width=20, command=stop).pack(side=BOTTOM)
    root.mainloop()
