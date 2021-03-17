from tkinter import *
from rlbot.setup_manager import SetupManager
import configparser
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
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


def ending_time():
    end_time = replay_end.get()
    config["REPLAYER"]["end_time"] = end_time
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def record_time():
    config["SETTINGS"]["record_time"] = record_entry.get()
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def pack_saver():
    ext = [("All files", "*.*"),
           ("Training Packs", "*.pack")]
    file = asksaveasfilename(filetypes=ext, defaultextension=".pack")
    if file:
        config["REPLAYER"]["save_as"] = file
        with open("src/config.ini", "w") as cfg:
            config.write(cfg)


if __name__ == "__main__":
    root = Tk()
    mode_var = IntVar()
    mode_var.set(config["SETTINGS"]["mode"])
    root.title("RIP core")
    title = Label(root, text="          RIP CORE", font=("Courier", 18))
    title.grid()
    time_label = Label(root, text="Set Playback Time", font=("Courier"))
    time_label.grid()
    time_entry = Entry(root, width=30)
    time_entry.grid(row=2, column=0)
    set_button = Button(root, text="SET TIME",
                        command=setbutton)
    set_button.grid(row=2, column=1)

    count_label = Label(root, text="Set Snap", font=("Courier"))
    count_label.grid()
    snap_entry = Entry(root, width=30)
    snap_entry.grid(row=4, column=0)
    set_snap = Button(root, text="SET SNAP",
                      command=setsnap).grid(row=4, column=1)

    mode_label = Label(root, text="Select Mode", font=("Courier"))
    mode_label.grid()
    Radiobutton(root, text="BOTH", variable=mode_var,
                value=0, command=setmode).grid()
    Radiobutton(root, text="BALL", variable=mode_var,
                value=1, command=setmode).grid()
    record_label = Label(root, text="Set Recording Time", font=("Courier"))
    record_label.grid()
    record_entry = Entry(root, width=30)
    record_entry.grid(row=9, column=0)
    record_time_set = Button(root, text="SET TIME",
                             command=record_time)
    record_time_set.grid(row=9, column=1)
    Label(root, text="\n").grid()
    ttk.Separator(root, orient="horizontal").grid(
        row=11, columnspan=3, sticky="ew")

    Label(root, text="Replay Viewer", font=("Courier")).grid()
    file_button = Button(
        root, text="Select Record", command=fileselect)
    file_button.grid(row=12, column=1)
    replay_playback = Entry(root, width=30)
    replay_playback.grid(row=13, column=0)
    playback_button = Button(
        root, text="Set Starting Time", command=starting_time).grid(row=13, column=1)
    replay_end = Entry(root, width=30)
    replay_end.grid(row=14, column=0)
    replay_end_button = Button(
        root, text="Set Ending Time", command=ending_time).grid(row=14, column=1)
    save_button = Button(root, text="Create Pack",
                         command=pack_saver).grid(row=15)

    start_button = Button(root, text="START", bg="green",
                          fg="white", width=10, command=start).grid(row=16, sticky="e")
    stop_button = Button(root, text="STOP", bg="red",
                         fg="white", width=10, command=stop).grid(row=16, column=1)

    root.mainloop()
