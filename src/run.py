from tkinter import *
from rlbot.setup_manager import SetupManager
import configparser
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os

config = configparser.ConfigParser()
config.read("src/config.ini")

manager = SetupManager()


def start():
    manager.early_start_seconds = 5
    manager.connect_to_game()
    manager.game_interface.load_interface(
        wants_quick_chat=False, wants_game_messages=False, wants_ball_predictions=False)
    manager.load_config(config_location="src/match.cfg")
    manager.launch_early_start_bot_processes()
    manager.start_match()
    manager.launch_bot_processes()


def stop():
    manager.shut_down(kill_all_pids=True)


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


def fileselect():
    filename = askopenfilename()
    file_button["text"] = os.path.basename(filename)
    config["REPLAYER"]["file"] = os.path.basename(filename)
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def starting_time():
    start_time = replay_playback.get()
    config["REPLAYER"]["start_time"] = start_time
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


if __name__ == "__main__":
    root = Tk()
    mode_var = IntVar()
    mode_var.set(config["SETTINGS"]["mode"])
    root.geometry("350x400")
    root.title("RIP core")
    Label(root, text="RIP CORE", font=("Courier", 18)).pack()

    time_label = Label(root, text="Set Playback Time", font=("Courier"))
    time_label.pack()
    time_entry = Entry(root, width=30)
    time_entry.pack()
    set_button = Button(root, text="SET TIME",
                        command=setbutton)
    set_button.pack()

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

    ttk.Separator(root, orient="horizontal").pack(fill="x")

    Label(root, text="Replay Viewer", font=("Courier")).pack()
    file_button = Button(
        root, text="Select Record", command=fileselect)
    file_button.pack()
    replay_playback = Entry(root, width=30)
    replay_playback.pack()
    playback_button = Button(
        root, text="Set Starting Time", command=starting_time).pack()

    stop_button = Button(root, text="STOP", bg="red",
                         fg="white", width=20, command=stop).pack(side=BOTTOM)
    start_button = Button(root, text="START", bg="green",
                          fg="white", width=20, command=start).pack(side=BOTTOM)
    root.mainloop()
