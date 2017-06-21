#pickleInit.py - This program initializes the databases for the first time, using the pickling module (like pickling food to save for later, you pickle the data for later).
import Item
import pickle

#a = []

#a.append(Item.Item("cone",35,"117","drak"))

b = []

# with open('inventory3.pickle', 'wb') as handle:
#     pickle.dump(a,handle,-1)

with open('returned3.pickle', 'wb') as handle:
    pickle.dump(b,handle,-1)
