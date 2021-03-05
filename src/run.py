from tkinter import *
import multiprocessing
from rlbot.setup_manager import SetupManager
import psutil
import json


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
    playback_time = int(time_entry.get())
    with open("src/Snapshot/playback.json", "w") as pp:
        json.dump({"playback_time": playback_time}, pp)


if __name__ == "__main__":
    root = Tk()

    root.geometry("300x300")
    root.title("RIP core")

    Label(root, text="Set PlayBack Time", font=("Courier", 18)).pack()
    time_entry = Entry(root, width=30)
    time_entry.pack()
    set_button = Button(root, text="SET TIME",
                        command=setbutton).pack()
    start_button = Button(root, text="START", bg="green",
                          fg="white", width=20, command=start).pack(side=BOTTOM)
    # test = Button(root, text="test", bg="green",
    #               fg="white", width=20, command=tes).pack(side=BOTTOM)
    stop_button = Button(root, text="STOP", bg="red",
                         fg="white", width=20, command=stop).pack(side=BOTTOM)

    root.mainloop()
