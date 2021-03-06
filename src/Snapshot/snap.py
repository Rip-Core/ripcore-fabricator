import pickle
import copy
import configparser


class Recorder:
    def __init__(self):
        self.config = None
        self.snap_count = None
        self.buffer = []

    def store(self, packet):
        self.buffer.append(copy.deepcopy(packet))

    def save(self):
        config = configparser.ConfigParser()
        config.read("src/config.ini")
        self.snap_count = int(config["SETTINGS"]["snap_count"])
        self.snap_count += 1
        config["SETTINGS"]["snap_count"] = str(self.snap_count)
        with open("src/config.ini", "w") as cfg:
            config.write(cfg)
        print("Saving")
        fp = open(
            "src/Snapshot/dumper/snapshot#{}.pickle".format(self.snap_count), "wb")
        pickle.dump(self.buffer, fp)
        fp.close()
        self.buffer.clear()
