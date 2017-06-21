import pickle
import Item

with open('inventory3.pickle', 'rb') as handle:
    iList = pickle.load(handle)

with open('signedOut3.pickle', 'rb') as handle:
    soList = pickle.load(handle)

with open('returned3.pickle', 'rb') as handle:
    rList = pickle.load(handle)

def showInventory():
    print "\nCurrently in Inventory:"
    for item in iList:
        item.display()

def showSignedOut():
    print"\nCurrently Signed Out:"
    for item in soList:
        item.display()
    print "\n"

def showReturned():
    print"\nIn Warehouse:"
    for item in rList:
        item.display()
    print "\n"

def search(n):
    print "In Inventory: "
    for item in iList:
        if item.name == n:
            item.display()
    print "\n"
    print "Signed Out: "
    for item in soList:
        if item.name == n:
            item.display()
    print "\n"
    print "Returned: "
    for item in rList:
        if item.name == n:
            item.display()
    print "\n"

def sort():
    iList.sort(key=lambda x: x.name, reverse=False)
    soList.sort(key=lambda x: x.name, reverse=False)
    rList.sort(key=lambda x: x.name, reverse=False)

def save():
    with open('inventory3.pickle', 'wb') as handle:
        pickle.dump(iList,handle,-1)

    with open('signedOut3.pickle', 'wb') as handle:
        pickle.dump(soList,handle,-1)

    with open('returned3.pickle', 'wb') as handle:
        pickle.dump(rList,handle,-1)

def showEquipment(owner):
    print "Currently signed out to " + owner + " is:\n"
    retList = []
    for item in soList:
        if item.owner == owner:
            retList.append(item)
    retList.sort(key=lambda x: x.name, reverse=False)
    for item in retList:
        item.display()
    print "\n"


def sortByOwner():
    iList.sort(key=lambda x: x.owner, reverse=False)
    soList.sort(key=lambda x: x.owner, reverse=False)

def getCount(n):
    count = 0
    for item in iList:
        if item.name == n:
            count += item.number
    for item in soList:
        if item.name == n:
            count += item.number
    print "The total count for " + n + " is: " + str(count)

while True:    # infinite loop
    command = raw_input('Enter a command (add, sign out, sign in, delete, used, show, show equipment, sort, search, count, return, quit): ')
    if command == "quit":
        break
    elif command == "add":
        string = raw_input('Enter an item, number, and location to add to inventory using this format without parenthesis (name,count,location): ')
        nS = string.split(",")
        n = nS[0]
        c = int(nS[1])
        loc = nS[2]
        if(any(x for x in iList if x.name == n)):
            if(any(x for x in iList if (x.name == n and x.location != loc))):
                print "You can't add things to a different location, put them all together so you don't lose shit, dumbass"
                save()
                continue
            else:
                for x in iList:
                    if x.name == n:
                        x.number = x.number + c
                        save()
        elif(not any(x for x in iList if x.name == n)):
            iList.append(Item.Item(n,c,loc,"drak"))
            save()

    elif command == "sign out":
        string = raw_input('Enter an item, number, location, and owner to sign out using this format without parenthesis (name,count,location,owner): ')
        nS = string.split(",")
        n = nS[0]
        c = int(nS[1])
        loc = nS[2]
        o = nS[3]
        inInventory = 0
        for x in iList:
            if x.name == n:
                inInventory = x.number
        if(not any(x for x in iList if x.name == n)):#not in inventory
            soList.append(Item.Item(n,c,loc,o))
            save()
        elif(c > inInventory):# if none, if more than are left
            print("You only have " + str(inInventory)+ " in inventory. Try that.")
            save()
            continue
        elif(not any(x for x in soList if x.name == n)):#not signed out
            for x in iList:
                if x.name == n:
                    x.number = x.number - c
            soList.append(Item.Item(n,c,loc,o))
            save()
        elif(any(x for x in soList if (x.name == n and x.owner == o))):#already signed out, same person
            for x in iList:
                if x.name == n:
                    x.number = x.number - c
            for x in soList:
                if x.name == n and x.owner == o:
                    x.number += c
            save()
        elif(any(x for x in soList if (x.name == n and not x.owner == o))):#already signed out, diff people
            for x in iList:
                if x.name == n:
                    x.number = x.number - c
            soList.append(Item.Item(n,c,loc,o))
            save()

    elif command == "sign in":
        string = raw_input('Enter an item, number, and person signing to sign in using this format without parenthesis (name,count,person signing from): ')
        nS = string.split(",")
        n = nS[0]
        c = int(nS[1])
        pO = nS[2]
        if(any(x for x in iList if x.name == n)):
            # flag = False
            # for item in iList:
            #     if item.name == n and not item.location == loc:
            #         print "You can't sign things in to a different location, put them all together so you don't lose shit, dumbass"
            #         flag = True
            # if(flag == True):
            #     continue
            flag = False
            for item in soList:
                if item.name == n and item.number < c and item.owner == pO:
                    print "You can't sign in more than are out. Duh."
                    print "Trying to sign in " + str(c) + " from " + str(item.number) + item.owner
                    flag = True
            if(flag == True):
                continue
            flag = False
            if(not any(x for x in soList if x.name == n)):
                print "this person didn't sign these out. find some else please"
                continue
            for x in iList:
                if x.name == n:
                    x.number += c
                    print "Item belongs in " + x.location
            for x in soList:
                if x.name == n and x.owner == pO:
                    x.number -= c
            for item in soList:
                if item.number == 0:
                    soList.remove(item)
            save()
        else:
            for x in soList:
                if x.name == n and x.owner == pO:
                    x.number -= c
            for item in soList:
                if item.number == 0:
                    soList.remove(item)
            save()
            if(any(x for x in iList if x.name == n)):
                # if(any(x for x in iList if (x.name == n and x.location != loc))):
                #     print "You can't add things to a different location, put them all together so you don't lose shit, dumbass"
                #     save()
                #     continue
                #else:
                for x in iList:
                    if x.name == n:
                        x.number = x.number + c
                        save()
            elif(not any(x for x in iList if x.name == n)):
                loc = raw_input("Please enter a location where the item is going: ")
                iList.append(Item.Item(n,c,loc,"drak"))
                save()



    elif command == "show":
        showInventory()
        showSignedOut()
        showReturned()

    elif command == "delete":
        string = raw_input('Enter an item and number to delete, or just an item to delete all: ')
        nS = string.split(",")
        n = nS[0]
        if len(nS) == 1:
            if(not any(x for x in iList if x.name == n )):#if none in inventory
                print "None in inventory, sorry, you lost it."
                continue
            else:
                if(any(x for x in soList if x.name == n )):#if not all signed in
                    print "You still have some signed out, you can't sign them all back in."
                    save()
                    continue
                for x in iList: #remove from inventory
                    if x.name == n:
                        iList.remove(x)
                save()

        else:
            c = int(nS[1])
            inInventory = 0
            for x in iList:
                if x.name == n:
                    inInventory = x.number
            if(c > inInventory):# if none, if more than are left
                print "You dont have that many in inventory, try again."
                continue
            for x in iList:
                if x.name == n:
                    x.number = x.number - c
            save()

    elif command == "sort":
        sort()

    elif command == "search":
        string = raw_input('Enter an item name to search for: ')
        print string
        search(string)

    elif command == "show equipment":
        string = raw_input('Enter a person to show their signed out equipment: ')
        showEquipment(string)

    elif command == "used":
        string = raw_input('Enter an item that was used with a number and owner (name,owner,number), or just an item and owner to indicate it was all used: ')
        nS = string.split(",")
        n = nS[0]
        o = nS[1]
        if len(nS) == 2:
            if(not any(x for x in soList if x.name == n)):#if none signed out
                print "None signed out, sorry."
                continue
            else:
                for x in soList: #remove from signed out
                    if x.name == n and x.owner == o:
                        soList.remove(x)
                save()

        else:
            c = int(nS[2])
            sO = 0
            for x in soList:
                if x.name == n and x.owner == o:
                    sO = x.number
            if(c > sO):# if none, if more than are left
                print "You dont have that many signed out, try again."
                continue
            for x in soList:
                if x.name == n and x.owner == o:
                    x.number = x.number - c
                    if(x.number == 0):
                        soList.remove(x)
            save()

    elif command == "count":
        string = raw_input('Enter an item to count: ')
        getCount(string)
        print

    elif command == "return":
        string = raw_input('Enter an item and number to return, or just an item to return all: ')
        nS = string.split(",")
        n = nS[0]
        if len(nS) == 1:
            if(not any(x for x in iList if x.name == n )):#if none in inventory
                print "None in inventory, sorry, you lost it."
                continue
            else:
                if(any(x for x in soList if x.name == n )):#if not all signed in
                    print "You still have some signed out, you can't return them all."
                    save()
                    continue
                currNum = 0
                for x in iList: #remove from inventory
                    if x.name == n:
                        iList.remove(x)
                        currNum = x.number
                if(any(x for x in rList if x.name == n )): #already in rList
                    for x in rList: #add to count
                        if x.name == n:
                            x.number += currNum
                    save()
                else:
                    rList.append(Item.Item(n,currNum,"warehouse","jake"))
                    save()
        elif(len(nS) == 2):
            c = int(nS[1])
            inInventory = 0
            for x in iList:
                if x.name == n:
                    inInventory = x.number
            if(c > inInventory):# if none, if more than are left
                print "You dont have that many in inventory, try again."
                continue
            for x in iList:
                if x.name == n:
                    x.number = x.number - c
            if(any(x for x in rList if x.name == n )): #already in rList
                for x in rList: #add to count
                    if x.name == n:
                        x.number += c
                save()
            else:
                rList.append(Item.Item(n,c,"warehouse","jake"))
                save()
            save()

    else:
        print "Not a valid command. Please try something else."

save()
sort()
showInventory()
showSignedOut()
showReturned()
print("\nThanks for working with the inventory. Here's a snapshot of the items you own.")
