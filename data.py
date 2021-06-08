import pickle
pickle_file = open("src/Snapshot/dumper/snapshot#561.pickle", "rb")
objects = []
while True:
    try:
        objects.append(pickle.load(pickle_file))
    except EOFError:
        break
pickle_file.close()

print(objects)