import pickle
import copy
import json


class Recorder:
    def __init__(self):
        with open("src/Snapshot/count.json", "r") as cc:
            count = json.load(cc)["snap_count"]
            if count:
                self.snap_count = count
            else:
                self.snap_count = 0
        self.buffer = []

    def store(self, packet):
        self.buffer.append(copy.deepcopy(packet))

    def save(self):
        self.snap_count += 1
        with open("src/Snapshot/count.json", "w") as cc:
            json.dump({"snap_count": self.snap_count}, cc)
        print("Saving")
        fp = open(
            "src/Snapshot/dumper/snapshot#{}.pickle".format(self.snap_count), "wb")
        pickle.dump(self.buffer, fp)
        fp.close()
        self.buffer.clear()
