import pandas as pd
from datetime import date
from datetime import datetime
import csv

#readCSV('FISHLIBRARY1.csv')
#readCSV('FISHINVENTORY.csv')

#debug
x = 'debug1'
y = 'debug2'
z = 'debug3'
a = 'debug4'

#current date
d = date.today().strftime("%B %d, %Y")

#time
t = datetime.now().strftime("%H:%M:%S")
h = int(t[0:2])

#fish library pulled from csv file 'FISHLIBRARY1'
FishDict = {}
MyInvenDict = {}

#get fish info from FISHLIBRARY1 csv file and turn it into a dic with all the info we need
def readCSV(csvFile):
    
    #whole main file
    wholeFile = pd.read_csv(csvFile)
    
    #column names
    colTitles = wholeFile.columns

    if csvFile == 'FISHLIBRARY1.csv':
        for x in colTitles:
            FishDict[str(x)] = [int(wholeFile.get(x)[0]),str(wholeFile.get(x)[1]),str(wholeFile.get(x)[2]),int(wholeFile.get(x)[3]),int(wholeFile.get(x)[4]),str(wholeFile.get(x)[5]),str(wholeFile.get(x)[6])]

    elif csvFile == 'FISHINVENTORY.csv':
        for x in colTitles:
            MyInvenDict[str(x)] = str(wholeFile.get(x))

#checks if the fish inputed is in the dict or not
def valid(fish):
    if fish in FishDict:
        return True
    else:
        return False

#returns all the relevent info in a list
def buildProfile(fish):
    price = FishDict[fish][0]
    where = FishDict[fish][1]
    whatTime = FishDict[fish][2]
    season = 'In Season: '
    catchable = False

    #first we will find out when in the year you can catch it

    #if year round
    if FishDict[fish][6] == 'ALL':
        catchable = True
        season += 'Yes'

        #second we check if it is within the timeframe to catch it

        #for any time
        if whatTime == 'ALL':
            catchable = True

        #for daytime fish
        elif FishDict[fish][5] == 'D':
            if FishDict[fish][3] <= h and FishDict[fish][4] > h:
                catchable = True
            else:
                catchable = False

        #for overnight fish
        elif FishDict[fish][5] == 'O':
            if (FishDict[fish][3] <= h and h <= 23):
                catchable = True

            elif (FishDict[fish][4] > h and h >= 0):
                catchable = True
                
            else:
                catchable = False

    #if specific month of year, check if it is that month
    elif d[0:3] in FishDict[fish][6]:
        catchable = True
        season += 'Yes'

        #for any time
        if whatTime == 'ALL':
            catchable = True

        #for daytime fish
        elif FishDict[fish][5] == 'D':
            if FishDict[fish][3] <= h and FishDict[fish][4] > h:
                catchable = True
            else:
                catchable = False

        #for overnight fish
        elif FishDict[fish][5] == 'O':
            if (FishDict[fish][3] <= h and h <= 23):
                catchable = True

            elif (FishDict[fish][4] > h and h >= 0):
                catchable = True
                
            else:
                catchable = False

    #if neither work
    else:
        catchable = False
        season += 'No'

    infoList = [fish,price,where,whatTime,season,catchable]

    return infoList

#returns all the fish that you can catch right now
def catchable():
    catchableFish = []
    
    #loops through the dict to see all catchable fish
    for x in FishDict:
        if buildProfile(x)[-1] == True:
            catchableFish.append(buildProfile(x)[0])
    return catchableFish

#continuisly updates your tab on inputed fish to find out how much you will make
def priceTracker():
    total = 0
    fish = input('Fish name ("e" for exit): ').upper()
    cjChecker = input('Is C.J. there?(N or Y): ').upper()

    #while loop until you wish to exit
    while fish != 'E':

        #checks validity
        if valid(fish) == False:
            print('invalid :(')
            priceTracker()

        if cjChecker == 'N':
            total += buildProfile(fish)[1]
            print(str(total), ' bells')
            fish = input('Fish name ("e" for exit): ').upper()

        elif cjChecker == 'Y':
            total += int((buildProfile(fish)[1] * 1.5))
            print(str(total), ' bells')
            fish = input('Fish name ("e" for exit): ').upper()

    main()

#price info getter
def priceInfo():
    fish = input('Fish name: ').upper()
    cjChecker = input('Is C.J. there?(N or Y): ').upper()

    #checks validity
    if valid(fish) == False:
            print('invalid :(')
            priceInfo()

    if cjChecker == 'N':
        print(str(buildProfile(fish)[1]), 'bells')
    elif cjChecker == 'Y':
        newPrice = buildProfile(fish)[1] * 1.5
        print(int(newPrice), 'bells')

#where getter
def whereInfo():
    fish = input('Fish name: ').upper()

    #checks validity
    if valid(fish) == False:
        print('invalid :(')
        whereInfo()

    #prints formatted string
    print('You can catch it in the',str(buildProfile(fish)[2].lower()))

#time getter
def timeInfo():
    fish = input('Fish name: ').upper()

    #checks validity
    if valid(fish) == False:
        print('invalid :(')
        timeInfo()

    #if you can catch anytime
    if str(FishDict[fish][2]) == 'ALL':
        print('You can catch it whenever!')

    #if you can only catch during certian times
    else:
        print('You can catch it from', str(FishDict[fish][2]))

#season getter
def seasonInfo():
    fish = input('Fish name: ').upper()

    #checks validity
    if valid(fish) == False:
        print('invalid :(')
        seasonInfo()

    #if you can catch anytime
    if str(FishDict[fish][-1]) == 'ALL':
        print('You can catch it whenever!')

    #if you can only catch in certain months
    else:
        print('You can catch it during',FishDict[fish][-1])

def catchInfo():
    fish = input('Fish name: ').upper()

    #checks validity
    if valid(fish) == False:
        print('invalid :(')
        catchInfo()

    if buildProfile(fish)[-1] == False:
        print('nope :(')
    elif buildProfile(fish)[-1] == True:
        print('yes :)')

#returns specific information about said fish
def specificInfo():
    info = input('What would you like to know?: ')

    #while loop until you wish to exit
    while info != 'e':

        #returns all the options you can do in this function
        if info == 'what are my options?':
            print('You can ask for price(price), where to catch(where), what time(time), if its in season(season), can i catch it(catchable), or exit(e).')
            info = input('What would you like to know?: ')

        #returns specific price info
        elif info == 'price':
            priceInfo()
            info = input('What would you like to know?: ')

        #returns where you can find this fish
        elif info == 'where':
            whereInfo()
            info = input('What would you like to know?: ')

        #returns what time you can catch this fish
        elif info == 'time':
            timeInfo()
            info = input('What would you like to know?: ')

        #returns when in the year you can catch the fish
        elif info == 'season':
            seasonInfo()
            info = input('What would you like to know?: ')

        #returns whether this specific fish is catchable
        elif info == 'catchable':
            catchInfo()
            info = input('What would you like to know?: ')

        #invalid input
        else:
            print('invalid :(')
            info = input('What would you like to know?: ')

    main()

#returns what fish you can currently catch in a specific body of water
def catchableHere():
    whereAreWe = input('Where are you?: ').upper()
    catchableWhere = []

    #returns all the options you can do in this function
    if whereAreWe == 'what are my options?':
        print('You are either at the sea, river, pier, mouth, clifftop, or pond.')
        catchableHere()

    #determines where we are
    elif whereAreWe == 'SEA' or whereAreWe == 'RIVER' or whereAreWe == 'PIER' or whereAreWe == 'MOUTH' or whereAreWe == 'CLIFFTOP' or whereAreWe == 'POND':
        for x in FishDict:
            if buildProfile(x)[-1] == True and str(buildProfile(x)[2]) == whereAreWe:
                catchableWhere.append(str(buildProfile(x)[0]))       
                    
    #invalid input
    else:
        print('invalid :(')
        catchableHere()

    print(catchableWhere)
    main()

#to find out what fish you still need
def whatINeed():
    needed = []
    
    for x in FishDict:
        if x not in MyInvenDict:
            needed.append(str(x))

    if len(needed) >= 1:
        print(needed)

    if len(needed) == 0:
        print('You got everything! :)')
    main()
    

#calculate how much your inventory is worth
def worth():
    total = 0

    for x in MyInvenDict:
        total += int(FishDict[x][0])

    print('Your inventory is worth',total,'bells')

#find out if you can catch anything you need now
def whatCanIGet():
    canGet = []
    temp = []
    
    for x in FishDict:
        if x not in MyInvenDict:
            temp = buildProfile(str(x))
            if temp[-1] == True:
                canGet.append([temp[0],temp[2]])
                
    print(canGet)

#main homie
def main():

    #calls readCSV 
    readCSV('FISHLIBRARY1.csv')
    readCSV('FISHINVENTORY.csv')

    #main input
    whatToDo = input('What would you like to do?: ').lower()

    #directory
    if whatToDo == 'what can i do?':
        print("For information on a specific fish: fish info")
        print('To find out what you can catch right now: catchable')
        print('To track how much you will make: price tracker')
        print('To find out specific fish info: specific info')
        print('To find out what you can catch in a specific body of water: catchable here')
        print('To find out what you still need: what i need')
        print('To find out what you already have: what i got')
        print('To find out how much your inventory is worth: worth')
        print('To see if you can catch anything you need right now: what to get')
        print('To exit: e')
        main()

    #gets all the fish info
    elif whatToDo == 'fish info':
        fish = input('Fish name: ').upper()

        #checks validity
        if valid(fish) == False:
                print('invalid :(')
                fish = input('Fish name: ').upper()

        #returns fish info from bp(fish)
        print(buildProfile(fish))
        main()

    #checks what fish are catchable right now
    elif whatToDo == 'catchable':
        
        #calls catchable()
        print(catchable())
        main()

    #brings up a price tracker to track fish
    elif whatToDo == 'price tracker':

        #calls priceTracker()
        priceTracker()

    #returns specific info
    elif whatToDo == 'specific info':

        #calls specificInfo()
        specificInfo()

    #returns what fish are catchable in specific places
    elif whatToDo == 'catchable here':
        
        #calls catchableHere()
        catchableHere()

    #returns what you still need to finish museum
    elif whatToDo == 'what i need':

        #calls whatINeed()
        whatINeed()

    #returns all the fish you have already caught
    elif whatToDo == 'what i got':
        gots = []
        for x in MyInvenDict:
            gots.append(str(x))
        print(gots)
        main()

    elif whatToDo == 'worth':
        worth()
        main()

    elif whatToDo == 'add':
        addToInv()

    elif whatToDo == 'what to get':
        whatCanIGet()
        main()

    #to exit
    elif whatToDo == 'e':
        print('thank you :)')

    #invalid input
    else:
        print('invalid :(')
        main()
