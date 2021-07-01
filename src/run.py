from tkinter import *
from rlbot.setup_manager import SetupManager
from configparser import ConfigParser
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

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
    config = ConfigParser()
    config.read("src/config.ini")
    playback_time = time_entry.get()
    config["SETTINGS"]["playback_time"] = playback_time
    with open("src/config.ini", "w") as pp:
        config.write(pp)


def setsnap():
    config = ConfigParser()
    config.read("src/config.ini")
    snap_set = snap_entry.get()
    config["SETTINGS"]["set_custom_snap"] = snap_set
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def setmode():
    config = ConfigParser()
    config.read("src/config.ini")
    mode_set = str(mode_var.get())
    config["SETTINGS"]["mode"] = mode_set
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)
    
def setteams():
    config = ConfigParser()
    config.read("src/match.cfg")
    team_set = str(team_var.get())
    
    if team_set == "0":
        config["Match Configuration"]["num_participants"] = "2"
        config["Participant Configuration"]["participant_team_1"] = "1"
    elif team_set == "1":
        config["Match Configuration"]["num_participants"] = "4"
        config["Participant Configuration"]["participant_team_1"] = "0"
        config["Participant Configuration"]["participant_team_2"] = "1"
        config["Participant Configuration"]["participant_team_3"] = "1"
    elif team_set == "2":
        config["Match Configuration"]["num_participants"] = "6"
        config["Participant Configuration"]["participant_team_1"] = "0"
        config["Participant Configuration"]["participant_team_2"] = "0"
        config["Participant Configuration"]["participant_team_3"] = "1"       
        config["Participant Configuration"]["participant_team_4"] = "1"
        config["Participant Configuration"]["participant_team_5"] = "1"  
    with open("src/match.cfg", "w") as cfg:
            config.write(cfg)

def fileselect():
    config = ConfigParser()
    config.read("src/config.ini")
    filename = askopenfilename()
    file_button["text"] = os.path.basename(filename)
    config["REPLAYER"]["file"] = os.path.basename(filename)
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def starting_time():
    config = ConfigParser()
    config.read("src/config.ini")
    start_time = replay_playback.get()
    config["REPLAYER"]["start_time"] = start_time
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def ending_time():
    config = ConfigParser()
    config.read("src/config.ini")
    end_time = replay_end.get()
    config["REPLAYER"]["end_time"] = end_time
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def record_time():
    config = ConfigParser()
    config.read("src/config.ini")
    config["SETTINGS"]["record_time"] = record_entry.get()
    with open("src/config.ini", "w") as cfg:
        config.write(cfg)


def pack_saver():
    config = ConfigParser()
    config.read("src/config.ini")
    ext = [("All files", "*.*"),
           ("Training Packs", "*.pack")]
    file = asksaveasfilename(filetypes=ext, defaultextension=".pack")
    if file:
        config["REPLAYER"]["save_as"] = file
        with open("src/config.ini", "w") as cfg:
            config.write(cfg)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("src/config.ini")
    teamconfig = ConfigParser()
    teamconfig.read("src/match.cfg")
    root = Tk()
    mode_var = IntVar()
    mode_var.set(config["SETTINGS"]["mode"])
    team_var = IntVar()
    team_var.set(teamconfig["Match Configuration"]["num_participants"])
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
    mode_label.grid(row=6, column = 0)
    Radiobutton(root, text="BOTH", variable=mode_var,
                value=0, command=setmode).grid()
    Radiobutton(root, text="BALL", variable=mode_var,
                value=1, command=setmode).grid()
    teams_label = Label(root, text= "Select Team Size", font=("Courier"))
    teams_label.grid(row=6, column = 1)
    Radiobutton(root, text="1v1", variable=team_var, 
                value = 0, command=setteams).grid(row = 7, column = 1)
    Radiobutton(root, text="2v2", variable=team_var, 
                value = 1, command=setteams).grid(row = 8, column =1)
    Radiobutton(root, text="3v3", variable=team_var, 
                value = 2, command=setteams).grid(row = 9, column = 1)        
    record_label = Label(root, text="Set Recording Time", font=("Courier"))
    record_label.grid()
    record_entry = Entry(root, width=30)
    record_entry.grid(row=10, column=0)
    record_time_set = Button(root, text="SET TIME",
                             command=record_time)
    record_time_set.grid(row=10, column=1)
    Label(root, text="\n").grid()
    ttk.Separator(root, orient="horizontal").grid(
        row=11, columnspan=3, sticky="ew")

    Label(root, text="Replay Viewer", font=("Courier")).grid()
    file_button = Button(
        root, text="Select Record", command=fileselect)
    file_button.grid(row=13, column=1)
    replay_playback = Entry(root, width=30)
    replay_playback.grid(row=14, column=0)
    playback_button = Button(
        root, text="Set Starting Time", command=starting_time).grid(row=14, column=1)
    replay_end = Entry(root, width=30)
    replay_end.grid(row=15, column=0)
    replay_end_button = Button(
        root, text="Set Ending Time", command=ending_time).grid(row=15, column=1)
    save_button = Button(root, text="Create Pack",
                         command=pack_saver).grid(row=17)

    start_button = Button(root, text="START", bg="green",
                          fg="white", width=10, command=start).grid(row=17, sticky="e")
    stop_button = Button(root, text="STOP", bg="red",
                         fg="white", width=10, command=stop).grid(row=17, column=1)

    root.mainloop()
